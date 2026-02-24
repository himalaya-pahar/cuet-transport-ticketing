from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
import schemas,database
from security import hashing
from typing import Annotated
import models

def create(admin:schemas.Admin,db:Annotated[Session,Depends(database.get_db)]):
    new_admin=models.Admin(id=admin.id,name=admin.name,password=hashing.hash_password(admin.password))
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

def show_admin(db:Annotated[Session,Depends(database.get_db)]):
    admins=db.query(models.Admin).all()
    if not admins:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no admin found")
    return admins

def show_one_admin(id:int,db:Annotated[Session,Depends(database.get_db)]):
    admin=db.query(models.Admin).filter(models.Admin.id==id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no admin found")
    return admin