from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Type


class Persistable:
    @classmethod
    def build_from(cls: Type['Persistable'], buildable) -> 'Persistable':
        return cls.parse_obj(buildable.dict())


class BaseRepository:
    
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session
