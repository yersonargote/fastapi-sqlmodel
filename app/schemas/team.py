from typing import Optional

from sqlmodel import SQLModel

from app.models.team import TeamBase


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    name: Optional[str] = None
    headquarters: Optional[str] = None
