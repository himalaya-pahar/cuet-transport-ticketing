from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Annotated
import schemas
import database
import models
from repository import bus as bus_repo
from security import oauth

router = APIRouter(
    prefix="/bus",
    tags=["Buses"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBus)
def add_bus(
    bus: schemas.BusCreate,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return bus_repo.add(bus, db)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBus])
def show_buses(
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return bus_repo.show(db)


@router.get('/{name}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBus)
def show_one_bus(
    name: str,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return bus_repo.show_one(name, db)


@router.delete('/{name}', status_code=status.HTTP_200_OK)
def delete_bus(
    name: str,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return bus_repo.delete_bus(name, db)
