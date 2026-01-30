from pydantic import BaseModel
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class CardBase(BaseModel):
    name: str
    cost: int
    attack: int
    health: int
    card_type: str
    description: str

class Card(CardBase):
    id: int
    class Config:
        from_attributes = True

class DeckBase(BaseModel):
    name: str
    cards: List[int]

class Deck(DeckBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True
