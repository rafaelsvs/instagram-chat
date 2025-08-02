from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    instagram_id = Column(String, index=True)
    username = Column(String)
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    origin = Column(String)  # DM, Comment, Story
    created_at = Column(DateTime(timezone=True), server_default=func.now())
