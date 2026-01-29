from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    decks = relationship("Deck", back_populates="owner")
    # For simplicity, games are stored as JSON blobs or just ID references in a real system
    # but here we can have a relation

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cost = Column(Integer)
    attack = Column(Integer, default=0)
    health = Column(Integer, default=0)
    card_type = Column(String) # "Unit", "Spell"
    effect_id = Column(String, nullable=True) # ID for effect lookup
    description = Column(String)

class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    cards = Column(JSON) # List of Card IDs

    owner = relationship("User", back_populates="decks")

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("users.id"))
    player2_id = Column(Integer, nullable=True) # Null if AI
    winner_id = Column(Integer, nullable=True)
    state = Column(JSON) # Snapshot of final state
    created_at = Column(String)
