from fastapi import status,HTTPException
from sqlalchemy.orm import Session
import schemas,models
from security import hashing

def add(bus:schemas.Bus,db:Session):
    new_bus=models.Bus(name=bus.name,password=hashing.hash_password(bus.password))
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)
    return new_bus

def show(db:Session):
    buses= db.query(models.Bus).all()
    if not buses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not bus found")
    return buses

def show_one(name:str,db:Session):
    bus= db.query(models.Bus).filter(models.Bus.name==name).first()
    if not bus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found")
    return bus
