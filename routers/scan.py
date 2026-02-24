from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from typing import List
import schemas,database
from repository import scan
from security import oauth

router=APIRouter(
    prefix="/scan",
    tags=["Scans"]
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowLog)
def create_log(log:schemas.CreateLog,db:Session=Depends(database.get_db),current_bus=Depends(oauth.get_current_bus)):
    return scan.create_log(log,db,current_bus)

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.ShowLog])
def get_all_log(db:Session=Depends(database.get_db),current_admin=Depends(oauth.get_current_admin)):
    return scan.get_all_log(db)

@router.get('/teacher/{id}',status_code=status.HTTP_200_OK,response_model=List[schemas.ShowLog])
def get_individual_log(id:int,db:Session=Depends(database.get_db),current_admin=Depends(oauth.get_current_admin)):
    return scan.get_individual_log(id,db)

@router.get('/bus/{bus}',status_code=status.HTTP_200_OK,response_model=List[schemas.ShowLog])
def get_individual_bus_log(bus:str,db:Session=Depends(database.get_db),current_admin=Depends(oauth.get_current_admin)):
    return scan.get_individual_bus_log(bus,db)

@router.get('/teacher/{id}/{bus}',status_code=status.HTTP_200_OK,response_model=List[schemas.ShowLog])
def get_individual_teacher_bus_log(id:int,bus:str,db:Session=Depends(database.get_db),current_admin=Depends(oauth.get_current_admin)):
    return scan.get_individual_teacher_bus_log(id,bus,db)