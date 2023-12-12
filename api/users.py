import http
from uuid import UUID

from fastapi import APIRouter, Body
from fastapi.params import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from common import ObjRef
from dependencies.db import get_session
from dependencies.repositories import get_user_repository, get_profile_repository
from logic.users import User, Profile, ProfileUpdate, RetrievedProfile
from repositories import UserRepository, ProfileRepository

router = APIRouter()


@router.post("/users", status_code=http.HTTPStatus.CREATED)
async def create_user(user: User = Body(..., description="User Data"),
                      user_repository: UserRepository = Depends(get_user_repository),
                      session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user_id = await user_repository.create(user)
    return ObjRef(id=user_id)


@router.get("/users/{user_id}", status_code=http.HTTPStatus.OK)
async def retrieve_user(user_id: UUID = Path(..., description="User ID"),
                        user_repository: UserRepository = Depends(get_user_repository),
                        session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user = await user_repository.retrieve(user_id)
    return user


@router.patch("/users/{user_id}", status_code=http.HTTPStatus.NO_CONTENT)
async def update_user(user_id: UUID = Path(..., description="User ID"),
                      user: User = Body(..., description="User data to update"),
                      user_repository: UserRepository = Depends(get_user_repository),
                      session: AsyncSession = Depends(get_session)):
    async with session.begin():
        await user_repository.update(user_id, user)


@router.delete("/users/{user_id}", status_code=http.HTTPStatus.NO_CONTENT)
async def delete_user(user_id: UUID = Path(..., description="User ID"),
                      user_repository: UserRepository = Depends(get_user_repository),
                      session: AsyncSession = Depends(get_session)):
    async with session.begin():
        await user_repository.delete(user_id)


@router.post("/users/{user_id}/profiles", status_code=http.HTTPStatus.CREATED)
async def create_profile(profile: Profile = Body(..., description="Profile Data"),
                         user_id: UUID = Path(..., description="User ID to add the profile"),
                         profile_repository: ProfileRepository = Depends(get_profile_repository),
                         session: AsyncSession = Depends(get_session)):
    async with session.begin():
        profile_id = await profile_repository.create_for(user_id, profile)
    return ObjRef(id=profile_id)


@router.get("/users/{user_id}/profiles", status_code=http.HTTPStatus.OK)
async def list_profiles(user_id: UUID = Path(..., description="User ID"),
                        profile_repository: ProfileRepository = Depends(get_profile_repository),
                        session: AsyncSession = Depends(get_session)) -> list[RetrievedProfile]:

    async with session.begin():
        profiles = await profile_repository.list(user_id)
    return profiles


@router.get("/profiles/{profile_id}", status_code=http.HTTPStatus.OK)
async def retrieve_profile(profile_id: UUID = Path(..., description="User ID"),
                           profile_repository: ProfileRepository = Depends(get_profile_repository),
                           session: AsyncSession = Depends(get_session)):

    async with session.begin():
        profile = await profile_repository.retrieve(profile_id)
    return profile


@router.patch("/profiles/{profile_id}", status_code=http.HTTPStatus.NO_CONTENT)
async def update_profile(profile_id: UUID = Path(..., description="Profile ID"),
                         profile: ProfileUpdate = Body(..., description="Profile data to update"),
                         profile_repository: ProfileRepository = Depends(get_profile_repository),
                         session: AsyncSession = Depends(get_session)):
    async with session.begin():
        await profile_repository.update(profile_id, profile)


@router.delete("/profiles/{profile_id}", status_code=http.HTTPStatus.NO_CONTENT)
async def delete_profile(profile_id: UUID = Path(..., description="Profile ID"),
                         profile_repository: ProfileRepository = Depends(get_profile_repository),
                         session: AsyncSession = Depends(get_session)):
    async with session.begin():
        await profile_repository.delete(profile_id)
