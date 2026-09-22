from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import database
import models
from . import token

oauth2_scheme_bus = OAuth2PasswordBearer(tokenUrl="/login/bus", scheme_name="BusAuth")
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="/login/admin", scheme_name="AdminAuth")


def get_current_bus(data: str = Depends(oauth2_scheme_bus), db: Session = Depends(database.get_db)) -> models.Bus:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate bus credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    payload = token.verify_access_token(data, credentials_exception)
    if payload.get("role") != "bus":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Bus authorization required"
        )
    bus_name = payload.get("sub")
    bus = db.query(models.Bus).filter(models.Bus.name == bus_name).first()
    if bus is None or not bus.is_active:
        raise credentials_exception
    return bus


def get_current_admin(data: str = Depends(oauth2_scheme_admin), db: Session = Depends(database.get_db)) -> models.Admin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    payload = token.verify_access_token(data, credentials_exception)
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Admin authorization required"
        )
    username = payload.get("sub")
    # Match on username or fallback to id for legacy tokens
    admin = db.query(models.Admin).filter(
        (models.Admin.username == username) | (models.Admin.name == username)
    ).first()
    if admin is None:
        raise credentials_exception
    return admin