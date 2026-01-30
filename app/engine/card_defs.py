from typing import Dict

CARD_DEFINITIONS = {
    "c1": {
        "id": "c1",
        "name": "Iron Apprentice",
        "cost": 1,
        "attack": 1,
        "health": 2,
        "card_type": "Unit",
        "description": "A eager student of the forge."
    },
    "c2": {
        "id": "c2",
        "name": "Forge Guardian",
        "cost": 3,
        "attack": 3,
        "health": 4,
        "card_type": "Unit",
        "description": "Protector of the sacred flames."
    },
    "c3": {
        "id": "c3",
        "name": "Spirit Fire",
        "cost": 2,
        "attack": 0,
        "health": 0,
        "card_type": "Spell",
        "description": "Deal 3 damage to any target.",
        "effect_id": "dmg_3"
    },
    "c4": {
        "id": "c4",
        "name": "Molten Giant",
        "cost": 8,
        "attack": 8,
        "health": 8,
        "card_type": "Unit",
        "description": "A massive golem of lava."
    },
    "c5": {
        "id": "c5",
        "name": "Hammer Strike",
        "cost": 1,
        "attack": 0,
        "health": 0,
        "card_type": "Spell",
        "description": "Deal 2 damage.",
        "effect_id": "dmg_2"
    }
}

def get_card_def(card_id: str):
    return CARD_DEFINITIONS.get(card_id)
