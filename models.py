from sqlalchemy import Column,Integer,String,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Teacher(Base):
    __tablename__='teacher'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)

    logs=relationship('Logs',back_populates='teacher')
    bills=relationship('Bill',back_populates='teacher')

class Bus(Base):
    __tablename__='bus'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,unique=True)
    password=Column(String)
    
    logs=relationship('Logs',back_populates='bus')

class Logs(Base):
    __tablename__='logs'
    id=Column(Integer,primary_key=True,index=True)
    time=Column(DateTime,default=datetime.now,index=True)
    teacher_id=Column(Integer,ForeignKey('teacher.id'),index=True)
    bus_name=Column(String,ForeignKey('bus.name'),index=True)

    teacher=relationship('Teacher',back_populates='logs')
    bus=relationship('Bus',back_populates='logs')

class Admin(Base):
    __tablename__='admin'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    password=Column(String)

class Bill(Base):
    __tablename__='bills'
    id=Column(Integer,primary_key=True)
    teacher_id=Column(Integer,ForeignKey('teacher.id'),index=True)
    total_bill=Column(Integer)
    billing_month=Column(String)
    teacher=relationship('Teacher',back_populates='bills')
