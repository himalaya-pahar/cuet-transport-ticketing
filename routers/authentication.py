from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from security import hashing,token
from fastapi.security import OAuth2PasswordRequestForm
import database,models
from repository import authentication as auth
from typing import Annotated

router=APIRouter(
    prefix='/login',
    tags=['Authentication']
)
@router.post('/bus')
def authentication_bus(bus:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    return auth.authentication_bus(bus,db)

@router.post('/admin')
def authentication_admiin(admin:Annotated[OAuth2PasswordRequestForm,Depends()],db:Annotated[Session,Depends(database.get_db)]):
    return auth.authentication_admin(admin,db)