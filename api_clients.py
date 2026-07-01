import requests
import os

ODDS_API_KEY = os.getenv("ODDS_API_KEY", "demo_key")

class OddsAPIClient:
    BASE_URL = "https://api.the-odds-api.com/v4/sports"
    
    @staticmethod
    def get_upcoming_matches(sport="soccer_epl", regions="eu", markets="h2h"):
        url = f"{OddsAPIClient.BASE_URL}/{sport}/odds"
        params = {
            "apiKey": ODDS_API_KEY,
            "regions": regions,
            "markets": markets,
            "oddsFormat": "decimal"
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Odds API Error: {e}")
            return []
    
    @staticmethod
    def get_completed_matches(sport="soccer_epl", days_ago=7):
        url = f"{OddsAPIClient.BASE_URL}/{sport}/scores"
        params = {
            "apiKey": ODDS_API_KEY,
            "daysFrom": days_ago
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Scores API Error: {e}")
            return []
