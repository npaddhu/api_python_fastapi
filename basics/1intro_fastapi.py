
'''
For manipulating the data temporarily, we can create a global variable and update it(instead of using database)
'''


from distutils.log import debug
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

import uvicorn

app = FastAPI()

# Creating global variable and hardcoding few values because if we re-start the service, it will have some values at least otherwise the updated values will be refreshed.
my_posts = [{
    "title": "Top universities in India",
    "content": "IITs",
    "published": True,
    "rating": 4,
    "id": 1             # Unique id to indicate post
}, {
    "title": "Top Restaurents in India",
    "content": "ABC",
    "published": True,
    "rating": 3,
    "id": 2
}]

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
    '''Returns all the posts available in my_posts'''
    return {"data": my_posts}

'''
@app.post("/posts")
def create_posts(post: PayloadSchema):
    post_dict = post.dict()
    post_dict['id'] = randrange(1000000)      # Every time it creates random (almost unique as the range is 1million) integer and it indicates as brand new record
    my_posts.append(post_dict)
    return {"data": post_dict}
'''

"""
@app.get("/posts/{id}")
def get_post(id: int, response: Response):           # def get_post(id: int)     This will automatically converts id into integer and if the path parameter contains string then it returns error
    '''Return a post based on the id. {id} is called as path parameter. FastAPI extracts the {id} value in puts in get_post(id).
    Path parameters always in the form of string'''
    #print(type(id))
    #post = find_post(int(id))
    post = find_post(id)

    return {"post_detail": post}
"""

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_post_index(id):
    for ind, post in enumerate(my_posts):
        if post["id"] == id:
            return ind

'''
@app.get("/posts/latest")   # Technically this is valid, but the path operation mataches with "/posts/{id}", so this won't execute. so, we can make it work by moving this funtion to above the path operation "/posts/{id}" or changing the path url
def get_latest_post():
    return {"latest_post": my_posts[-1]}
'''

'''
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND    # we can return http response here
        return {"post_details": f"Post id with {id} was not found"}     # customized error message

    return {"post_detail": post}
'''


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,              # standard way to use raise HTTP exceptions
                            detail=f"Post id with {id} was not found")
    return {"post_detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)    #returning default created status code
def create_posts(post: PostsSchema):
    post_dict = post.dict()
    post_dict['id'] = randrange(1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = find_post_index(id)

    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id with {id} does not exist.")

    my_posts.pop(post_index)
    #return  {"message": f"Post with id {id} has been deleted successfully!"}   # Ca
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: PostsSchema):
    post_index = find_post_index(id)
    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id with {id} does not exist.")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[post_index] = post_dict

    return {"message": post_dict}


if __name__=="__main__":
    uvicorn.run("main:app", port=8000, reload=True)