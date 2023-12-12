from uuid import UUID, uuid4

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from logic.users import User, UserNotFound, RetrievedUser
from models.users import User as UserModel
from repositories.common import BaseRepository, Persistable


class PersistableUser(User, Persistable):

    async def persist_to(self, session: AsyncSession):
        user = UserModel(id=uuid4(), email=self.email)
        session.add(user)
        return user.id


class Repository(BaseRepository):

    USER_QUERY = select(UserModel).select_from(UserModel)

    async def create(self, user: User):
        persistable = PersistableUser.build_from(user)
        return await persistable.persist_to(self.async_session)

    async def retrieve(self, user_id: UUID):
        query = self.USER_QUERY.where(UserModel.id == user_id)
        res = await self.async_session.execute(query)
        res_all = res.all()
        if len(res_all) > 0:
            model = res_all[0][0]
            returnable = RetrievedUser(
                id=model.id,
                email=model.email,
                created_at=model.created_at,
                updated_at=model.updated_at)
            return returnable
        raise UserNotFound(user_id)

    async def update(self, user_id: UUID, user: User):
        query = self.USER_QUERY.where(UserModel.id == user_id)
        res = await self.async_session.execute(query)
        res_all = res.all()
        if len(res_all) > 0:
            model = res_all[0][0]
            model.email = user.email
            self.async_session.add(model)
            return
        raise UserNotFound(user_id)

    async def delete(self, user_id):
        query = delete(UserModel).where(UserModel.id == user_id)
        res = await self.async_session.execute(query)
        if res.rowcount == 0:
            raise UserNotFound(user_id)
