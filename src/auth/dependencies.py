from fastapi.security import HTTPBearer
from .utils import decode_token
from fastapi import status,HTTPException
class HTTPBearerToken(HTTPBearer):
    def __init__(self, *, auto_error = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request):
        creds= await super().__call__(request)
        token=creds.credentials
        token_data=decode_token(token)

        if not self.token_valid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
        
        if token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide access token")

        return creds

    
    def token_valid(self,token:str):
        token_data=decode_token(token)
        return True if token_data is not None else False