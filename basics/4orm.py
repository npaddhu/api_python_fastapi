'''
When it comes to working with a DB in a Python application or any other language application, there are couple of ways to interact with the DB.
Here, we saw how to use default Postgres driver to talk to a Postgres DB by sending SQL commands. 
People who are familiar with SQL, they can use this default method to interact with DB by sending SQL commands thru the specific driver in any programming language.

However, There are other methods. One popular method is to interact with DB is ORM(Object Relational Mapper).

ORM(Object Relational Mapper): (Useful link https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/)
    - Layer of abstraction that sits between DB and us(eg: our FastAPI appliaction). So, we never talk to DB directly. We talk to ORM and which talks to DB. So, one of the benefit
    is that we no need to work on SQL any more. Instead of using any raw SQL queries, we will use standard Python code which calls various methods/functions that alternatives 
    into SQL queries themselves.
    - We can perform all DB operations through traditional Python code. No more SQL!

    Traditional vs ORM:

        Traditional: (Connecting to DB thru SQL queries. Here, we need to write sql queries.)
                                                SQL
                FastAPI <-------------------------------------------------------> DATABASE

        ORM: (We will write standard python code and ORM takes and converts into sql and connect to DB with driver psycopg and returns final results.
                Here, we are trying to abstract the complexity of writing sql queries and make use of standard python program language).

                                               _______
                                python         |     |         SQL(psycopg)
                FastAPI <--------------------->| ORM |<-------------------------> DATABASE
                                               |_____|

What can ORMs Do??
    - Instead of manually defining tables in postgres, we can define our tables as Python models.
    - Queries can be made exclusively thru python code. No SQL is necessary.

    eg:
        Creating table:
            class Post(Base):
                __tablename__ = "posts"

                id = Column(Integer, primary_key=True, index=True)
                title = Column(String, index=True, nullable=False)
                content = Column(String, nullable=False)
                published = Column(Boolean)
    
        Querying table:
            db.query(models.Post).filter(models.Post.id == id).first()


SQLALCHEMY:
    - SQLAlchemy is one of the most popular Python ORMs.
    - It is a standalone library and has no association with FastAPI. I can be used in any other python web frameworks or any python based application.


'''