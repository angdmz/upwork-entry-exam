from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ObjRef(BaseModel):
    id: UUID


class Retrieved(ObjRef):
    created_at: datetime
    updated_at: datetime
