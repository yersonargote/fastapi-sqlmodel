from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamRead, TeamUpdate

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)


@router.post("/", response_model=TeamRead)
async def create_team(
    *,
    session: AsyncSession = Depends(get_session),
    team: TeamCreate,
):
    db_team = Team.from_orm(team)
    session.add(db_team)
    await session.commit()
    await session.refresh(db_team)
    return db_team


@router.get("/", response_model=List[TeamRead])
async def read_teams(
    *,
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    result = await session.execute(select(Team).offset(offset).limit(limit))
    teams = result.scalars().all()
    return teams


@router.get("/{team_id}", response_model=TeamRead)
async def read_team(*, team_id: int, session: AsyncSession = Depends(get_session)):
    team = await session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/{team_id}", response_model=TeamRead)
async def update_team(
    *,
    session: AsyncSession = Depends(get_session),
    team_id: int,
    team: TeamUpdate,
):
    db_team = await session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    await session.commit()
    await session.refresh(db_team)
    return db_team


@router.delete("/{team_id}", response_model=TeamRead)
async def delete_team(*, session: AsyncSession = Depends(get_session), team_id: int):
    team = await session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    await session.delete(team)
    await session.commit()
    return team
