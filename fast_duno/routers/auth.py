from http import HTTPStatus
from typing import Annotated

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fast_duno.database import get_session
from fast_duno.models import User
from fast_duno.schemas import Token
from fast_duno.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])
T_Session = Annotated[sa.orm.Session, Depends(get_session)]
T_OAuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token", status_code=HTTPStatus.OK, response_model=Token)
def login_for_access_token(session: T_Session, form_data: T_OAuthForm):
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
