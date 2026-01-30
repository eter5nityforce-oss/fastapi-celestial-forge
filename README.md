# Celestial Forge: Card Strategy Game

A complex, browser-based, turn-based deck-building strategy game built with FastAPI and WebSockets.

## Features

-   **Game Engine**: A robust Python-based game engine handling Mana, Unit Combat, Spell Effects, and Turn Progression.
-   **Multiplayer**: Real-time state synchronization using WebSockets.
-   **AI Opponent**: Play against an AI that makes tactical decisions.
-   **Deck Building**: (MVP) Pre-constructed decks with diverse card types (Units, Spells).
-   **User System**: Registration, Login, and Persistent User Profiles.
-   **Interactive UI**: Dark-themed, responsive game board built with HTML5/CSS3/JS.

## Technology Stack

-   **Backend**: FastAPI, Uvicorn, SQLAlchemy
-   **Database**: SQLite (Portability focus)
-   **Real-time**: FastAPI WebSockets
-   **Frontend**: Vanilla JS (ES6+), CSS3
-   **Testing**: Pytest, Playwright

## Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Project

1.  Start the server:
    ```bash
    uvicorn app.main:app --reload
    ```
2.  Open your browser and navigate to:
    ```
    http://localhost:8000
    ```

## Demo Instructions

1.  **Register**: Click "Create Account" on the login page. Enter a username (e.g., `hero1`) and password.
2.  **Login**: Use the credentials to log in.
3.  **Lobby**: Click "New Battle vs AI" to start a single-player game.
4.  **Gameplay**:
    -   **Draw Phase**: Cards are drawn automatically at the start of your turn.
    -   **Play Cards**: Click a card in your hand (green border), then click the Board (for Units) or the Enemy (for Spells).
    -   **Combat**: Click your Unit (green border), then click an Enemy Unit or the Enemy Hero to attack.
    -   **End Turn**: Click the "End Turn" button. The AI will take its turn immediately.
    -   **Win**: Reduce the Enemy Hero's HP to 0.

## Project Structure

-   `app/`: Core application code.
    -   `engine/`: Game logic (Rules, State, Cards).
    -   `routers/`: API endpoints (Auth, Game).
    -   `main.py`: Entry point.
-   `static/`: Frontend assets (HTML, CSS, JS).
-   `tests/`: Unit and Integration tests.

## License

MIT
