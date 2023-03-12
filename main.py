from __future__ import annotations

from fastapi import FastAPI

from app.api import heroes_router, teams_router
from app.db.session import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


app.include_router(heroes_router)
app.include_router(teams_router)
