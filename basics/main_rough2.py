from distutils.log import debug
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends

import psycopg2
from psycopg2.extras import RealDictCursor
import time

import uvicorn
from sqlalchemy.orm import Session

from . import models, schemas, utils
from database import engine, get_db
#import pdb; pdb.set_trace()
models.Base.metadata.create_all(bind=engine)    # Basically, this creates the table in DB. you can check with 'pgAdmin'. It checks the table name, if the name exists, nothing will happen otherwise it will create a table with the given name.
from typing import List

app = FastAPI()


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


@app.get("/")
def get_root():
    return "Welcome to FastAPI..!"


#Testing session
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    #print(posts)
    return {"status": "successful"}
    '''
    posts = db.query(models.Post)
    print(posts)
    #This prints the actual sql query as db.query converts and returns sql queries.
        # prints: SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts

    posts = db.query(models.Post).all()
    Here: 
        db -> session
        models.Post -> Class name for table that you want to query
    '''


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    '''Returns all the posts available in my_posts/DB'''

    ## Traditional SQL approach
    '''
    query = """ SELECT * FROM posts; """
    cur.execute(query)
    db_posts = cur.fetchall()
    '''

    ## ORM approach
    db_posts = db.query(models.Post).all()
    return db_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)    #returning default created status code
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    '''
    # Create brand new post by inserting the user's post details into db.

    ## Traditional SQL approach
    cur.execute(""" INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    """
    We can use f string here like cur.execute(f"INSERT INTO posts(title, content, published) VALUES('{post.title}', '{post.content}', '{post.published}') RETURNING *")
    It works, but there SQL Injection threat issue with the f string notation. That hacker can inject some sql queries like INSERT INTO and do some issues. 
    So, always go for %s %s %s notation.
    """

    new_post = cur.fetchone()   #This fetchone is Returning * results.
    
    #This will return the inserted data in response. But, actually the data is not inserted into the DB(This we can see in pgAdmin).
    #To insert into the db properly, we need to do commit.
    conn.commit()
    '''

    ## ORM approach
    #new_post = models.Post(title=post.title, content=post.content, published=post.published) 
    # Its difficult to assign the user values field by field in the above statment if there are many fields. so we can un-pack the values and assign like below.
    new_post = models.Post(**post.dict())   #post.dict() returns the user values in the form of python dictionary.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    '''
    ## Traditional SQL approach
    #query = """ SELECT * FROM posts WHERE id = %d; """
    cur.execute(""" SELECT * FROM posts WHERE id = %s; """, (str(id),))  
    # Here, id is integer. But, we have to give the id in the string format in the querry. so convert by adding "str". 
    # Also, the positional variable should be a tuple. thats why it is (str(id), )
    db_post = cur.fetchone()
    '''

    ## ORM approach
    #db_post = db.query(models.Post).filter(models.Post.id == id).all()         # It searches all the records even if you found the record early.
    db_post = db.query(models.Post).filter(models.Post.id == id).first()        # Returns the first matched record 
    '''
    #we can split the query
    post = db.query(models.Post).filter(models.Post.id == id)
    print(post)     # o/p: SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts WHERE posts.id = %(id_1)s
    db_post = post.first()      #o/p: <models.Post object at 0x000002612770E2E0>
    '''
    #print(db_post)

    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,              # standard way to use raise HTTP exceptions
                            detail=f"Post id with {id} was not found")
    
    return db_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    '''
    ## Traditional SQL approach
    cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING *; """, (str(id),))
    deleted_post = cur.fetchone()
    conn.commit()
    '''

    ## ORM approach
    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id with {id} does not exist.")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    '''
    ## Traditional SQL approach
    cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *; """, (post.title, post.content, post.published, str(id)))
    updated_post = cur.fetchone()
    conn.commit()
    '''

    ## ORM approach
    updated_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id with {id} does not exist.")

    # updated_query.update({"title": "updated title", "content": "updated content"}, synchronize_session=False)     ##syn: query.update(python_dictionary, synchronize_session=False)
    updated_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return updated_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateRes)
def create_users(user: schemas.UserCreateReq, db: Session = Depends(get_db)):
    # Hashing the password
    hashed_pwd = utils.get_password_hash(user.password)
    # Updating hashed password so that hashed password will be store in the DB
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schemas.UserGetRes)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User id with {id} was not found")
    
    return user


if __name__=="__main__":
    uvicorn.run("main:app", port=8000, reload=True)