from http import HTTPStatus

import sqlalchemy as sa
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from fast_duno.database import get_session
from fast_duno.models import User
from fast_duno.schemas import Message, Token, UserList, UserPublic, UserSchema
from fast_duno.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Hello world!"}


@app.get("/page", status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_page():
    return """This is a page."""


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(
    user: UserSchema,
    session: sa.orm.Session = Depends(get_session),
):
    db_user = session.scalar(
        sa.select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Username already exists",
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email already exists",
            )

    new_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10,
    skip: int = 0,
    session: sa.orm.Session = Depends(get_session),
):
    users = session.scalars(sa.select(User).limit(limit).offset(skip))
    return {"users": users}


@app.get(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user(user_id: int, session: sa.orm.Session = Depends(get_session)):
    db_user = session.scalar(sa.select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )

    return db_user


@app.put(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: sa.orm.Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough permissions",
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(
    user_id: int,
    session: sa.orm.Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough permissions",
        )

    session.delete(current_user)
    session.commit()

    return {"message": "User deleted"}


@app.post("/token", status_code=HTTPStatus.OK, response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: sa.orm.Session = Depends(get_session),
):
    db_user = session.scalar(
        sa.select(User).where(User.email == form_data.username)
    )

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data_payload={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "Bearer"}
