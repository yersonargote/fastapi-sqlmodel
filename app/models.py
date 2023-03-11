from __future__ import annotations

from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class HeroTeamLink(SQLModel, table=True):
    team_id: Optional[int] = Field(
        default=None,
        foreign_key="team.id",
        primary_key=True,
    )
    hero_id: Optional[int] = Field(
        default=None,
        foreign_key="hero.id",
        primary_key=True,
    )


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    heroes: List[Hero] = Relationship(
        back_populates="team",
        link_model=HeroTeamLink,
    )


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    headquarters: Optional[str] = None


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    team: Optional[Team] = Relationship(
        back_populates="heroes",
        link_model=HeroTeamLink,
    )


class HeroCreate(HeroBase):
    pass


class HeroRead(HeroBase):
    id: int


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None


class HeroReadWithTeam(HeroRead):
    team: Optional[TeamRead] = None


class TeamReadWithHeroes(TeamRead):
    heroes: List[HeroRead] = []
