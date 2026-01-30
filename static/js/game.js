const urlParams = new URLSearchParams(window.location.search);
const gameId = urlParams.get('game_id');
const username = localStorage.getItem("username");
const token = localStorage.getItem("token");

if (!gameId || !username) {
    window.location.href = "/static/index.html";
}

let ws = new WebSocket(`ws://${window.location.host}/ws/game/${gameId}`);
let gameState = null;

let selectedHandCardId = null;
let selectedBoardUnitId = null;

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === "state_update") {
        gameState = msg.game;
        render();
    } else if (msg.type === "error") {
        alert(msg.message);
        // Reset selections on error
        selectedHandCardId = null;
        selectedBoardUnitId = null;
        render();
    }
};

ws.onopen = () => {
    console.log("Connected to game");
    // Optionally fetch initial state if not pushed immediately
    // For now we rely on an action or the server broadcasting on connect (not impl yet)
    // Let's trigger a fetch via API just in case or wait for an update.
    // Ideally backend sends state on connect.
    // For now, let's just make a dummy call or refresh.
    fetchState();
};

async function fetchState() {
    const res = await fetch(`/game/${gameId}`, {
        headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await res.json();
    gameState = data;
    render();
}

function sendAction(action, data) {
    ws.send(JSON.stringify({
        token: token,
        player_id: username,
        action: action,
        data: data
    }));
    // Clear selections
    selectedHandCardId = null;
    selectedBoardUnitId = null;
    render();
}

function endTurn() {
    sendAction("end_turn", {});
}

function handleHandCardClick(e, card) {
    e.stopPropagation();
    if (gameState.current_player_index !== getMyPlayerIndex()) return;

    if (selectedHandCardId === card.instance_id) {
        selectedHandCardId = null; // Deselect
    } else {
        selectedHandCardId = card.instance_id;
        selectedBoardUnitId = null;
    }
    render();
}

function handleMyUnitClick(e, unit) {
    e.stopPropagation();
    if (gameState.current_player_index !== getMyPlayerIndex()) return;

    // Check if we are selecting a target for a spell?
    // For now, assume we can't target own units with spells in this MVP.

    if (selectedBoardUnitId === unit.instance_id) {
        selectedBoardUnitId = null;
    } else {
        selectedBoardUnitId = unit.instance_id;
        selectedHandCardId = null;
    }
    render();
}

function handleTarget(targetType, targetId) {
    // targetType: 'board', 'opponent_hero', 'opponent_unit'
    if (gameState.current_player_index !== getMyPlayerIndex()) return;

    if (selectedHandCardId) {
        // Playing a card
        const card = getMyPlayer().hand.find(c => c.instance_id === selectedHandCardId);
        if (card.card_type === "Unit" && targetType === 'board') {
             sendAction("play_card", { card_id: selectedHandCardId });
        } else if (card.card_type === "Spell") {
             // Spells usually target units or heroes
             let actualTarget = targetId;
             if (targetType === 'opponent_hero') actualTarget = 'opponent_hero';

             // If spell targets board (AOE) or doesn't need target, targetId might be null
             // MVP Spells are target based
             sendAction("play_card", { card_id: selectedHandCardId, target_id: actualTarget });
        }
    } else if (selectedBoardUnitId) {
        // Attacking
        if (targetType === 'opponent_hero' || targetType === 'opponent_unit') {
            let actualTarget = targetId;
             if (targetType === 'opponent_hero') actualTarget = 'opponent_hero';
            sendAction("attack", { attacker_id: selectedBoardUnitId, target_id: actualTarget });
        }
    }
}

function getMyPlayerIndex() {
    return gameState.players[0].player_id === username ? 0 : 1;
}

function getMyPlayer() {
    return gameState.players[getMyPlayerIndex()];
}

function getOpponent() {
    return gameState.players[1 - getMyPlayerIndex()];
}

function render() {
    if (!gameState) return;

    const myIdx = getMyPlayerIndex();
    const oppIdx = 1 - myIdx;
    const me = gameState.players[myIdx];
    const opp = gameState.players[oppIdx];
    const isMyTurn = gameState.current_player_index === myIdx;

    document.getElementById("turn-text").innerText = `Turn ${gameState.turn} - ${isMyTurn ? "Your Turn" : "Opponent Turn"}`;
    document.getElementById("status-msg").innerText = gameState.status === "FINISHED" ? `Winner: ${gameState.winner}` : "";
    document.getElementById("end-turn-btn").disabled = !isMyTurn;

    // Me
    document.getElementById("my-name").innerText = me.name;
    document.getElementById("my-hp").innerText = me.hero.hp;
    document.getElementById("my-mana").innerText = me.mana;
    document.getElementById("my-max-mana").innerText = me.mana_crystals;

    // Opponent
    document.getElementById("opp-name").innerText = opp.name;
    document.getElementById("opp-hp").innerText = opp.hero.hp;
    document.getElementById("opp-mana").innerText = opp.mana;

    // Render Hand
    const handDiv = document.getElementById("player-hand");
    handDiv.innerHTML = "";
    me.hand.forEach(card => {
        const c = createCardEl(card);
        c.onclick = (e) => handleHandCardClick(e, card);
        if (selectedHandCardId === card.instance_id) c.classList.add("selected");
        handDiv.appendChild(c);
    });

    // Render Opponent Hand (Backs)
    const oppHandDiv = document.getElementById("opponent-hand");
    oppHandDiv.innerHTML = "";
    opp.hand.forEach(() => {
        const c = document.createElement("div");
        c.className = "card";
        c.style.background = "#444"; // Card back
        oppHandDiv.appendChild(c);
    });

    // Render My Board
    const myBoardDiv = document.getElementById("player-board");
    myBoardDiv.innerHTML = "";
    // Click on board background to play unit
    myBoardDiv.onclick = () => handleTarget('board', null);

    me.board.forEach(unit => {
        const c = createCardEl(unit);
        if (unit.exhausted) c.classList.add("exhausted");
        c.onclick = (e) => handleMyUnitClick(e, unit);
        if (selectedBoardUnitId === unit.instance_id) c.classList.add("selected");
        myBoardDiv.appendChild(c);
    });

    // Render Opponent Board
    const oppBoardDiv = document.getElementById("opponent-board");
    oppBoardDiv.innerHTML = "";
    opp.board.forEach(unit => {
        const c = createCardEl(unit);
        c.onclick = (e) => {
            e.stopPropagation();
            handleTarget('opponent_unit', unit.instance_id);
        };
        c.classList.add("target-mode"); // Always a potential target
        oppBoardDiv.appendChild(c);
    });

    // Logs
    const logDiv = document.getElementById("action-log");
    logDiv.innerHTML = gameState.action_log.map(l => `<div>${l}</div>`).join("");
    logDiv.scrollTop = logDiv.scrollHeight;
}

function createCardEl(card) {
    const el = document.createElement("div");
    el.className = "card";
    el.innerHTML = `
        <div class="card-cost">${card.cost}</div>
        <div style="text-align: center; font-weight: bold; margin-top: 10px;">${card.name}</div>
        <div style="font-size: 9px; text-align: center;">${card.description || ""}</div>
        ${card.card_type === "Unit" ?
            `<div class="card-stats">
                <span class="card-atk">${card.attack}</span>
                <span class="card-hp">${card.health}</span>
             </div>` :
            `<div style="text-align: center; margin-top: auto;">SPELL</div>`
        }
    `;
    return el;
}
