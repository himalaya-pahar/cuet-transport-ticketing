from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


# ==========================
# Token Schemas
# ==========================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


# ==========================
# Bus Schemas
# ==========================
class BusBase(BaseModel):
    name: str
    route: Optional[str] = None


class BusCreate(BusBase):
    password: str


class ShowBus(BusBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# Keep legacy aliases for backwards compatibility
Bus = BusCreate


# ==========================
# Teacher Schemas
# ==========================
class TeacherBase(BaseModel):
    id: int
    name: str
    department: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class ShowTeacher(TeacherBase):
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


Teacher = TeacherCreate


# ==========================
# Admin Schemas
# ==========================
class AdminBase(BaseModel):
    username: str
    name: str
    email: Optional[str] = None


class AdminCreate(AdminBase):
    password: str


class ShowAdmin(AdminBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


Admin = AdminCreate


# ==========================
# Scan / Log Schemas
# ==========================
class CreateLog(BaseModel):
    teacher_id: int


class ShowLog(BaseModel):
    id: int
    time: datetime
    teacher_id: int
    bus_name: str
    bus_id: Optional[int] = None
    teacher_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================
# Bill Schemas
# ==========================
class ShowBill(BaseModel):
    id: int
    teacher_id: int
    total_trips: int
    fare_per_trip: int
    total_bill: int
    billing_month: str
    status: str
    created_at: datetime
    teacher_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class BillUpdateStatus(BaseModel):
    status: str  # "paid", "unpaid", "cancelled"


class GenerateBillResponse(BaseModel):
    message: str
    bills_generated: int
    billing_month: str