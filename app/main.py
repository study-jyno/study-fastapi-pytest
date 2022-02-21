from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import manage

from app.auth.service import jwt_auth_init
from app.api import api_router
from app.config import ROOT_PATH

app = FastAPI(
    title="Study FastAPI Pytest",
    description="",
    version="0.0.1",
)

origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generate Refresh Token Setting
jwt_auth_init()

manage.create_all()

# Static Test
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

templates = Jinja2Templates(directory=ROOT_PATH + '/static')


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.mount("/", StaticFiles(directory="static"), name="static")

# app.include_router(auth.router)
app.include_router(api_router)

# # Test 중엔 실행되지 않음
# @app.on_event("startup")
# async def startup_event():
#     start_scheduler()
