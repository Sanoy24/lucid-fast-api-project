from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.core.database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(Text)  # for long text, no length needed
