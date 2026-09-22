from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Annotated
import schemas
import database
import models
from repository import teacher as repo_teacher
from security import oauth

router = APIRouter(
    prefix="/teacher",
    tags=["Teachers"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowTeacher)
def create_teacher(
    teacher: schemas.TeacherCreate,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return repo_teacher.create(teacher, db)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowTeacher])
def show_teacher(
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return repo_teacher.show_teacher(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowTeacher)
def show_one_teacher(
    id: int,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return repo_teacher.show_one_teacher(id, db)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_teacher(
    id: int,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return repo_teacher.delete_teacher(id, db)
