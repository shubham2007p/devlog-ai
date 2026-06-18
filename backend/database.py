import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from backend.config import settings

# Parse the database URL and ensure the directory exists for SQLite
if settings.DATABASE_URL.startswith("sqlite:///"):
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    # Handle relative paths properly
    if not os.path.isabs(db_path):
        db_path = os.path.abspath(os.path.join(os.getcwd(), db_path))
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

# Create SQLAlchemy engine
# check_same_thread is needed only for SQLite
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare declarative base using SQLAlchemy 2.x style
class Base(DeclarativeBase):
    pass

# Dependency to get db session in endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
