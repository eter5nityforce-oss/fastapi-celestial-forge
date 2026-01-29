from app.engine.game import GameEngine

def test_core_loop():
    engine = GameEngine()
    game = engine.create_game("p1", "Player 1", "p2", "Player 2")

    # Check initial state
    p1 = game.players[0]
    p2 = game.players[1]

    # Initial draw is 3, plus 1 for start_turn = 4
    assert len(p1.hand) == 4
    assert len(p2.hand) == 3 # Player 2 hasn't started turn yet

    assert p1.mana == 1
    assert p1.mana_crystals == 1

    # End turn p1
    engine.end_turn(game, "p1")

    assert game.current_player_index == 1
    assert p2.mana == 1
    assert len(p2.hand) == 4

    # End turn p2
    engine.end_turn(game, "p2")

    # Back to p1, Turn 2
    assert game.turn == 2
    assert game.current_player_index == 0
    assert p1.mana == 2
    assert p1.mana_crystals == 2
    assert len(p1.hand) == 5

if __name__ == "__main__":
    test_core_loop()
    print("Engine Core tests passed!")
