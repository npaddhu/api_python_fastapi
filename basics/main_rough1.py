

from distutils.log import debug
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
import time

import uvicorn

app = FastAPI()

'''
#DB connection
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print('Database connection was successfull.')
        break   # Once we get the DB connection, come out of the loop.

    except Exception as error:
        print("Connecting to DB failed.")
        print("Error: ", error)
        time.sleep(2)   # Wait for 2 seconds and then try to connect db
'''

# Creating schema using pydantic
class PostsSchema(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def get_root():
    return "Welcome to FastAPI..!"


@app.get("/posts")
def get_posts():
    '''Returns all the posts available in my_posts/DB'''
    query = """ SELECT * FROM posts; """
    cur.execute(query)
    db_posts = cur.fetchall()
    #return {"data": my_posts}
    return {"data": db_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)    #returning default created status code
def create_posts(post: PostsSchema):
    # Create brand new post by inserting the user's post details into db.
    cur.execute(""" INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    '''
    We can use f string here like cur.execute(f"INSERT INTO posts(title, content, published) VALUES('{post.title}', '{post.content}', '{post.published}') RETURNING *")
    It works, but there SQL Injection threat issue with the f string notation. That hacker can inject some sql queries like INSERT INTO and do some issues. 
    So, always go for %s %s %s notation.
    '''

    new_post = cur.fetchone()   #This fetchone is Returning * results.
    
    #This will return the inserted data in response. But, actually the data is not inserted into the DB(This we can see in pgAdmin).
    #To insert into the db properly, we need to do commit.
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    #query = """ SELECT * FROM posts WHERE id = %d; """
    cur.execute(""" SELECT * FROM posts WHERE id = %s; """, (str(id),))  
    # Here, id is integer. But, we have to give the id in the string format in the querry. so convert by adding "str". 
    # Also, the positional variable should be a tuple. thats why it is (str(id), )
    db_post = cur.fetchone()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,              # standard way to use raise HTTP exceptions
                            detail=f"Post id with {id} was not found")
    
    return {"post_detail": db_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING *; """, (str(id),))
    deleted_post = cur.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id with {id} does not exist.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: PostsSchema):
    cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *; """, (post.title, post.content, post.published, str(id)))
    updated_post = cur.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id with {id} does not exist.")

    return {"data": updated_post}


if __name__=="__main__":
    uvicorn.run("main:app", port=8000, reload=True)