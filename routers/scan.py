from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Annotated
import schemas
import database
import models
from repository import scan
from security import oauth

router = APIRouter(
    prefix="/scan",
    tags=["Scans"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowLog)
def create_log(
    log: schemas.CreateLog,
    db: Annotated[Session, Depends(database.get_db)],
    current_bus: models.Bus = Depends(oauth.get_current_bus)
):
    return scan.create_log(log, db, current_bus)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowLog])
def get_all_log(
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    return scan.get_all_log(db, skip=skip, limit=limit)


@router.get('/teacher/{id}', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowLog])
def get_individual_log(
    id: int,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    return scan.get_individual_log(id, db, skip=skip, limit=limit)


@router.get('/bus/{bus_name}', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowLog])
def get_individual_bus_log(
    bus_name: str,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    return scan.get_individual_bus_log(bus_name, db, skip=skip, limit=limit)


@router.get('/teacher/{id}/bus/{bus_name}', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowLog])
def get_individual_teacher_bus_log(
    id: int,
    bus_name: str,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return scan.get_individual_teacher_bus_log(id, bus_name, db)