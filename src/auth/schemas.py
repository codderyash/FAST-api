from pydantic import BaseModel,Field
from datetime import datetime
import uuid

class CreateUser(BaseModel):
    username:str
    email:str
    password:str
    first_name:str
    last_name:str

    class Config:
        orm_mode=True

class UserModel(BaseModel):
    uid:uuid.UUID
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    is_verified:bool
    created_at:datetime
    updated_at:datetime
    password_hash:str=Field(exclude=True)

    class Config:
        orm_mode=True

class UserLoginModel(BaseModel):
    email   : str
    password: str

    class Config:
        orm_mode=True
