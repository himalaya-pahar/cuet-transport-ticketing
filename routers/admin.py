from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional
import schemas
import database
import models
from repository import admin as repo_admin
from security import oauth

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post('/', response_model=schemas.ShowAdmin, status_code=status.HTTP_201_CREATED)
def create_admin(
    admin: schemas.AdminCreate,
    db: Annotated[Session, Depends(database.get_db)],
    token: Optional[str] = Depends(oauth.oauth2_scheme_admin)
):
    admin_count = db.query(models.Admin).count()
    if admin_count > 0:
        # Require authentication if an admin already exists
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Admin authentication required to register new admins"
            )
        oauth.get_current_admin(data=token, db=db)
    return repo_admin.create(admin, db)


@router.get('/', response_model=List[schemas.ShowAdmin], status_code=status.HTTP_200_OK)
def get_all_admins(
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return repo_admin.show_admin(db)


@router.get('/{id}', response_model=schemas.ShowAdmin, status_code=status.HTTP_200_OK)
def show_one_admin(
    id: int,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return repo_admin.show_one_admin(id, db)
