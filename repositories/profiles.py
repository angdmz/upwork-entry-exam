from uuid import UUID, uuid4

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from logic.users import UserNotFound, Profile, RetrievedProfile, ProfileUpdate, ProfileNotFound
from models.users import Profile as ProfileModel
from models.users import User as UserModel
from repositories.common import BaseRepository, Persistable


class PersistableProfile(Profile, Persistable):

    async def persist_to(self, session: AsyncSession, user_id: UUID):
        profile = ProfileModel(id=uuid4(),
                               full_name=self.full_name,
                               description=self.description,
                               user_id=user_id,
                               is_favorite=self.is_favorite)
        session.add(profile)
        return profile.id


class Repository(BaseRepository):
    PROFILE_QUERY = select(ProfileModel).select_from(ProfileModel)

    async def create_for(self, user_id: UUID, profile: Profile):
        persistable = PersistableProfile.build_from(profile)
        return await persistable.persist_to(self.async_session, user_id)

    async def retrieve(self, user_id: UUID):
        query = self.PROFILE_QUERY.where(ProfileModel.id == user_id)
        res = await self.async_session.execute(query)
        res_all = res.all()
        if len(res_all) > 0:
            model = res_all[0][0]
            returnable = RetrievedProfile(
                id=model.id,
                full_name=model.full_name,
                description=model.description,
                is_favorite=model.is_favorite,
                created_at=model.created_at,
                updated_at=model.updated_at)
            return returnable
        raise UserNotFound(user_id)

    async def update(self, profile_id: UUID, profile: ProfileUpdate):
        query = self.PROFILE_QUERY.where(ProfileModel.id == profile_id)
        res = await self.async_session.execute(query)
        res_all = res.all()
        if len(res_all) > 0:
            model = res_all[0][0]
            fields_to_update = profile.model_dump(exclude_none=True)
            for field, value in fields_to_update.items():
                setattr(model, field, value)
            self.async_session.add(model)
            return
        raise UserNotFound(profile_id)

    async def delete(self, profile_id: UUID):
        query = delete(ProfileModel).where(ProfileModel.id == profile_id)
        res = await self.async_session.execute(query)
        if res.rowcount == 0:
            raise ProfileNotFound(profile_id)

    async def list(self, user_id):
        query = self.PROFILE_QUERY.where(UserModel.id == user_id)
        res = await self.async_session.execute(query)
        res_all = res.all()
        if len(res_all) > 0:
            returnable = []
            for res in res_all:
                model = res[0]
                returnable.append(RetrievedProfile(
                    id=model.id,
                    full_name=model.full_name,
                    description=model.description,
                    is_favorite=model.is_favorite,
                    created_at=model.created_at,
                    updated_at=model.updated_at))
            return returnable
        raise UserNotFound(user_id)
