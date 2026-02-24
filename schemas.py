from pydantic import BaseModel

class Bus(BaseModel):
    name: str
    password:str

    
class ShowBus(BaseModel):
    name:str
    class Config():
        from_attributes = True

class Teacher(BaseModel):
    id:int
    name:str

class ShowTeacher(Teacher):
    class Config():
        from_attributes = True


class CreateLog(BaseModel):
    teacher_id:int

    
class ShowLog(CreateLog):
    id:int
    class Config():
        from_attributes = True

class Admin(BaseModel):
    id:int
    name:str
    password:str
class ShowAdmin(BaseModel):
    id:int
    name:str
    class Config():
        from_attributes = True        