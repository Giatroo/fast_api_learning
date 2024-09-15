from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_duno.schemas import Message

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Hello world!"}


@app.get("/page", status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_page():
    return """This is a page."""
