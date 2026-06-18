from fastapi import APIRouter, Request, Depends, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services import github_service
from backend.utils.logger import get_logger

router = APIRouter()
logger = get_logger("webhook_route")

@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    POST /webhook/github
    Receive and process GitHub push webhooks.
    """
    # Retrieve the raw request bytes to perform HMAC signature validation
    body_bytes = await request.body()
    
    # 1. Validate GitHub Signature (TASK-020)
    if not github_service.verify_signature(body_bytes, x_hub_signature_256):
        logger.warning("Rejecting webhook: Signature verification failed.")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "error": {
                    "code": "INVALID_SIGNATURE",
                    "message": "Invalid webhook signature"
                }
            }
        )
    
    # 2. Parse JSON Payload (TASK-021)
    try:
        payload = await request.json()
    except Exception as parse_err:
        logger.error(f"Failed to parse JSON webhook payload: {parse_err}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "Invalid JSON body payload"
                }
            }
        )

    # 3. Process Payload & Save Records (TASK-021 through TASK-025)
    try:
        processing_result = github_service.process_push_payload(payload, db)
        return {
            "success": True,
            "data": {
                "message": "Webhook processed",
                "details": processing_result
            }
        }
    except Exception as e:
        logger.error(f"Internal error processing push payload: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Webhook processing failed"
                }
            }
        )
