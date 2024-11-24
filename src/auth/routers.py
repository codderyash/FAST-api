from  fastapi import APIRouter,Depends,HTTPException,status
from fastapi.responses import JSONResponse
auth_router=APIRouter()
from src.db.main import get_session
from .service import *
from .schemas import *
from .utils import create_access_token,decode_token

userservice=UserService()
@auth_router.post("/signup",response_model=UserModel)
async def create_user_account(user_data:CreateUser,session:AsyncSession=Depends(get_session)):
    user_email=user_data.email

    user_exist=await userservice.user_exist(user_email,session)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Email already exists.")
    user=await userservice.create_user(user_data,session)
    return user

# @auth_router.get("/get_users",response_model=UserModel):
# async def get_users(session:AsyncSession=Depends(get_session)):
#     return await userservice.get_user()

@auth_router.post('/login')
async def login_users(user_data:UserLoginModel,session:AsyncSession=Depends(get_session)):
    email=user_data.email
    password=user_data.password


    user= await userservice.get_user(email,session)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User with email not exist")
    
    verify_user=verify_password(password,user.password_hash)
    if not verify_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid password")
    access_token=create_access_token(user_data={
        'email':user.email,
        'user_uid':str(user.uid)
    })

    refresh_token=create_access_token(user_data={
        'email':user.email,
        'user_uid':str(user.uid)
    },
    expiry=timedelta(days=2),refresh=True)
    
    return JSONResponse(content={
        "message":"Login Successful",
        "access_token":access_token,
        "refresh_token":refresh_token,
        "user":{
            "email":user.email,
            "uid":str(user.uid)
        }
    })
