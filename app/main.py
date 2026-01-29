from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from .database import engine, Base
from .routers import auth, game

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Celestial Forge")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(game.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Celestial Forge</title>
            <style>
                body { font-family: sans-serif; text-align: center; margin-top: 50px; background: #1a1a1a; color: #fff; }
                a { color: #4CAF50; text-decoration: none; font-size: 20px; border: 1px solid #4CAF50; padding: 10px 20px; border-radius: 5px; }
                a:hover { background: #4CAF50; color: white; }
            </style>
        </head>
        <body>
            <h1>Celestial Forge API</h1>
            <p>Welcome to the card strategy game backend.</p>
            <br>
            <a href='/static/index.html'>Enter Game Portal</a>
        </body>
    </html>
    """
