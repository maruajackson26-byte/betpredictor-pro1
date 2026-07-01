import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import os

MODEL_PATH = "ai_model_v1.pkl"

class BetPredictorAI:
    def __init__(self):
        self.model = self._load_or_train_model()
    
    def _load_or_train_model(self):
        if os.path.exists(MODEL_PATH):
            return joblib.load(MODEL_PATH)
        return self._train_initial_model()
    
    def _train_initial_model(self):
        np.random.seed(42)
        n_samples = 1000
        X = np.random.rand(n_samples, 6)
        X[:, 0] = np.random.uniform(1.2, 5.0, n_samples)
        X[:, 1] = np.random.uniform(1.2, 8.0, n_samples)
        X[:, 2] = np.random.uniform(2.0, 6.0, n_samples)
        X[:, 3] = np.random.uniform(0, 1, n_samples)
        X[:, 4] = np.random.uniform(0, 1, n_samples)
        X[:, 5] = np.random.uniform(0, 10, n_samples)
        implied_prob = 1 / X[:, 0]
        true_prob = X[:, 3] * 0.6 + (1 - X[:, 4]) * 0.3 + X[:, 5] * 0.01
        y = (true_prob > implied_prob + 0.05).astype(int)
        model = GradientBoostingClassifier(n_estimators=100, max_depth=4)
        model.fit(X, y)
        joblib.dump(model, MODEL_PATH)
        return model
    
    def predict_match(self, match_data):
        features = np.array([[
            match_data.get('home_odds', 2.0),
            match_data.get('away_odds', 2.5),
            match_data.get('draw_odds', 3.2),
            match_data.get('home_form', 0.5),
            match_data.get('away_form', 0.5),
            match_data.get('h2h', 5.0)
        ]])
        prob = self.model.predict_proba(features)[0][1]
        confidence = round(prob * 100, 1)
        home_odds = match_data.get('home_odds', 2.0)
        away_odds = match_data.get('away_odds', 2.5)
        if home_odds < away_odds:
            prediction = f"{match_data['home_team']} Win"
            best_odds = home_odds
        else:
            prediction = f"{match_data['away_team']} Win"
            best_odds = away_odds
        return {
            'prediction': prediction,
            'odds': round(best_odds, 2),
            'confidence': confidence
        }

ai_engine = BetPredictorAI()
