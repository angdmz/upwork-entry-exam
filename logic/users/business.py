from datetime import datetime

from pydantic import BaseModel, EmailStr

from common import Retrieved


class User(BaseModel):
    email: EmailStr
    
    def email_is(self, email):
        return self.email == email


class RetrievedUser(User, Retrieved):
    pass


class Profile(BaseModel):
    full_name: str
    description: str
    is_favorite: bool = False

    def is_named(self, full_name):
        return self.full_name == full_name

    def is_described_as(self, description):
        return self.description == description


class ProfileUpdate(BaseModel):
    full_name: str | None = None
    description: str | None = None
    is_favorite: bool | None = None


class RetrievedProfile(Profile, Retrieved):
    pass
