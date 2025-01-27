from pydantic import BaseModel, EmailStr, field_validator
from apps.boards.validations.exceptions import TitleTooLing
from datetime import datetime

POST_MAX_LENGTH = None


class CreatePost(BaseModel):
    title: str
    content: str
    author_id: int

    @field_validator("title", mode="after")
    @classmethod
    def title_validator(cls, value: str):
        if POST_MAX_LENGTH and len(value) > POST_MAX_LENGTH:
            raise TitleTooLing
        return value


class UpdatePost(BaseModel):
    title: str
    content: str
    updated_at: datetime
    post_id: int
    request_user_id: int

    @field_validator("title", mode="after")
    @classmethod
    def title_validator(cls, value: str):
        if POST_MAX_LENGTH and len(value) > POST_MAX_LENGTH:
            raise TitleTooLing
        return value


class LoginEntity(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenEntity(BaseModel):
    refresh: str
