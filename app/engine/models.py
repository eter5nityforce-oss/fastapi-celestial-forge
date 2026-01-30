from typing import List, Optional, Dict
from pydantic import BaseModel, Field
import uuid

class CardInstance(BaseModel):
    instance_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    card_id: str # Reference to the card definition
    name: str
    cost: int
    attack: int
    health: int
    max_health: int
    card_type: str # "Unit" or "Spell"
    description: str
    can_attack: bool = False
    exhausted: bool = True # Summoning sickness

class Hero(BaseModel):
    hp: int = 30
    max_hp: int = 30
    armor: int = 0
    name: str = "Hero"

class PlayerState(BaseModel):
    player_id: str
    name: str
    hero: Hero = Field(default_factory=Hero)
    hand: List[CardInstance] = []
    deck: List[CardInstance] = []
    board: List[CardInstance] = [] # Units on field
    graveyard: List[CardInstance] = []
    mana: int = 0
    max_mana: int = 0
    mana_crystals: int = 0 # Permanent mana capacity

class GameState(BaseModel):
    game_id: str
    turn: int = 1
    current_player_index: int = 0
    players: List[PlayerState]
    status: str = "WAITING" # WAITING, ACTIVE, FINISHED
    winner: Optional[str] = None
    action_log: List[str] = []

    def get_current_player(self) -> PlayerState:
        return self.players[self.current_player_index]

    def get_opponent(self) -> PlayerState:
        return self.players[1 - self.current_player_index]
