import psycopg2

from psycopg2.extras import RealDictCursor
import time
'''
try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
    # Host can be cloud instance if we are dealing with cloud
    cursor = conn.cursor()
    print("Database connection was successful.")

except Exception as error:
    print("Connecting to Database failed.")
    print("Error: ", error)
'''

# Without connecting to DB, the application can't get any data. So, we have to wait until we get the DB connection with the use of some loop. 
# If there is a internet connection then we can wait and try to get the db connection. If the credentials are wrong, we will never get to connection to db.

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successfull.')
        break   # Once we get the DB connection, come out of the loop.

    except Exception as error:
        print("Connecting to DB failed.")
        print("Error: ", error)
        time.sleep(2)   # Wait for 2 seconds and then try to connect db

'''
Note:
Here, The db credentials are hardcoded. It's not a good method to hardcode the credentials. If the deployment is in cloud, then this will be difficult to main all the credentials
just by hardcoding. So, we have to dynamically take the credentials and get the db connection. We can use Environmental variables to do that.
'''

