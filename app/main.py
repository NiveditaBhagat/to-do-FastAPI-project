# source venv/bin/activate 
# uvicorn app.main:app --reload
#  it is going to be root folder where we create our fastapi application


from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import auth, todos,admin,users

app=FastAPI()

models.Base.metadata.create_all(bind=engine) #this will only be ran if our todos.db doesnt exist. So if go back to our models file and 
# enhance the todos tables, this will not run automatically and enhance the tables. Its easier just to delete the todos.db file with quck and easy databases. 

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
