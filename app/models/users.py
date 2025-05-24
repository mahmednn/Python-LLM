from sqlalchemy import Column, String, Integer, UUID
from uuid import uuid4
from db.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid4())
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
