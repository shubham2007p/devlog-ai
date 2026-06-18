import hmac
import hashlib
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.config import settings
from backend.models.commits import GitHubCommit
from backend.models.evidence import Evidence
from backend.utils.logger import get_logger

logger = get_logger("github_service")

def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    """
    Validate the GitHub signature header using the local secret.
    Supports secure constant-time comparisons to prevent timing attacks.
    """
    # Bypass verification locally if the default developer secret placeholder is used
    # and no signature header was received (assisting local testing)
    if not settings.WEBHOOK_SECRET or settings.WEBHOOK_SECRET == "local_webhook_secret_placeholder":
        if not signature_header:
            logger.warning("Signature validation bypassed: Using local placeholder secret and signature header is missing.")
            return True

    if not signature_header:
        logger.error("Signature verification failed: Missing X-Hub-Signature-256 header.")
        return False

    try:
        sha_name, signature = signature_header.split("=")
        if sha_name != "sha256":
            logger.error(f"Signature verification failed: Unsupported signature algorithm '{sha_name}'.")
            return False
        
        # Calculate HMAC digest
        mac = hmac.new(
            settings.WEBHOOK_SECRET.encode("utf-8"),
            msg=payload_body,
            digestmod=hashlib.sha256
        )
        
        # Safe comparison to prevent timing attacks
        is_valid = hmac.compare_digest(mac.hexdigest(), signature)
        if not is_valid:
            logger.error("Signature verification failed: HMAC SHA256 signature mismatch.")
        return is_valid
    except Exception as e:
        logger.error(f"Signature verification failed with error: {e}")
        return False

def process_push_payload(payload: dict, db: Session) -> dict:
    """
    Parses the push payload, extracts individual commits, stores new commits in github_commits,
    creates corresponding timeline logs in the evidence table, and deduplicates already stored SHA values.
    """
    try:
        repo_name = payload.get("repository", {}).get("name")
        ref = payload.get("ref", "")
        # Extract branch name from ref ('refs/heads/main' -> 'main')
        branch_name = ref.replace("refs/heads/", "") if ref else "unknown"

        if not repo_name:
            raise ValueError("Repository name is missing in the payload.")

        commits = payload.get("commits", [])
        logger.info(f"Processing webhook payload for repository '{repo_name}' on branch '{branch_name}' ({len(commits)} commits).")

        commits_added = 0
        commits_ignored = 0

        for commit in commits:
            commit_sha = commit.get("id")
            if not commit_sha:
                logger.warning("Commit missing 'id' (SHA), skipping commit record.")
                continue

            # Prevent Duplicate Commits (TASK-025)
            existing = db.query(GitHubCommit).filter_by(commit_sha=commit_sha).first()
            if existing:
                logger.info(f"Commit {commit_sha[:7]} already exists. Skipping duplicate.")
                commits_ignored += 1
                continue

            # Parse files changed (Added + Removed + Modified)
            added = commit.get("added", [])
            removed = commit.get("removed", [])
            modified = commit.get("modified", [])
            files_changed = list(set(added + removed + modified))

            # Parse timestamp to naive datetime in UTC
            timestamp_str = commit.get("timestamp", "")
            try:
                # standard ISO string conversion
                ts_str = timestamp_str.replace("Z", "+00:00")
                timestamp = datetime.fromisoformat(ts_str)
                if timestamp.tzinfo is not None:
                    timestamp = timestamp.astimezone(timezone.utc).replace(tzinfo=None)
            except Exception as ts_err:
                logger.warning(f"Error parsing commit timestamp '{timestamp_str}': {ts_err}. Falling back to current UTC datetime.")
                timestamp = datetime.utcnow()

            commit_message = commit.get("message", "")
            commit_url = commit.get("url", "")
            author_name = commit.get("author", {}).get("name", "unknown")

            # 1. Store Commit (TASK-023)
            db_commit = GitHubCommit(
                commit_sha=commit_sha,
                repo_name=repo_name,
                branch_name=branch_name,
                commit_message=commit_message,
                commit_url=commit_url,
                author_name=author_name,
                files_changed=files_changed,
                timestamp=timestamp
            )
            db.add(db_commit)

            # 2. Create Timeline Evidence Record (TASK-024)
            first_line_msg = commit_message.split("\n")[0] if commit_message else ""
            db_evidence = Evidence(
                source="github",
                event_type="commit",
                title=f"Commit: {first_line_msg[:60]}",
                content=f"Repo: {repo_name} | Branch: {branch_name}\nCommit: {commit_message}\nFiles Changed: {', '.join(files_changed) if files_changed else 'None'}",
                event_metadata={
                    "repo_name": repo_name,
                    "branch_name": branch_name,
                    "commit_sha": commit_sha,
                    "commit_url": commit_url,
                    "files_changed": files_changed
                },
                event_time=timestamp
            )
            db.add(db_evidence)
            commits_added += 1
            logger.info(f"Saved new commit {commit_sha[:7]} to commits and evidence logs (TASK-023, TASK-024).")

        db.commit()
        logger.info(f"Push webhook completed. Added: {commits_added}, Ignored duplicates: {commits_ignored}.")
        
        return {
            "commits_processed": commits_added,
            "commits_ignored": commits_ignored
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Push webhook database processing failed: {e}")
        raise e
