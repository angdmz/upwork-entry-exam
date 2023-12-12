from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db import get_session
from repositories import UserRepository, ProfileRepository


def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)


def get_profile_repository(session: AsyncSession = Depends(get_session)):
    return ProfileRepository(session)
