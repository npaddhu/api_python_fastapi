'''
Every model represenets a Table in DB.
'''

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from app.database import Base


class Post(Base):
    __tablename__ = "posts"     #This is the table name that we want to create in DB

    #Columns and their properties of the 'posts' table.
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Creating Foreign key
    # Foreign key data type should the type of refernce key in master table. We don't mention the Class name User, instead we mention the table.column like users.id
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Some cases we may need the Parent tables info. For that SQLAlchemy gives a powerful feature for providing the relationship.
    owner = relationship("User")    # Here, we provide Class name only


class User(Base):
    __tablename__ = "users" 

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_numer = Column(String, unique=True, nullable=False)

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

