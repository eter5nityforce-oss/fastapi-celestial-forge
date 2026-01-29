import random
import time
from app.engine.game import GameEngine
from app.engine.models import GameState

class AIPlayer:
    def __init__(self, engine: GameEngine):
        self.engine = engine

    def take_turn(self, game: GameState, ai_player_id: str):
        # Allow multiple actions per turn
        while True:
            action_taken = False

            player = game.get_current_player()
            opponent = game.get_opponent()

            if player.player_id != ai_player_id:
                break # Not my turn

            # 1. Try to play cards (Prioritize spending mana efficiently)
            # Sort cards by cost descending
            playable_cards = [c for c in player.hand if c.cost <= player.mana]
            playable_cards.sort(key=lambda x: x.cost, reverse=True)

            if playable_cards:
                card = playable_cards[0]
                target_id = None

                if card.card_type == "Spell":
                    # Simple spell targeting: Always face if damage
                    target_id = opponent.player_id

                try:
                    self.engine.play_card(game, ai_player_id, card.instance_id, target_id)
                    action_taken = True
                    continue # Loop again to see if we can do more
                except ValueError as e:
                    print(f"AI Failed to play card: {e}")

            # 2. Try to attack
            ready_units = [u for u in player.board if u.can_attack and not u.exhausted]
            if ready_units:
                attacker = ready_units[0]
                # Decide target:
                # If opponent has taunt (not impl), attack taunt.
                # Else if we have lethal, face.
                # Else trade or face.

                target_id = opponent.player_id # Default face

                # Simple trade logic: if opponent has a unit with attack > 0, attack it
                # (Very dumb AI, but functional)
                valid_targets = [u for u in opponent.board]
                if valid_targets:
                    # Pick random unit to attack
                    target_id = random.choice(valid_targets).instance_id

                try:
                    self.engine.attack(game, ai_player_id, attacker.instance_id, target_id)
                    action_taken = True
                    continue
                except ValueError as e:
                     print(f"AI Failed to attack: {e}")

            if not action_taken:
                break

        # End Turn
        self.engine.end_turn(game, ai_player_id)
