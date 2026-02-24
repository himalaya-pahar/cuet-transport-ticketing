from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
import schemas,models,database

def create(teacher:schemas.Teacher,db:Session=Depends(database.get_db)):
    new_teacher=models.Teacher(id=teacher.id,name=teacher.name)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher

def show_teacher(db:Session=Depends(database.get_db)):
    teachers=db.query(models.Teacher).all()
    if not teachers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No teacher found")
    return teachers

def show_one_teacher(id:int,db:Session=Depends(database.get_db)):
    teacher=db.query(models.Teacher).filter(models.Teacher.id==id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No teacher found for this id")
    return teacher