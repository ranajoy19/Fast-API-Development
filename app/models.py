from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from database import Base
from datetime import datetime



class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True,nullable=False,autoincrement=True)
    title = Column(String, index=True,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

