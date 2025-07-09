from uuid import UUID
from typing import Union
from pydantic import BaseModel, EmailStr

class RegisterUserRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str | None = None

    def get_uuid(self) -> UUID:
        if not self.user_id:
            raise ValueError("Invalid or missing user_id in token")
        return UUID(self.user_id)