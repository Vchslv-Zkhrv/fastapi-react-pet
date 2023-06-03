import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _database
import models as _models
import schemas as _shemas


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
    user: _shemas.UserCreate,
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
