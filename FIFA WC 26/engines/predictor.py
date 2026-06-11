import pandas as pd
import joblib


class MatchPredictor:

    def __init__(self):

        # Load trained model
        self.model = joblib.load("models/winner_model.pkl")

        # Load FIFA rankings
        self.rankings = pd.read_csv(
            "data/fifa_ranking_2026-06-08.csv"
        )

    def get_team_info(self, team):

        row = self.rankings[
            self.rankings["team"] == team
        ]

        if row.empty:
            raise ValueError(
                f"Team not found in rankings: {team}"
            )

        return {
            "rank": float(row.iloc[0]["rank"]),
            "points": float(row.iloc[0]["points"]),
            "matches": float(row.iloc[0]["rated_matches"])
        }

    def build_features(
        self,
        home_team,
        away_team
    ):

        home = self.get_team_info(home_team)
        away = self.get_team_info(away_team)

        rank_difference = (
            home["rank"] - away["rank"]
        )

        points_difference = (
            home["points"] - away["points"]
        )

        experience_difference = (
            home["matches"] - away["matches"]
        )

        home_rank_inverse = (
            1 / home["rank"]
        )

        away_rank_inverse = (
            1 / away["rank"]
        )

        modern_era = 1
        round_encoded = 4

        return pd.DataFrame([
            {
                "rank_difference": rank_difference,
                "points_difference": points_difference,
                "experience_difference": experience_difference,
                "home_rank_inverse": home_rank_inverse,
                "away_rank_inverse": away_rank_inverse,
                "home_is_top10": int(home["rank"] <= 10),
                "away_is_top10": int(away["rank"] <= 10),
                "modern_era": modern_era,
                "round_encoded": round_encoded
            }
        ])

    def predict_match(
        self,
        home_team,
        away_team
    ):

        features = self.build_features(
            home_team,
            away_team
        )

        prediction = self.model.predict(
            features
        )[0]

        probabilities = self.model.predict_proba(
            features
        )[0]

        confidence = max(probabilities)

        if prediction == 1:
            winner = home_team

        elif prediction == 0:
            winner = away_team

        else:
            # knockout fallback
            if probabilities[1] >= probabilities[0]:
                winner = home_team
            else:
                winner = away_team

        return {
            "winner": winner,
            "probability": round(
                float(confidence),
                3
            )
        }