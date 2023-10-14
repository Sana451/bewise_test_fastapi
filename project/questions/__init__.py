from fastapi import APIRouter

questions_router = APIRouter(
    prefix="/questions",
)

from . import models
