from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
import models


def create(teacher: schemas.TeacherCreate, db: Session):
    existing = db.query(models.Teacher).filter(models.Teacher.id == teacher.id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Teacher with ID {teacher.id} is already registered"
        )
    if teacher.email:
        existing_email = db.query(models.Teacher).filter(models.Teacher.email == teacher.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Teacher with email '{teacher.email}' already exists"
            )

    new_teacher = models.Teacher(
        id=teacher.id,
        name=teacher.name,
        department=teacher.department,
        email=teacher.email,
        phone=teacher.phone,
        is_active=True
    )
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher


def show_teacher(db: Session) -> List[models.Teacher]:
    return db.query(models.Teacher).all()


def show_one_teacher(id: int, db: Session):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No teacher found with id {id}"
        )
    return teacher


def delete_teacher(id: int, db: Session):
    teacher = show_one_teacher(id, db)
    db.delete(teacher)
    db.commit()
    return {"detail": f"Teacher {id} deleted successfully"}