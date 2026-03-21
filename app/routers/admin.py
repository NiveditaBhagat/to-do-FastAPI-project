from turtle import st
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from pydantic import BaseModel, Field

from starlette import status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Todos
from app.routers.auth import get_current_user

router= APIRouter(

    prefix='/admin',
    tags=['admin']
)

# models.Base.metadata.create_all(bind=engine) #this will only be ran if our todos.db doesnt exist. So if go back to our models file and 
# # enhance the todos tables, this will not run automatically and enhance the tables. Its easier just to delete the todos.db file with quck and easy databases. 

# app.include_router(auth.router)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]


@router.get("/todos",status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401,detail='Authentication Failed')
    return db.query(Todos).all()

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db:db_dependency):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401,detail='Authentication Failed')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo not found')
    db.query(Todos).filter(Todos.id==todo_id).first().delete()
    db.commit()