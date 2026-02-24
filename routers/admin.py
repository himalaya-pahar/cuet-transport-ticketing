from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
import schemas,database
from typing import Annotated,List
from repository import admin as repo_admin
from security import oauth

router=APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post('/',response_model=schemas.ShowAdmin,status_code=status.HTTP_201_CREATED)
def create_admin(admin:schemas.Admin,db:Annotated[Session,Depends(database.get_db)]):
    return repo_admin.create(admin,db)

@router.get('/',response_model=List[schemas.ShowAdmin],status_code=status.HTTP_200_OK)
def show_admin(db:Annotated[Session,Depends(database.get_db)],current_admin=Depends(oauth.get_current_admin)):
    return repo_admin.show_admin(db)

@router.get('/{id}',response_model=schemas.ShowAdmin,status_code=status.HTTP_200_OK)
def show_admin(id:int,db:Annotated[Session,Depends(database.get_db)],current_admin=Depends(oauth.get_current_admin)):
    return repo_admin.show_one_admin(id,db)
