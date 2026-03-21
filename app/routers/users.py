
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from pydantic import BaseModel, Field

from starlette import status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Todos,Users
from app.routers.auth import get_current_user
from passlib.context import CryptContext

router= APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str=Field(min_length=6)

    


@router.get("/",status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    #Depends is dependency injection. It means in programming that we need to do something before we execute what we're trying to execute.
    return db.query(Users).filter(Users.id==user.get('id')).first()

# @router.put("/user/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
# async def update_password(user: user_dependency,db:db_dependency,):
#     if user is None:
#         raise HTTPException(status_code=401,detail='Authentication Failed')
#     user_model=db.query(Users).filter(Users.id==user_id).first()
#     user_model.hashed_password=bcrypt_context.hash(.password)

@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401,detail='Authentication Failed')
    user_model.hashed_password=bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit
