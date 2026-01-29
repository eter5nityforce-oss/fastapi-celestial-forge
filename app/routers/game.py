from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth
from ..managers import game_manager
from ..websockets import manager
import uuid

router = APIRouter(tags=["game"])

@router.post("/game/create", response_model=dict)
def create_game(current_user: models.User = Depends(auth.get_current_user)):
    # Create a game against AI for now (or generic matchmaking later)
    # For MVP: User vs AI
    game = game_manager.create_game(
        player1_id=current_user.username,
        player1_name=current_user.username,
        player2_id="ai_bot",
        player2_name="AI Opponent",
        vs_ai=True
    )
    return {"game_id": game.game_id}

@router.get("/game/{game_id}")
def get_game_state(game_id: str, current_user: models.User = Depends(auth.get_current_user)):
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    # In a real app, we should filter private info (opponent hand)
    return game.dict()

@router.websocket("/ws/game/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    # Note: Authentication in WS is tricky. Often pass token in query param.
    # keeping it simple: anyone with ID can join.
    await manager.connect(game_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Expecting {"token": "...", "action": "...", "data": ...}
            # Verify token
            token = data.get("token")
            # We need to decode token manually here or pass it in connection
            # Skipping WS auth for MVP simplicity, trusting client sends valid player_id

            player_id = data.get("player_id")
            action = data.get("action")
            action_data = data.get("data", {})

            try:
                updated_game = game_manager.process_action(game_id, player_id, action, action_data)
                # Broadcast new state
                await manager.broadcast(game_id, {"type": "state_update", "game": updated_game.dict()})
            except ValueError as e:
                await websocket.send_json({"type": "error", "message": str(e)})
            except Exception as e:
                 await websocket.send_json({"type": "error", "message": "Internal error"})
                 print(f"WS Error: {e}")

    except WebSocketDisconnect:
        manager.disconnect(game_id, websocket)
