from app.engine.game import GameEngine
from app.engine.models import CardInstance

def test_combat():
    engine = GameEngine()
    game = engine.create_game("p1", "Player 1", "p2", "Player 2")
    p1 = game.players[0]
    p2 = game.players[1]

    # Setup state manually for test
    p1.mana = 10

    # Create a Unit Card for P1
    u1 = CardInstance(instance_id="u1", card_id="c1", name="Unit 1", cost=1, attack=2, health=2, max_health=2, card_type="Unit", description="")
    p1.hand.append(u1)

    # Play the unit
    engine.play_card(game, "p1", "u1")
    assert len(p1.board) == 1
    assert p1.board[0].exhausted == True

    # Skip turns to wake it up
    engine.end_turn(game, "p1")
    engine.end_turn(game, "p2")

    assert p1.board[0].exhausted == False

    # Attack Hero
    engine.attack(game, "p1", "u1", "p2") # Attack p2 hero
    assert p2.hero.hp == 28 # 30 - 2
    assert p1.board[0].exhausted == True

def test_spell():
    engine = GameEngine()
    game = engine.create_game("p1", "Player 1", "p2", "Player 2")
    p1 = game.players[0]
    p2 = game.players[1]

    p1.mana = 10
    # Spell: Deal 3 damage
    s1 = CardInstance(instance_id="s1", card_id="c3", name="Fire", cost=2, attack=0, health=0, max_health=0, card_type="Spell", description="Deal 3 damage", effect_id="dmg_3")
    p1.hand.append(s1)

    engine.play_card(game, "p1", "s1", "p2")
    assert p2.hero.hp == 27 # 30 - 3
    assert len(p1.graveyard) == 1

if __name__ == "__main__":
    test_combat()
    test_spell()
    print("Combat tests passed!")
