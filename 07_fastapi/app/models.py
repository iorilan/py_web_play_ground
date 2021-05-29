from sqlalchemy import Column, Integer, String
from .database import Base


class TODO(Base):
    __tablename__ = "todos2"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    desc = Column(String)
    created_at = Column(Integer)
