from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
import schemas,database
from repository import teacher as repo_teacher

router=APIRouter(
    prefix="/teacher",
    tags=["Teachers"]
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def create_teacher(teacher:schemas.Teacher,db:Session=Depends(database.get_db)):
    return repo_teacher.create(teacher,db)

@router.get('/',status_code=status.HTTP_200_OK,response_model=list[schemas.ShowTeacher])
def show_teacher(db:Session=Depends(database.get_db)):
    return repo_teacher.show_teacher(db)

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowTeacher)
def show_one_teacher(id:int,db:Session=Depends(database.get_db)):
    return repo_teacher.show_one_teacher(id,db)
