import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
from loguru import logger

import database as _database
import models as _models
import schemas as _schemas


oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")


JWT_SECRET = "mysecretkey"


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        # should be closed after exiting parent function
        db.close()


async def get_user_by_email(
    email: str,
    db: _orm.Session
):
    return db.query(_models.User).filter(_models.User.email == email)


async def create_user(
    user: _schemas.UserCreate,
    db: _orm.Session
):
    user_obj = _models.User(
        email=user.email,
        hashed_password=_hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    # {email:str, id:int, hashed_password:str}
    return user_obj


async def authentificate_user(
    email: str,
    password: str,
    db: _orm.Session
):

    q = await get_user_by_email(email, db)
    user = q.all()

    if not user:
        return False

    if not user[0].verify_password(password):
        return False

    return user[0]


async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)
    token = _jwt.encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")


async def get_current_user(
        db: _orm.Session = _fastapi.Depends(get_db),
        token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except Exception as e:
        logger.error(e)
        raise _fastapi.HTTPException(
            status_code=401,
            detail="Wrong email or passowrd`"
        )
    else:
        return _schemas.User.from_orm(user)
