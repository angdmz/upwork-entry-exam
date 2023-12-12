from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.orm import mapped_column, relationship

from models.base import BaseModelWithID


class User(BaseModelWithID):
    __tablename__ = "users"

    email = Column(String, nullable=False)
    profiles = relationship("Profile", back_populates="user", cascade="all, delete-orphan")


class Profile(BaseModelWithID):
    __tablename__ = "profiles"

    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="profiles")
    full_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    is_favorite = Column(BOOLEAN, nullable=False, default=True)
