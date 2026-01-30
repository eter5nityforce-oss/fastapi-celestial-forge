from app.engine.game import GameEngine
from app.ai import AIPlayer

def test_ai_behavior():
    engine = GameEngine()
    ai = AIPlayer(engine)

    # Create game: p1 (Human), p2 (AI)
    game = engine.create_game("p1", "Human", "ai_bot", "AI Bot")

    # Fast forward to AI turn
    engine.end_turn(game, "p1")

    assert game.get_current_player().player_id == "ai_bot"

    # AI takes turn
    ai.take_turn(game, "ai_bot")

    # Should be Human's turn now
    assert game.get_current_player().player_id == "p1"

    # Check log to see if AI did something
    print(game.action_log)

    # Since it's turn 1 (or 2 actually), AI likely played a card if it had a 1-cost
    # or just ended turn if it had only expensive cards.
    # At least "end_turn" happened.

if __name__ == "__main__":
    test_ai_behavior()
    print("AI tests passed!")
