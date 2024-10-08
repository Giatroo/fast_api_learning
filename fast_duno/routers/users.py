from http import HTTPStatus
from typing import Annotated

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException

from fast_duno.database import get_session
from fast_duno.models import User
from fast_duno.schemas import Message, UserList, UserPublic, UserSchema
from fast_duno.security import get_current_user, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])
T_Session = Annotated[sa.orm.Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
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


@router.get("/", status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    session: T_Session,
    limit: int = 10,
    skip: int = 0,
):
    users = session.scalars(sa.select(User).limit(limit).offset(skip))
    return {"users": users}


@router.get("/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user(user_id: int, session: sa.orm.Session = Depends(get_session)):
    db_user = session.scalar(sa.select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )

    return db_user


@router.put("/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
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


@router.delete("/{user_id}", status_code=HTTPStatus.OK, response_model=Message)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough permissions",
        )

    session.delete(current_user)
    session.commit()

    return {"message": "User deleted"}
