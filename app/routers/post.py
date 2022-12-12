from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas
from database import get_db
import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


#@router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=list[schemas.PostVoteRes])
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): # limit is query parameter
    '''Returns all the posts available in my_posts/DB'''

    ## Traditional SQL approach
    '''
    query = """ SELECT * FROM posts; """
    cur.execute(query)
    db_posts = cur.fetchall()
    '''

    ## ORM approach
    #db_posts = db.query(models.Post).all()

    # Restrict the number data points with the query parameter limit
    #db_posts = db.query(models.Post).limit(limit).all()
    # For skip
    #db_posts = db.query(models.Post).limit(limit).offset(skip).all()
    # search based query parameter
    #db_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    '''
    # if we want to restrict the posts only for logged user then use the below
    db_posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    '''

    #SQL join format: SELECT posts.*, COUNT(votes.post_id) FROM posts LEFT JOIN votes ON posts.id=votes.post_id where posts.id=8 group by posts.id;
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #return db_posts
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)    #returning default created status code
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
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
    #print(current_user)
    #print(current_user.id, current_user.email)
    ## ORM approach
    #new_post = models.Post(title=post.title, content=post.content, published=post.published) 
    # Its difficult to assign the user values field by field in the above statment if there are many fields. so we can un-pack the values and assign like below.
    new_post = models.Post(owner_id=current_user.id, **post.dict())   #post.dict() returns the user values in the form of python dictionary.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#@router.get("/{id}", response_model=schemas.PostResponse)
@router.get("/{id}", response_model=schemas.PostVoteRes)
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
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
    #db_post = db.query(models.Post).filter(models.Post.id == id).first()        # Returns the first matched record 

    db_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
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
    
    '''
    #this is to check whether the correct user is tyring to delete the post or not. 
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    '''

    
    return db_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
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
    
    #this is to check whether the correct the user is tyring to delete the post or not. 
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
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

    #this is to check whether the correct the user is tyring to update the post or not. 
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")



    # updated_query.update({"title": "updated title", "content": "updated content"}, synchronize_session=False)     ##syn: query.update(python_dictionary, synchronize_session=False)
    updated_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return updated_query.first()
