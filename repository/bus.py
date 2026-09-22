from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
import models
from security import hashing


def add(bus: schemas.BusCreate, db: Session):
    existing = db.query(models.Bus).filter(models.Bus.name == bus.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bus with name '{bus.name}' already exists"
        )
    new_bus = models.Bus(
        name=bus.name,
        route=bus.route,
        password=hashing.hash_password(bus.password),
        is_active=True
    )
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)
    return new_bus


def show(db: Session) -> List[models.Bus]:
    return db.query(models.Bus).all()


def show_one(name: str, db: Session):
    bus = db.query(models.Bus).filter(models.Bus.name == name).first()
    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bus '{name}' not found"
        )
    return bus


def delete_bus(name: str, db: Session):
    bus = show_one(name, db)
    db.delete(bus)
    db.commit()
    return {"detail": f"Bus '{name}' deleted successfully"}
