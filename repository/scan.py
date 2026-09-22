from datetime import datetime, timedelta, timezone
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
import models


def _format_log(log: models.Logs) -> dict:
    return {
        "id": log.id,
        "time": log.time,
        "teacher_id": log.teacher_id,
        "bus_name": log.bus_name,
        "bus_id": log.bus_id,
        "teacher_name": log.teacher.name if log.teacher else None,
    }


def create_log(log: schemas.CreateLog, db: Session, current_bus: models.Bus):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == log.teacher_id).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher ID {log.teacher_id} is not registered"
        )
    if not teacher.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Teacher ID {log.teacher_id} is currently marked inactive"
        )

    # Debounce check: prevent accidental double-tap within 60 seconds
    recent_threshold = datetime.now(timezone.utc) - timedelta(seconds=60)
    recent_scan = db.query(models.Logs).filter(
        models.Logs.teacher_id == log.teacher_id,
        (models.Logs.bus_name == current_bus.name) | (models.Logs.bus_id == current_bus.id),
        models.Logs.time >= recent_threshold
    ).first()

    if recent_scan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate scan: teacher was already scanned on this bus in the last 60 seconds"
        )

    # Explicitly store bus_name and bus_id
    new_log = models.Logs(
        teacher_id=teacher.id,
        bus_name=current_bus.name,
        bus_id=current_bus.id,
        time=datetime.now(timezone.utc)
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return _format_log(new_log)


def get_all_log(db: Session, skip: int = 0, limit: int = 100) -> List[dict]:
    logs = db.query(models.Logs).order_by(models.Logs.time.desc()).offset(skip).limit(limit).all()
    return [_format_log(log) for log in logs]


def get_individual_log(teacher_id: int, db: Session, skip: int = 0, limit: int = 100) -> List[dict]:
    logs = db.query(models.Logs).filter(
        models.Logs.teacher_id == teacher_id
    ).order_by(models.Logs.time.desc()).offset(skip).limit(limit).all()
    return [_format_log(log) for log in logs]


def get_individual_bus_log(bus_name: str, db: Session, skip: int = 0, limit: int = 100) -> List[dict]:
    bus = db.query(models.Bus).filter(models.Bus.name == bus_name).first()
    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bus '{bus_name}' not found"
        )
    logs = db.query(models.Logs).filter(
        (models.Logs.bus_name == bus_name) | (models.Logs.bus_id == bus.id)
    ).order_by(models.Logs.time.desc()).offset(skip).limit(limit).all()
    return [_format_log(log) for log in logs]


def get_individual_teacher_bus_log(teacher_id: int, bus_name: str, db: Session) -> List[dict]:
    bus = db.query(models.Bus).filter(models.Bus.name == bus_name).first()
    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bus '{bus_name}' not found"
        )
    logs = db.query(models.Logs).filter(
        models.Logs.teacher_id == teacher_id,
        (models.Logs.bus_name == bus_name) | (models.Logs.bus_id == bus.id)
    ).order_by(models.Logs.time.desc()).all()
    return [_format_log(log) for log in logs]