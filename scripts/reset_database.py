import sys
import os

# Include the project root directory in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import engine, Base
# Import all models to register them with Base.metadata before calling create_all
from backend.models.evidence import Evidence
from backend.models.commits import GitHubCommit
from backend.models.notes import LearningNote
from backend.models.drafts import DailyLog, GeneratedContent, GenerationRun, DraftFeedback
from backend.models.settings import Setting

def init_db():
    """
    Drops and recreates all database tables defined in our models.
    """
    print("Initializing Database...")
    print("Dropping all existing tables (if any)...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating tables based on SQLAlchemy models...")
    Base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()
