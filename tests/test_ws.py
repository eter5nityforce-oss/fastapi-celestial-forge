from fastapi.testclient import TestClient
from app.main import app
from app.managers import game_manager

client = TestClient(app)

def test_websocket_game():
    # 1. Create Game
    # Mock auth by manually creating a game in manager
    game = game_manager.create_game("p1", "Player 1", "ai_bot", "AI")
    game_id = game.game_id

    # 2. Connect WS
    with client.websocket_connect(f"/ws/game/{game_id}") as websocket:
        # 3. Send action (End turn)
        websocket.send_json({
            "player_id": "p1",
            "action": "end_turn",
            "data": {},
            "token": "fake_token"
        })

        # 4. Receive update
        data = websocket.receive_json()
        assert data["type"] == "state_update"
        new_game_state = data["game"]

        # Check that turn changed (or AI played)
        # If AI played, it might have sent another update, or the state reflects it
        # The manager processes the AI turn immediately after user end_turn in the same thread
        # So we should see the result of AI turn.

        # p1 ended turn -> p2 (AI) starts -> p2 plays -> p2 ends -> p1 starts (Turn 2)
        # OR p2 starts and waits?
        # In managers.py:
        # if action == "end_turn": ... if next is AI, self.ai.take_turn
        # AI take_turn calls engine.end_turn at the end.
        # So we should be back to p1, Turn 2.

        assert new_game_state["turn"] >= 2
        assert new_game_state["players"][0]["mana"] == 2

if __name__ == "__main__":
    test_websocket_game()
    print("WS tests passed!")
