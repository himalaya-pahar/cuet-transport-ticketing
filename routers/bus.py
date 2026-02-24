from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
import schemas,database
from repository import bus as bus_repo
from security import oauth

router=APIRouter(
    prefix="/bus",
    tags=["Buses"]
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowBus)
def add_bus(bus: schemas.Bus,db: Session=Depends(database.get_db),current_admin=Depends(oauth.get_current_admin)):
    return bus_repo.add(bus,db)

@router.get('/',status_code=status.HTTP_200_OK,response_model=list[schemas.ShowBus])
def show_bus(db: Session=Depends(database.get_db)):
    return bus_repo.show(db)

@router.get('/{name}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBus)
def show_one_bus(name:str,db: Session=Depends(database.get_db)):
    return bus_repo.show_one(name,db)
