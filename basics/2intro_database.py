'''
What is Database?
    Database is a collection of Organized data that can be easily accessed and managed. Eg: the users registered data and the posts created by user which 
    are stored in Database which sits on the disk.

Data Base Management System(DBMS):
    - We don't work or interact with DataBases directly.
    - Instead we make use of a software referred to as DBMS. (when we want to perform an operation on DataBase, we have to send a request to DBMS and then DBMS performs
      performs operation and sends the results back. We never interact with Database directly, instead the s/w DBMBS sits in the middle and manages.)

Two types of DBMS:
    1. Relational
        - MYSQL
        - POSTGRESQL   (This is used in this course)
        - ORACLE
        - SQL SERVER
    2. NoSQL
        - MongoDB
        - DynamoDB
        - ORACLE
        - SQL SERVER

SQL(Structured Query Language) - Language used to communicate with DBMS.

POSTGRESQL:
    - Each instance of postgres can be carved into multiple seperate databases(eg: Different applications can use different Databases).
    - By default every Postgre installation comes with one database already created called "postgres".(However, we don't use this database usually).
    - This is important because Postgre requires you to specify the name of a database to make a connection. So there needs to always be one database.

Tables:
    A table represents a Subject or Event in an application. Eg: An e-commerce website can have different tables like Users, Products and Purchases. All these Tables will have 
    some sort of Relations, that's why these are Relational Databases. One should understand the relationship so that he can design the DataBase very efficiently.

    - A table is made up of columns and rows. 
    - Each column represents a different attribute. Eg: Id, Name, Age, Sex are the columns
    - Each row represents a different entry in the table. Eg: (1234, Sanjeevi, 25, M), (567, Chandramma, 23, F) are the entries

Postgres DataTypes:
    - Databases have data types just like any programming language.

Primary key:
    - To identify each row/entry in a table, we need a unique key. This unique is called Primary Key. A primary key is a column or group of columns that 
      identifies each row in a table.
    - Table can have one and only one primary key.

Unique Constraints:
    - A unique constraint can be applied to any column to make sure every record has a unique value for that column.

Null Constraints:
    - By default, when adding a new entry to the database, any column can be left blank. When a column is left blank, It has null value.
    - If you need a column to be properly filled into create a new record, a NOT NULL constraint can be added to the column to ensure that the column is never left blank.


Note: pgAdmin4 has been installed for PostgreSQL in windows.

For learning basics "products" table has been created.


SQL Basics:

    Basic sql querires:
        SELECT * FROM products;
        SELECT id, name FROM products;
        SELECT id AS product_id FROM products;
        SELECT id AS product_id, name AS product_name FROM products;

    Filter results with WHERE:
        SELECT * FROM products WHERE price = 200;
        SELECT * FROM products WHERE name = 'Microphone';

    SQL Operators:
        SELECT * FROM products WHERE price = 200 OR price = 50;
        SELECT * FROM products WHERE price = 50 AND name = 'Microphone';    -- Single quotes
        SELECT * FROM products WHERE price > 100;
        SELECT * FROM products WHERE price > 100 AND price <400;
        SELECT * FROM products WHERE price != 100;  -- we can also use <> operator for not equal
        SELECT id, name, inventory FROM products WHERE price = 50 AND name = 'Microphone';

    IN Operator:
        SELECT * FROM products WHERE id=7 OR id=14 or id=5;
        SELECT * FROM products WHERE id IN (7, 14, 5);

        select * FROM products;

    Pattern matching with LIKE:
        SELECT * FROM products WHERE name LIKE 'TV%';   --Names begin with 'TV'
        SELECT * FROM products WHERE name NOT LIKE 'TV%'; 
        SELECT * FROM prodcuts WHERE name LIKE 'No_ka';
        SELECT * FROM prodcuts WHERE name NOT LIKE 'Nook_';
            (% -> To match arbitrary number of characters
             _ -> To match any single character)

    Ordering Results:
        SELECT * FROM products ORDER BY price;  -- displays the results based on the order by column; by default it's in Ascending order
        SELECT * FROM products ORDER BY price ASC;  -- ascending order
        SELECT * FROM products ORDER BY price DESC; -- descending order
        SELECT * FROM products ORDER BY inventory DESC;
        SELECT * FROM products ORDER BY inventory DESC, price;     -- Can order for 2nd parameter when 1st values are tie; by default ASC for price
        SELECT * FROM products ORDER BY inventory DESC, price DESC;    
        SELECT * FROM products WHERE price>=300 ORDER BY create_at DESC;    -- Filtering on Price and Display recently created items

    LIMIT & OFFSET:
        SELECT * FROM products LIMIT 10;		-- Displays only 10 results
        SELECT * FROM products ORDER BY create_at DESC LIMIT 10;
        SELECT * FROM products WHERE price > 99 LIMIT 5;
        
        OFFSET n - It skips the first n rows
        SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 2;		-- Display rows with id increasing order; skips 2 rows; displays next 5 rows with increasing order id
                                                                    This LIMIT and OFFSET are useful when we talk about pagination.
                                                                    
    Modifying data:
        Creating/INserting new data:
            INSERT INTO products (name, price, inventory) VALUES ('tortilla', 4, 1000);		-- Columns and VALUES in respective order.
            INSERT INTO products (name, price, inventory) VALUES ('car', 10000, 100) RETURNING *;	-- This will inserts the car data and displays all the columns of newely entered data.
            INSERT INTO products (name, price, inventory) VALUES ('jeep', 10000, 100), ('Goat', 1000, 100), ('Sheep', 10000, 100) RETURNING id, name, create_at;	-- inserts multiple rows of data at once and returns mentioned columns
        
        Deleting data:
            DELETE FROM products WHERE id = 18;
            DELETE FROM products WHERE id = 18 RETURNING *;		-- Deletes id 18 data and displays deleted data
        
        Updating data:
            UPDATE products SET name = 'flour tortilla', price = 50 WHERE id = 25;
            UPDATE products SET name = 'yellow tortilla', price = 50 WHERE id = 30 RETURNING *;
		
		
    Joins: https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-joins/
        Table1: users(id, email, password, created_at)
        Table2: posts(id, title, content, published, created_at, owner_id)      #owner_id is foreign key for Table1-users(id)
        Table3:

        Left join:
            SELECT * FROM users LEFT JOIN posts ON users.id=posts.owner_id;     # Retrieves all the columns on the condion users.id=posts.owner_id
            
            SELECT title, content, email FROM users LEFT JOIN posts ON users.id=posts.owner_id; # In the entire view, it displays posts.title, posts.content and users.email
            
            SELECT id, content, email FROM users LEFT JOIN posts ON users.id=posts.owner_id; #Error: bcoz; the DB don't know which id has to be consider so its ambiguous. so, we have to mention with table name.
                    SELECT users.id, content, email FROM users LEFT JOIN posts ON users.id=posts.owner_id; 
            
            SELECT posts.*, users.email FROM users LEFT JOIN posts ON users.id=posts.owner_id;

            SELECT users.id, COUNT(*) FROM posts RIGHT JOIN users ON posts.owner_id=users.id group by users.id; # Counts the number of posts by each user. If a specific user(eg: user_id=20) doesn't have any post(s) then still the results will show 1 for that user_id=20. This is becoz COUNT(*) counts everything including null values.
                #To void null values we use the follwoing
                    SELECT users.id, COUNT(posts.id) FROM posts RIGHT JOIN users ON posts.owner_id=users.id group by users.id;
                    SELECT users.id, users.email, COUNT(posts.id) FROM posts RIGHT JOIN users ON posts.owner_id=users.id group by users.id;
            SELECT posts.*, COUNT(votes.post_id) FROM posts LEFT JOIN votes ON posts.id=votes.post_id group by posts.id;    #number of votes for each post
            SELECT posts.*, COUNT(votes.post_id) FROM posts LEFT JOIN votes ON posts.id=votes.post_id where posts.id=8 group by posts.id;   # number of vote for specific post
            

'''



