'''
Pydantic Models vs SQLAlchemy Models:

Pydantic Models:
    - Schema/Pydantic models define the structure of a Request and Response.
    - This ensure that when a user wants to create a post, the request will only go through if it has a 'title' and 'content' in the body(In our PostSchema example).

     ___________________                                 ______________
    |                   | Request(Schema/Pydantic model) |            |  
    |    Browser        |------------------------------> |  FastAPI   |
    |                   |<----------------------------   |            |
    |___________________|Response(Schema/Pydantic model) |____________|

    (When trigger a request, Pydantic model validates the request for all the fields(like field names and field types). So that we can restrict the user to send only what we expect).
    Note: Technically, we don't need the Pydantic model. but when we build APIs, we strictly want to define what kind of data we can receive and/or send from/to the user.
    (We can have different models for each of the request)

SQLAlchemy Models:
    - Responsible for defining the columns of our 'posts' table within postgres(In our case).
    - Is used to query, create, delete, and update entries within the database.
'''