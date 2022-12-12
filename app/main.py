from fastapi import FastAPI
import uvicorn
import models
from database import engine
from routers import post, user, auth, vote
from config import settings
from fastapi.middleware.cors import CORSMiddleware

'''
#print(settings)
# Basically, this creates the table in DB. you can check with 'pgAdmin'. It checks the table name, if the name exists, nothing will happen otherwise it will create a table with the given name.
models.Base.metadata.create_all(bind=engine)        # Commenting this as Alembic takes care of all the table operations
'''

app = FastAPI()

# these are origins that we want to allow our API to access
#origins = ["https://www.google.com", "https://www.youtube.com"]     # this allows only google.com and youtube.com domains
origins = ["*"]     # allows all the domains. In our case we can make allow all the domains as our APIs are public APIs. this give great security as we can restrict the origins to access our APIS.
#CORS
app.add_middleware(
    CORSMiddleware,             # which runs as middleware when we get the requests and do some operations
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],        # we can restrict the methods that we want to allow like get, post. * allows all the methods
    allow_headers=["*"],        # allows all the headers
)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI..!"}

app.include_router(post.router)     # Control goes from here to routers/post/ urls
app.include_router(user.router)   
app.include_router(auth.router)  
app.include_router(vote.router)


if __name__=="__main__":
    uvicorn.run("main:app", port=8000, reload=True)