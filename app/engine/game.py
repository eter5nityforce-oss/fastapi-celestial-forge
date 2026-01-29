import random
import copy
from typing import List, Optional
from .models import GameState, PlayerState, CardInstance
from .card_defs import get_card_def, CARD_DEFINITIONS

class GameEngine:
    def __init__(self):
        pass

    def create_game(self, player1_id: str, player1_name: str, player2_id: str, player2_name: str) -> GameState:
        p1 = PlayerState(player_id=player1_id, name=player1_name)
        p2 = PlayerState(player_id=player2_id, name=player2_name)

        # Initialize basic decks for MVP
        p1.deck = self._create_starter_deck()
        p2.deck = self._create_starter_deck()

        game = GameState(game_id=f"game_{random.randint(1000,9999)}", players=[p1, p2])
        self.start_game(game)
        return game

    def _create_starter_deck(self) -> List[CardInstance]:
        deck = []
        # Create a simple deck of 20 cards
        keys = list(CARD_DEFINITIONS.keys())
        for _ in range(20):
            card_key = random.choice(keys)
            c_def = get_card_def(card_key)
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
            deck.append(card)
        return deck

    def start_game(self, game: GameState):
        game.status = "ACTIVE"

        # Shuffle decks
        random.shuffle(game.players[0].deck)
        random.shuffle(game.players[1].deck)

        # Draw initial hands (3 cards)
        for _ in range(3):
            self.draw_card(game, 0)
            self.draw_card(game, 1)

        # Start first player's turn
        self.start_turn(game)
        game.action_log.append("Game Started")

    def draw_card(self, game: GameState, player_index: int):
        player = game.players[player_index]
        if len(player.deck) > 0:
            card = player.deck.pop(0)
            if len(player.hand) < 10: # Max hand size
                player.hand.append(card)
                # game.action_log.append(f"{player.name} drew a card.")
            else:
                game.action_log.append(f"{player.name}'s hand is full! Burned {card.name}.")
        else:
            # Fatigue: Deal damage to hero
            damage = 1 # Simplified fatigue
            player.hero.hp -= damage
            game.action_log.append(f"{player.name} takes {damage} fatigue damage!")

    def start_turn(self, game: GameState):
        player = game.get_current_player()

        # Increase Mana Crystals
        if player.mana_crystals < 10:
            player.mana_crystals += 1

        # Refill Mana
        player.mana = player.mana_crystals

        # Draw Card
        self.draw_card(game, game.current_player_index)

        # Wake up units
        for unit in player.board:
            unit.exhausted = False
            unit.can_attack = True

        game.action_log.append(f"Turn {game.turn}: {player.name}'s turn.")

    def end_turn(self, game: GameState, player_id: str):
        if game.get_current_player().player_id != player_id:
            raise ValueError("Not your turn!")

        # Switch player
        game.current_player_index = 1 - game.current_player_index
        if game.current_player_index == 0:
            game.turn += 1

        self.start_turn(game)

    def play_card(self, game: GameState, player_id: str, card_instance_id: str, target_id: Optional[str] = None):
        player = game.get_current_player()
        if player.player_id != player_id:
            raise ValueError("Not your turn!")

        # Find card in hand
        card_index = -1
        card = None
        for i, c in enumerate(player.hand):
            if c.instance_id == card_instance_id:
                card = c
                card_index = i
                break

        if not card:
            raise ValueError("Card not in hand")

        if player.mana < card.cost:
            raise ValueError("Not enough mana")

        # Deduct Mana
        player.mana -= card.cost

        # Remove from hand
        player.hand.pop(card_index)

        game.action_log.append(f"{player.name} played {card.name}")

        if card.card_type == "Unit":
            card.exhausted = True
            card.can_attack = False
            if len(player.board) < 7: # Board limit
                player.board.append(card)
            else:
                game.action_log.append("Board full! Unit destroyed.")
                player.graveyard.append(card)

        elif card.card_type == "Spell":
            self._resolve_spell_effect(game, card, target_id)
            player.graveyard.append(card)

    def _resolve_spell_effect(self, game: GameState, card: CardInstance, target_id: str):
        # Very simple hardcoded effects based on description or id
        # In real engine, use the effect_id
        c_def = get_card_def(card.card_id)
        effect_id = c_def.get("effect_id") if c_def else None

        if effect_id == "dmg_3" or (card.description and "Deal 3 damage" in card.description):
             self._deal_damage(game, target_id, 3)
        elif effect_id == "dmg_2" or (card.description and "Deal 2 damage" in card.description):
             self._deal_damage(game, target_id, 2)

    def attack(self, game: GameState, player_id: str, attacker_id: str, target_id: str):
        player = game.get_current_player()
        opponent = game.get_opponent()

        if player.player_id != player_id:
            raise ValueError("Not your turn")

        attacker = next((u for u in player.board if u.instance_id == attacker_id), None)
        if not attacker:
            raise ValueError("Attacker not found on board")

        if not attacker.can_attack or attacker.exhausted:
            raise ValueError("Unit cannot attack")

        # Identify Target
        target_unit = next((u for u in opponent.board if u.instance_id == target_id), None)
        is_hero_target = (target_id == "opponent_hero") or (target_id == opponent.player_id)

        if not target_unit and not is_hero_target:
             # Might be attacking opponent hero directly if passed ID matches
             if target_id == opponent.player_id:
                 is_hero_target = True
             else:
                 raise ValueError("Invalid target")

        game.action_log.append(f"{attacker.name} attacks!")

        if is_hero_target:
            opponent.hero.hp -= attacker.attack
            game.action_log.append(f"{opponent.name} takes {attacker.attack} damage!")
        else:
            # Unit vs Unit combat
            target_unit.health -= attacker.attack
            attacker.health -= target_unit.attack

            if target_unit.health <= 0:
                opponent.board.remove(target_unit)
                opponent.graveyard.append(target_unit)
                game.action_log.append(f"{target_unit.name} died.")

            if attacker.health <= 0:
                player.board.remove(attacker)
                player.graveyard.append(attacker)
                game.action_log.append(f"{attacker.name} died.")

        attacker.exhausted = True
        attacker.can_attack = False

        self._check_game_over(game)

    def _deal_damage(self, game: GameState, target_id: str, amount: int):
        # Find target in both players boards and heroes
        if not target_id:
            return

        for p in game.players:
            if p.player_id == target_id or target_id == "opponent_hero":
                 # Logic for "opponent_hero": find the player who is NOT current
                 target_p = p
                 if target_id == "opponent_hero":
                     target_p = game.get_opponent()

                 target_p.hero.hp -= amount
                 game.action_log.append(f"{target_p.name} takes {amount} damage.")
                 self._check_game_over(game)
                 return

            for unit in p.board:
                if unit.instance_id == target_id:
                    unit.health -= amount
                    if unit.health <= 0:
                        p.board.remove(unit)
                        p.graveyard.append(unit)
                        game.action_log.append(f"{unit.name} died.")
                    return

    def _check_game_over(self, game: GameState):
        for p in game.players:
            if p.hero.hp <= 0:
                game.status = "FINISHED"
                # The other player wins
                winner = next(pl for pl in game.players if pl != p)
                game.winner = winner.player_id
                game.action_log.append(f"Game Over! {winner.name} wins!")
