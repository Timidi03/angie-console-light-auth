import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    ALGORITHM = os.getenv('ALGORITHM')
    SECRET_KEY = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS'))

    LDAP_SERVER = os.getenv('LDAP_SERVER')
    BASE_DN = os.getenv('BASE_DN')
    GROUP_DN = os.getenv('GROUP_DN')

    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')

    SERVER_HOST = os.getenv('SERVER_HOST')
    SERVER_PORT = os.getenv('SERVER_PORT')
    ORIGINS = os.getenv('ORIGINS')


settings = Settings()

