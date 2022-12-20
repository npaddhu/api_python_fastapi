'''DB connection details.'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

'''
Connection string URL format(which is used to pass to the SQLALCHEMY).
SQLALCHEMY_DATABASE_URL = 'TypeOfDatabase://<username>:<password>@<ip-address/hostname>/<database_name>'
'''
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi'    # Not the best practice to hardcode the credentials.
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#Engine is responsible for SQLAlchemy to connect to PostgreSQL. So, create engine as like below
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#We have to make use of "Session" to talk to the SQL DB.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#To inherit each of the database models, we will be using the below mentioned Base class.
Base = declarative_base()


# Dependency
'''The session object is responsible for talking with DB. This function is created for getting the DB session. Everytime we get the DB connection or 
session when we get the request. And then built the sql statements. Finally, close the session once it is done.)
'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
