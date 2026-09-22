from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import models
from .generatebill import generate_monthly_bills


def _format_bill(bill: models.Bill) -> dict:
    return {
        "id": bill.id,
        "teacher_id": bill.teacher_id,
        "total_trips": bill.total_trips,
        "fare_per_trip": bill.fare_per_trip,
        "total_bill": bill.total_bill,
        "billing_month": bill.billing_month,
        "status": bill.status,
        "created_at": bill.created_at,
        "teacher_name": bill.teacher.name if bill.teacher else None,
    }


def get_all_bills(
    db: Session,
    month: Optional[str] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[dict]:
    query = db.query(models.Bill)
    if month:
        query = query.filter(models.Bill.billing_month == month)
    if status_filter:
        query = query.filter(models.Bill.status == status_filter)
    bills = query.order_by(models.Bill.created_at.desc()).offset(skip).limit(limit).all()
    return [_format_bill(b) for b in bills]


def get_teacher_bills(teacher_id: int, db: Session) -> List[dict]:
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher ID {teacher_id} not found"
        )
    bills = db.query(models.Bill).filter(
        models.Bill.teacher_id == teacher_id
    ).order_by(models.Bill.created_at.desc()).all()
    return [_format_bill(b) for b in bills]


def get_bill_by_id(bill_id: int, db: Session) -> dict:
    bill = db.query(models.Bill).filter(models.Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bill ID {bill_id} not found"
        )
    return _format_bill(bill)


def update_bill_status(bill_id: int, new_status: str, db: Session) -> dict:
    bill = db.query(models.Bill).filter(models.Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bill ID {bill_id} not found"
        )
    bill.status = new_status.lower()
    db.commit()
    db.refresh(bill)
    return _format_bill(bill)


def trigger_bill_generation(db: Session) -> dict:
    return generate_monthly_bills(db=db)
