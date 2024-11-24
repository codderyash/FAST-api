from passlib.context import CryptContext
from datetime import timedelta
from datetime import datetime
from src.config import Config
import jwt
import uuid
passwd_context=CryptContext(
    schemes=["bcrypt"],
)
ACCESS_TOKEN_EXPIRY=3600
def generate_hash_password(password:str):
    return passwd_context.hash(password)

def verify_password(password:str,hash:str):
    return passwd_context.verify(password,hash)

def create_access_token(user_data:dict,expiry:timedelta=None,refresh:bool=False):
    payload={}
    payload['user']=user_data
    payload['exp']=datetime.now()+(expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti']=str(uuid.uuid4())
    payload['refresh']=refresh 

    token=jwt.encode(payload=payload,key=Config.JWT_SECRET,algorithm=Config.JWT_ALGORITHM)
    return token

def decode_token(token:str):
    try:
        token_data=jwt.decode(jwt=token,algorithms=[Config.JWT_ALGORITHM],key=Config.JWT_SECRET)
        return token_data
    except jwt.PyJWTError as e:
        return None