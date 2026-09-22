from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


def get_utc_now():
    return datetime.now(timezone.utc)


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    logs = relationship('Logs', back_populates='teacher', cascade="all, delete-orphan")
    bills = relationship('Bill', back_populates='teacher', cascade="all, delete-orphan")


class Bus(Base):
    __tablename__ = 'bus'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    route = Column(String, nullable=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    logs = relationship('Logs', back_populates='bus', cascade="all, delete-orphan", foreign_keys='Logs.bus_name')


class Logs(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, default=get_utc_now, index=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id', ondelete='CASCADE'), nullable=False, index=True)
    bus_name = Column(String, ForeignKey('bus.name', ondelete='CASCADE'), nullable=False, index=True)
    bus_id = Column(Integer, ForeignKey('bus.id', ondelete='CASCADE'), nullable=True, index=True)

    teacher = relationship('Teacher', back_populates='logs')
    bus = relationship('Bus', back_populates='logs', foreign_keys=[bus_name])


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    password = Column(String, nullable=False)


class Bill(Base):
    __tablename__ = 'bills'
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id', ondelete='CASCADE'), nullable=False, index=True)
    total_trips = Column(Integer, default=0, nullable=False)
    fare_per_trip = Column(Integer, default=15, nullable=False)
    total_bill = Column(Integer, nullable=False)
    billing_month = Column(String, nullable=False)
    status = Column(String, default="unpaid", nullable=False)
    created_at = Column(DateTime, default=get_utc_now)

    teacher = relationship('Teacher', back_populates='bills')

    __table_args__ = (
        UniqueConstraint('teacher_id', 'billing_month', name='uq_teacher_billing_month'),
    )
