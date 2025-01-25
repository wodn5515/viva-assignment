from pydantic import BaseModel, EmailStr, model_validator
from pydantic_core import PydanticCustomError
from apps.accounts.validations.exceptions import PasswordNotMatched


class SignUp(BaseModel):
    email: EmailStr
    name: str
    password: str
    password_check: str

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.password_check:
            raise PasswordNotMatched
        return self


class Login(BaseModel):
    email: EmailStr
    password: str
