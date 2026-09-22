from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
import database
import schemas
from repository import authentication as auth

router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)


@router.post('', response_model=schemas.Token, summary="Unified Login for Admin and Bus")
@router.post('/', response_model=schemas.Token, include_in_schema=False)
def login_unified(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(database.get_db)]):
    return auth.authentication_unified(form_data, db)


@router.post('/bus', response_model=schemas.Token, summary="Dedicated Bus Terminal Login")
def login_bus(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(database.get_db)]):
    return auth.authentication_bus(form_data, db)


@router.post('/admin', response_model=schemas.Token, summary="Dedicated Administrator Login")
def login_admin(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(database.get_db)]):
    return auth.authentication_admin(form_data, db)