from app.engine.models import GameState, PlayerState, CardInstance
from app.engine.card_defs import get_card_def

def test_game_state_init():
    p1 = PlayerState(player_id="p1", name="Player 1")
    p2 = PlayerState(player_id="p2", name="Player 2")

    game = GameState(game_id="g1", players=[p1, p2])

    assert game.turn == 1
    assert game.status == "WAITING"
    assert game.get_current_player().player_id == "p1"
    assert game.get_opponent().player_id == "p2"
    assert game.players[0].hero.hp == 30

def test_card_instance():
    c_def = get_card_def("c1")
    card = CardInstance(
        card_id=c_def["id"],
        name=c_def["name"],
        cost=c_def["cost"],
        attack=c_def["attack"],
        health=c_def["health"],
        max_health=c_def["health"],
        card_type=c_def["card_type"],
        description=c_def["description"]
    )

    assert card.name == "Iron Apprentice"
    assert card.health == 2
    assert card.exhausted is True

if __name__ == "__main__":
    test_game_state_init()
    test_card_instance()
    print("Engine Model tests passed!")
