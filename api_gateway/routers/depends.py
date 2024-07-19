from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


bearer_scheme = HTTPBearer(bearerFormat="JWT")


async def get_token(http_auth: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = http_auth.credentials
    return token
