from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from app.db.session import get_session
from app.models.hero import Hero
from app.models.team import Team
from app.schemas.hero import HeroCreate, HeroRead, HeroReadWithTeam, HeroUpdate

router = APIRouter(
    prefix="/heroes",
    tags=["heroes"],
)


@router.post("/", response_model=HeroRead)
async def create_hero(
    *,
    session: AsyncSession = Depends(get_session),
    hero: HeroCreate,
):
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    await session.commit()
    await session.refresh(db_hero)
    return db_hero


@router.get("/", response_model=List[HeroRead])
async def read_heroes(
    *,
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    result = await session.execute(select(Hero).offset(offset).limit(limit))
    heroes = result.scalars().all()
    return heroes


@router.get("/{hero_id}", response_model=HeroRead)
async def read_heroe(*, session: AsyncSession = Depends(get_session), hero_id: int):
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found.")
    return HeroRead.from_orm(hero)


@router.get("/{hero_id}/with_team", response_model=HeroReadWithTeam)
async def read_hero_with_team(
    *,
    session: AsyncSession = Depends(get_session),
    hero_id: int,
):
    query = (
        select(Hero, Team)
        .join(Team, Hero.team_id == Team.id, isouter=True)
        .where(Hero.id == hero_id)
    )
    result = await session.execute(query)
    hero, team = result.first()

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found.")

    hero_data = hero.__dict__
    team_data = team.__dict__ if team else None

    hero_with_team = HeroReadWithTeam(**hero_data, team=team_data)
    return hero_with_team


@router.patch("/{hero_id}", response_model=HeroRead)
async def update_hero(
    *, session: AsyncSession = Depends(get_session), hero_id: int, hero: HeroUpdate
):
    db_hero = await session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found.")
    hero_data = hero.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    await session.commit()
    await session.refresh(db_hero)
    return db_hero


@router.delete("/{hero_id}", response_model=HeroRead)
async def delete_hero(*, session: AsyncSession = Depends(get_session), hero_id: int):
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found.")
    await session.delete(hero)
    await session.commit()
    return hero
