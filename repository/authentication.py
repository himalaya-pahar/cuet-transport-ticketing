from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from security import hashing, token
import models


def authentication_bus(form_data: OAuth2PasswordRequestForm, db: Session):
    bus = db.query(models.Bus).filter(models.Bus.name == form_data.username).first()
    if not bus or not hashing.verify_password(form_data.password, bus.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bus name or password"
        )
    if not bus.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bus account is inactive"
        )
    access_token = token.create_access_token(data={"sub": bus.name, "role": "bus"})
    return {"access_token": access_token, "token_type": "bearer", "role": "bus"}


def authentication_admin(form_data: OAuth2PasswordRequestForm, db: Session):
    # Support login by username or name
    admin = db.query(models.Admin).filter(
        (models.Admin.username == form_data.username) | (models.Admin.name == form_data.username)
    ).first()
    
    # Also support numeric ID login for backwards compatibility if input is numeric
    if not admin and form_data.username.isdigit():
        admin = db.query(models.Admin).filter(models.Admin.id == int(form_data.username)).first()

    if not admin or not hashing.verify_password(form_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = token.create_access_token(data={"sub": admin.username, "role": "admin"})
    return {"access_token": access_token, "token_type": "bearer", "role": "admin"}


def authentication_unified(form_data: OAuth2PasswordRequestForm, db: Session):
    # 1. Check if user is an Admin
    admin = db.query(models.Admin).filter(
        (models.Admin.username == form_data.username) | (models.Admin.name == form_data.username)
    ).first()
    if not admin and form_data.username.isdigit():
        admin = db.query(models.Admin).filter(models.Admin.id == int(form_data.username)).first()

    if admin and hashing.verify_password(form_data.password, admin.password):
        access_token = token.create_access_token(data={"sub": admin.username, "role": "admin"})
        return {"access_token": access_token, "token_type": "bearer", "role": "admin"}

    # 2. Check if user is a Bus
    bus = db.query(models.Bus).filter(models.Bus.name == form_data.username).first()
    if bus and hashing.verify_password(form_data.password, bus.password):
        if not bus.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bus account is inactive"
            )
        access_token = token.create_access_token(data={"sub": bus.name, "role": "bus"})
        return {"access_token": access_token, "token_type": "bearer", "role": "bus"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username/bus name or password"
    )