from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone

SECRET_KEY="MOTHERLAND_OR_DEATTH"
ALGORITHM="HS256"
ACCESS_TIMEOUT_EXPIRE_MINUTES=30

def create_access_token(data:dict,expires_delta:timedelta|None=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.now(timezone.utc)+timedelta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TIMEOUT_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        bus_name:str=payload.get("sub")
        if not bus_name:
            raise credentials_exception
        else:
            return bus_name
    except JWTError:
        raise credentials_exception
