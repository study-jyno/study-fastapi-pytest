from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database.core import get_db
from app.log.service import service_log

from app.routers.util import get_summary_location

router = APIRouter(
    prefix='/item',
    tags=['Item']
)
