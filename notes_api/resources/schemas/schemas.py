from pydantic import BaseModel, EmailStr, Field
from typing import Optional

#регистрации пользователя
class SignupSchema(BaseModel):
    email: EmailStr
    login: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)

# вход пользователя
class SigninSchema(BaseModel):
    login: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)

class PatchUserSchema(BaseModel):
    email: Optional[EmailStr]
    login: Optional[str]
    password: Optional[str]

class NewNoteSchema(BaseModel):
    title: str = Field(..., min_length=1)
    text: str

class PatchNoteSchema(BaseModel):
    title: Optional[str]
    text: Optional[str]

class NoteDataSchema(BaseModel):
    id: int
    title: str
    text: str
