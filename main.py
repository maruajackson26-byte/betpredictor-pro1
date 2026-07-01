from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from datetime import datetime
import os

from database import (
    init_db, save_prediction, save_settled_bet,
    get_today_predictions, get_betting_history, get_performance_stats
)
from ai_model import ai_engine
from api_clients import OddsAPIClient
from scheduler import start_scheduler

app = FastAPI(title="BetPredictor Pro API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    init_db()
    start_scheduler()

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/api/predictions/today")
async def today_predictions():
    predictions = get_today_predictions()
    if not predictions:
        predictions = []
    return {
        "count": len(predictions),
        "predictions": predictions,
        "generated_at": datetime.utcnow().isoformat()
    }

@app.get("/api/history")
async def betting_history(limit: int = 20):
    history = get_betting_history(limit)
    stats = get_performance_stats()
    win_rate = (stats['wins'] / stats['total'] * 100) if stats['total'] > 0 else 0
    return {
        "history": history,
        "stats": {
            "total": stats['total'],
            "wins": stats['wins'],
            "losses": stats['losses'],
            "win_rate": round(win_rate, 1),
            "total_pl": round(stats['total_pl'] or 0, 1)
        }
    }

@app.get("/api/stats")
async def performance_stats():
    stats = get_performance_stats()
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
