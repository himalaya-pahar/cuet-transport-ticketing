from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from security import hashing,token
from fastapi.security import OAuth2PasswordRequestForm
import database,models
from typing import Annotated

def authentication_bus(bus:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    find_bus=db.query(models.Bus).filter(models.Bus.name==bus.username).first()
    if not find_bus:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect name or password")
    if not hashing.verify_password(bus.password,find_bus.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect name or password")
    access_token=token.create_access_token(data={"sub":bus.username})
    return {"access_token": access_token,"token_type":"bearer"}

def authentication_admin(admin:Annotated[OAuth2PasswordRequestForm,Depends()],db:Annotated[Session,Depends(database.get_db)]):
    find_admin=db.query(models.Admin).filter(models.Admin.id==admin.username).first()
    if not find_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect name or password")
    if not hashing.verify_password(admin.password,find_admin.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect name or password")
    access_token=token.create_access_token(data={"sub":admin.username})
    return {"access_token": access_token,"token_type":"bearer"}