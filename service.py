from sqlmodel import Session, select
from models import Hero
from typing import List, Optional

class HeroesService:
    def __init__(self, session: Session):
        self.session = session

    def get_heroes_by_magic_points(self, magic_points: int) -> List[Hero]:
        statement = select(Hero).where(Hero.magic_points == magic_points)
        results = self.session.exec(statement)
        return results.all()

    def add_hero(self, hero: Hero) -> Hero:
        self.session.add(hero)
        self.session.commit()
        self.session.refresh(hero)
        return hero

    def edit_hero(self, hero_id: int, hero_data: Hero) -> Optional[Hero]:
        hero_db = self.session.get(Hero, hero_id)
        if not hero_db:
            return None
        
        # Update fields
        hero_db.name = hero_data.name
        hero_db.magic_points = hero_data.magic_points
        hero_db.killed_monsters = hero_data.killed_monsters
        
        self.session.add(hero_db)
        self.session.commit()
        self.session.refresh(hero_db)
        return hero_db

    def delete_hero(self, hero_id: int) -> bool:
        hero_db = self.session.get(Hero, hero_id)
        if not hero_db:
            return False
        
        self.session.delete(hero_db)
        self.session.commit()
        return True