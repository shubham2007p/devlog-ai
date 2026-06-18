from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base

class Setting(Base):
    """
    Stores key-value pair settings configurations for the application.
    """
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    setting_key: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    setting_value: Mapped[str] = mapped_column(Text, nullable=False)
