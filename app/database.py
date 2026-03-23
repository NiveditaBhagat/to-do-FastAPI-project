from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
# SQLALCHEMY_DATABASE_URL='sqlite:///./todosapp.db'  # this url is used to create location of this database on our fastAPI application. 
# Our database is going to be inside this directory of our to do app.

# databse engine is something that we can use to be able to open up a connection and be able to use our database.
load_dotenv()

SQLALCHEMY_DATABASE_URL=os.getenv("DATABASE_URL")
print(SQLALCHEMY_DATABASE_URL)
engine=create_engine(SQLALCHEMY_DATABASE_URL)

# create a session local and each instance of the session local will have a database session.The class itself is not a database session yet.

SessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base= declarative_base()