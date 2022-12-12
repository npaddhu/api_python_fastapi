from pydantic import BaseSettings

#Validation of Env variables
class Settings(BaseSettings):
    database_hostname: str
    database_port: str          # this is string as this goes into DB URL otherwise we need to convert into string and add
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()

