from datetime import datetime, timedelta
import ldap
import jwt
from datetime import timezone
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.database import redis
from ..settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db = {}


def verify_password(email: str, password: str):
    try:
        conn = ldap.initialize(settings.LDAP_SERVER)
        conn.simple_bind_s(f"cn={email},{settings.BASE_DN}", password)
    except ldap.SERVER_DOWN as e:
        print(f"Error: {e}")
        return False
    except ldap.INVALID_CREDENTIALS as e:
        print(f"Error: {e}")
        return False
    except ldap.LDAPError as e:
        print(f"Error: {e}")
        return False
    return True


def verify_user(email: str):
    pass


def get_access_token(username: str, role: str = None) -> str:
    payload = {
        'sub': username,
        'exp': datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        'iat': datetime.utcnow(),
        'role': role
    }
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM, headers={'alg': settings.ALGORITHM,
                                                                                 'typ': 'JWT_access'}
                      )


def get_refresh_token(username: str) -> str:
    payload = {
        'sub': username,
        'exp': datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        'iat': datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM, headers={'alg': settings.ALGORITHM,
                                                                                 'typ': 'JWT_refresh'}
                      )


def update_tokens(access_token: str, refresh_token: str) -> dict:
    username: str = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM, options={'verify_signature': False})['sub']
    if username.encode('utf-8') in redis.keys() and redis.get(username.encode('utf-8')) == refresh_token.encode('utf-8'):
        access_token = get_access_token(username)
        refresh_token = get_refresh_token(username)
        return {'access_token': access_token, 'refresh_token': refresh_token}


def validate_access_token(token: str) -> bool:
    try:
        jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM],
                   options={'verify_signature': True, 'verify_exp': True})
        return True

    except jwt.ExpiredSignatureError as e:
        return False
        raise HTTPException(status_code=401, detail='Expired token') from e

    except jwt.InvalidSignatureError as e:
        raise HTTPException(status_code=401, detail='Invalid signature') from e
