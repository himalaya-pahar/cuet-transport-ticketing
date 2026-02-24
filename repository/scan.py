from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas,models,database

def create_log(log,db,current_bus):
    check_teacher=db.query(models.Teacher).filter(models.Teacher.id==log.teacher_id).first()

    if not check_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Teacher not registered")

    new_log=models.Logs(teacher_id=log.teacher_id,bus_name=current_bus.name)
    
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def get_all_log(db:Session=Depends(database.get_db)):
    logs=db.query(models.Logs).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No logs found")
    return logs

def get_individual_log(id:int,db:Session=Depends(database.get_db)):
    logs=db.query(models.Logs).filter(models.Logs.teacher_id==id).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No logs found")
    return logs

def get_individual_bus_log(bus:str,db:Session=Depends(database.get_db)):
    logs=db.query(models.Logs).filter(models.Logs.bus_name==bus).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No logs found for that bus")
    return logs

def get_individual_teacher_bus_log(id:int,bus:str,db:Session=Depends(database.get_db)):
    logs=db.query(models.Logs).filter(models.Logs.teacher_id==id).filter(models.Logs.bus_name==bus).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No logs found")
    return logs