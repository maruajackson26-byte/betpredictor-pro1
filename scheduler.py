from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()

def refresh_predictions_job():
    print(f"[{datetime.utcnow()}] Running prediction refresh...")

def settle_bets_job():
    print(f"[{datetime.utcnow()}] Running bet settlement...")

def start_scheduler():
    scheduler.add_job(refresh_predictions_job, 'interval', hours=2, id='refresh')
    scheduler.add_job(settle_bets_job, 'interval', hours=1, id='settle')
    scheduler.start()
    print("✅ Background scheduler started")
