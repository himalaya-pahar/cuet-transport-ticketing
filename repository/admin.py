from fastapi import status, HTTPException
from sqlalchemy.orm import Session
import schemas
import models
from security import hashing


def create(admin: schemas.AdminCreate, db: Session):
    existing = db.query(models.Admin).filter(models.Admin.username == admin.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Admin with username '{admin.username}' already exists"
        )
    new_admin = models.Admin(
        username=admin.username,
        name=admin.name,
        email=admin.email,
        password=hashing.hash_password(admin.password)
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


def show_admin(db: Session):
    return db.query(models.Admin).all()


def show_one_admin(id: int, db: Session):
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id {id} not found"
        )
    return admin