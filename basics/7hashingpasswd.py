from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

passwords = ["paddhu", "nooka2434@", "@pojl2383P"]

for password in passwords:
    hashedpwd = pwd_context.hash(password)   # pwd_context().hash() converts each string to hashing
    print(hashedpwd)
    '''
    hashedpwd1 = pwd_context.hash(password)         #every time hash algo gives different hashing, but verifies correctly
    print(hashedpwd1)
    '''
    #print(pwd_context.verify(password, hashedpwd))
    print(pwd_context.verify(password, pwd_context.hash(password)))