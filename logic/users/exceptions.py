from uuid import UUID

from exceptions import ResourceNotFound


class UserNotFound(ResourceNotFound):
    def __init__(self, user_id: UUID):
        super().__init__(f"User not found. ID: {user_id}")


class ProfileNotFound(ResourceNotFound):
    def __init__(self, profile_id: UUID):
        super().__init__(f"Profile not found. ID: {profile_id}")
