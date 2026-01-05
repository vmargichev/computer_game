from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from database import get_session
from models import Hero
from service import HeroesService
from typing import List

heroes_controller = APIRouter(prefix="/heroes", tags=["Heroes"])

def get_service(session: Session = Depends(get_session)):
    return HeroesService(session)

@heroes_controller.get("/", response_model=List[Hero])
def getAllHeroesByMagicPoints(
    magic_points: int, 
    service: HeroesService = Depends(get_service)
):
    return service.get_heroes_by_magic_points(magic_points)

@heroes_controller.post("/", response_model=Hero, status_code=201)
def addHero(hero: Hero, service: HeroesService = Depends(get_service)):
    return service.add_hero(hero)

@heroes_controller.put("/{heroID}", response_model=Hero)
def editHero(
    heroID: int, 
    hero: Hero, 
    service: HeroesService = Depends(get_service)
):
    updated_hero = service.edit_hero(heroID, hero)
    if not updated_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return updated_hero

@heroes_controller.delete("/", status_code=204)
def deleteHero(
    heroID: int = Query(..., description="ID of hero to delete"), 
    service: HeroesService = Depends(get_service)
):
    success = service.delete_hero(heroID)
    if not success:
        raise HTTPException(status_code=404, detail="Hero not found")
    return