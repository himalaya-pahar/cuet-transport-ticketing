from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
import database,models
from . import token

oauth2_scheme_bus=OAuth2PasswordBearer(tokenUrl="/login/bus")

def get_current_bus(data:str=Depends(oauth2_scheme_bus),db:Session=Depends(database.get_db)):
    credentials_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    bus_name=token.verify_access_token(data,credentials_exception)
    bus=db.query(models.Bus).filter(models.Bus.name==bus_name).first()
    if bus is None:
        raise credentials_exception
    return bus

oauth2_scheme_admin=OAuth2PasswordBearer(tokenUrl="/login/admin")

def get_current_admin(data:str=Depends(oauth2_scheme_admin),db:Session=Depends(database.get_db)):
    credentials_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    admin_id=token.verify_access_token(data,credentials_exception)
    admin=db.query(models.Admin).filter(models.Admin.id==admin_id).first()
    if admin is None:
        raise credentials_exception
    return admin