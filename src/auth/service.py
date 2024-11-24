from .models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from .schemas import CreateUser
from .utils import *
class UserService:
    async def get_user(self,email:str,session:AsyncSession):
        statement= select(User).where(User.email==email)
        result= await session.execute(statement)
        user=result.scalar()
        return user
    
    async def user_exist(self,email,session:AsyncSession):
        user=await self.get_user(email,session)
        if user :
            return True
        return False
    
    async def create_user(self,user_data:CreateUser,session:AsyncSession):
        user_data_dict=user_data.model_dump()
        new_user=User(**user_data_dict)
        new_user.password_hash=generate_hash_password(user_data_dict['password'])
        session.add(new_user)
        await session.commit()
        return new_user

    