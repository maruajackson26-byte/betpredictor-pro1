import sqlite3
from datetime import datetime
from contextlib import contextmanager

DB_PATH = "betpredictor.db"

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id TEXT UNIQUE,
                home_team TEXT,
                away_team TEXT,
                league TEXT,
                match_time TEXT,
                prediction TEXT,
                odds REAL,
                confidence REAL,
                status TEXT DEFAULT 'pending',
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS betting_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id TEXT,
                match_name TEXT,
                league TEXT,
                prediction TEXT,
                odds REAL,
                stake REAL DEFAULT 100.0,
                result TEXT,
                profit_loss REAL,
                settled_at TEXT
            )
        """)
        conn.commit()

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def save_prediction(pred):
    with get_db() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO predictions 
            (match_id, home_team, away_team, league, match_time, prediction, odds, confidence, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pred['match_id'], pred['home_team'], pred['away_team'],
            pred['league'], pred['match_time'], pred['prediction'],
            pred['odds'], pred['confidence'], 'pending',
            datetime.utcnow().isoformat()
        ))
        conn.commit()

def save_settled_bet(bet):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO betting_history 
            (match_id, match_name, league, prediction, odds, stake, result, profit_loss, settled_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            bet['match_id'], bet['match_name'], bet['league'],
            bet['prediction'], bet['odds'], bet['stake'],
            bet['result'], bet['profit_loss'], datetime.utcnow().isoformat()
        ))
        conn.commit()

def get_today_predictions():
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        today = datetime.utcnow().strftime('%Y-%m-%d')
        rows = conn.execute("""
            SELECT * FROM predictions 
            WHERE DATE(match_time) = ? AND status = 'pending'
            ORDER BY confidence DESC LIMIT 10
        """, (today,)).fetchall()
        return [dict(r) for r in rows]

def get_betting_history(limit=20):
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT * FROM betting_history 
            ORDER BY settled_at DESC LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]

def get_performance_stats():
    with get_db() as conn:
        stats = conn.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN result = 'WIN' THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN result = 'LOSS' THEN 1 ELSE 0 END) as losses,
                SUM(profit_loss) as total_pl
            FROM betting_history
        """).fetchone()
        return dict(stats) if stats else {'total': 0, 'wins': 0, 'losses': 0, 'total_pl': 0}
