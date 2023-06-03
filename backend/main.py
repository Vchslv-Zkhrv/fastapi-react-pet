from loguru import logger
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm

import services as _services
import schemas as _schemas


app = _fastapi.FastAPI()


@app.post("/api/users")
async def create_user(
    # pydantic is awesome!
    user: _schemas.UserCreate,
    # session should be closed after executing def
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):

    # SELECT * FROM users WHERE email == user.email
    db_user = await _services.get_user_by_email(user.email, db)
    # if EMPTY SET
    if db_user.all():
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

    return await _services.create_user(user, db)


@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    user = await _services.authentificate_user(
        email=form_data.username,
        password=form_data.password,
        db=db
    )

    if not user:
        raise _fastapi.HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return await _services.create_token(user)


@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(
    user: _schemas.User = _fastapi.Depends(_services.get_current_user)
):
    return user
