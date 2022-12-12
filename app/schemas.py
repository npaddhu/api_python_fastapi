from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# Creating schema using pydantic
class PostsBase(BaseModel):
    title: str
    content: str
    published: bool = True

## We can create different Pydantic models for each request like one model for CreatePost and another model for UpdatePost. 
## If one or more models shares some common fields, then we can put them in a single model and inherit them


class PostCreate(PostsBase):
    pass
    #Here all the fields of PostsBase will be inherited to CreatePost model.


class UserCreateReq(BaseModel):
    email: EmailStr
    password: str

class UserCreateRes(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserGetRes(UserCreateRes):    # We can directly use UserCreateRes structure for UserGetRes
    pass

'''
class PostResponse(BaseModel):
    title: str
    content: str
    published: bool
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
'''

class PostResponse(PostsBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserGetRes

    class Config:           # Converts SQLAlchemy mode to Pydantic model
        orm_mode = True


class PostVoteRes(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class UserLoginReq(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]=None

class VoteReq(BaseModel):
    post_id: int
    direction: conint(le=1) #if direction=1 -> like, direction=0 -> remove like
