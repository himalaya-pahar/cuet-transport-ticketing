from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated
import schemas
import database
import models
from repository import bill as repo_bill
from security import oauth

router = APIRouter(
    prefix="/bill",
    tags=["Bills"]
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBill])
def get_all_bills(
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin),
    month: Optional[str] = Query(None, description="Filter by billing month, e.g. 'February-2026'"),
    status: Optional[str] = Query(None, description="Filter by status: 'unpaid' or 'paid'"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    return repo_bill.get_all_bills(db, month=month, status_filter=status, skip=skip, limit=limit)


@router.get('/teacher/{teacher_id}', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBill])
def get_teacher_bills(
    teacher_id: int,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return repo_bill.get_teacher_bills(teacher_id, db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBill)
def get_bill_by_id(
    id: int,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return repo_bill.get_bill_by_id(id, db)


@router.patch('/{id}/status', status_code=status.HTTP_200_OK, response_model=schemas.ShowBill)
def update_bill_status(
    id: int,
    payload: schemas.BillUpdateStatus,
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return repo_bill.update_bill_status(id, payload.status, db)


@router.post('/generate', status_code=status.HTTP_200_OK, response_model=schemas.GenerateBillResponse)
def trigger_bill_generation(
    db: Annotated[Session, Depends(database.get_db)],
    current_admin: models.Admin = Depends(oauth.get_current_admin)
):
    return repo_bill.trigger_bill_generation(db)
