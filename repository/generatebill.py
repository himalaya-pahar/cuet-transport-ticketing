from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from datetime import datetime,timedelta

def bill():
    print ("Generating bill successfully")
    db=SessionLocal()
    teachers=db.query(models.Teacher).all()
    if not teachers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no teachers found")
    
    today=datetime.now()
    first_day_current_month = today.replace(day=1)
    last_day_of_prev_month = first_day_current_month-timedelta(days=1)
    first_day_of_prev_month = last_day_of_prev_month.replace(day=1)
    billing_month=first_day_of_prev_month.strftime("%B-%Y")
    for teacher in teachers:
        total_trip=db.query(models.Logs).filter(
            models.Logs.teacher_id==teacher.id,
            models.Logs.time >= first_day_of_prev_month,
            models.Logs.time <= last_day_of_prev_month
        ).count()
        if total_trip!=0:
            total_bill=total_trip*15
            new_bill=models.Bill(teacher_id=teacher.id,total_bill=total_bill,billing_month=billing_month)
            db.add(new_bill)
    db.commit()
    db.close()

