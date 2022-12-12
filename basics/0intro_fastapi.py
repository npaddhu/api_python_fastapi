'''
Course: Python API Development for Beginners; Link: https://www.youtube.com/watch?v=0sOvCWFmrtA
Author: Sanjeev Thiagarajan; YouTube: https://www.youtube.com/channel/UC2sYgV-NV6S5_-pqLGChoNQ

Goal: 
    - To build-out fully featured API that includes 1. Authentication, 2. CRUD Operation, 3. Validation, 4. Documentation
    - We will also learn the tools around building this robust API
    - SQL (Basics, Methods to integrate queries in API 1.Raw sql queries, 2.ORMs)
    - Alembic (Database migration tool which allows to do incremental data base schema changes) 
    - Postman (To construct http packets to test API during the development)
    - Automation of integration Test (To run Automation to make sure haven't broken the pre-existing functionality)
    - Deployment (1.unix cloud instances, 2. Nginx, 3. Heroku(Free, where we can deploy our services))
    - Docker (Process to Dockerize the API)
    - CI/CD pipeline using GitHub actions


Tech Stack:
    - FastAPI 
            Reasons to choose FastAPI: 
                1. Really fast, not only in terms of perfomance but also the development.
                2. Auto documentation functionality. API documentations is important as we need to tell how it works. 
                   We no need to update the documentation whenever there is a change to API. this is cumbersome task. FastAPI automatically documents the changes.
    - PostgreSQL DB
    - SQLAlchemy
'''




from fastapi import FastAPI
from fastapi.params import Body
from typing import Optional

app = FastAPI()

@app.get("/")           #-> this is called 'Path operations' or 'Routing' in other programming languages; #Decorating root function; 
def root():
    return {"message": "Welcome To FastAPI!!"}

@app.get("/posts")
def posts():
    return {"data": "These are your posts"}

#Note: If the path operations are same, then FastAPI executes the first function(without error) that match with the path operation. So the order matters when the path operations are same.


@app.post("/posts")
def createPosts(payload: dict = Body(...)):     # It extracts all the contents given in the body in the form of Python dictionary and puts in 'payload' argument
    #print("Received data", payload)
    #return {"message": "successfully created posts"}
    return {"message": f"Title - {payload['title']} Content - {payload['content']}"}

'''
Whey we need Schema??

    - It's pain to get all the values from the Body.
    - The client can send whatever data they want.
    - The data is not getting validated.
    - We ultimately want to force the client to send data in a schema that we expect.

For this we Pydantic is useful for defining the schema.
Note: Technically, Pydantic has nothing to do with FastAPI, it's own and complete library which can be used for any Python application.
'''

from pydantic import BaseModel

class PayloadSchema(BaseModel):
    title: str
    content: str
    published: bool = True          # Optional bool values; Here, True is default value.
    rating: Optional[int] = None    # Optoinal integer value; default vlaue is None

@app.post("/createposts1")
def createPosts1(payload: PayloadSchema):       # FastAPI intenally validates the PayloadSchema against the payload i.e it checks title and cotent fields and their types
    print(payload); print(payload.title); print(payload.content) #print(payload.name)
    print(payload.published); print(payload.rating)
    print(type(payload))    #Here, payload is a pydantic model type
    print(payload.dict())   #To convert into a python object dictionary, use payload.dict()
    return {"message": payload}

'''
Note:
    1. If user posts extra fields in the Body part, then FastAPI simply ignores and takes only the mentioned values in the Schema.
    2. If any of the fields that are mentioned in the schema are not present in the Body, then it will return 422 unprocessable entry message.
    3. if there is a bug, then it returns 500 internal server error.
    4. If the API request is good and validates properly then fastapi returns 200 Ok SUCCESS message.
'''

'''
CRUD: (If the application is based on CRUD operations it supports Create, Read, Update, Delete)

Create:
    Http Method: Post; Path Operation: /posts ; Python Syntax: @app.post("/posts")
Read:
    Http Method: Get; Path Operation: /posts  (OR) /posts/:id ; Python Syntax: @app.get("/posts") (OR) @app.get("/posts/{id}")
Update:
    Http Method: Put/Patch (Put-Updates everything, eg: complete post, Patch=updates specific fields, eg: updates 'title'); Path Operation: /posts/:id ; Python Syntax: @app.put("/posts/{id}")
Delete:
    Http Method: Delete; Path Operation: /posts/:id ; Python Syntax: @app.delete("/posts/{id}")
'''


'''
Note: Documentation is automatically prepared with the FastAPI. 
    - http://127.0.0.1:8000/docs link which is similar to swagger.
    - http://127.0.0.1:8000/redoc is another link which gives different representation.
'''