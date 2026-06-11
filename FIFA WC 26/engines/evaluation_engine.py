class EvaluationEngine:
    def __init__(self, multipliers=None):
        self.multipliers = multipliers or {
            "Group Stage": 1,
            "Round of 32": 1,
            "Round of 16": 2,
            "Quarter-final": 4,
            "Semi-final": 8,
            "Final": 16
        }

    # --------------------------
    # SCORE SINGLE MATCH
    # --------------------------
    def score_match(self, prediction, actual, round_name="Group Stage"):
        score = 0
        multiplier = self.multipliers.get(round_name, 1)

        # Winner prediction
        if prediction["winner"] == actual["winner"]:
            score += 40

        # Goal difference
        pred_diff = prediction["home_goals"] - prediction["away_goals"]
        act_diff = actual["home_goals"] - actual["away_goals"]

        if pred_diff == act_diff:
            score += 10

        # Total goals
        if (prediction["home_goals"] + prediction["away_goals"]) == \
           (actual["home_goals"] + actual["away_goals"]):
            score += 10

        # Corners
        if prediction["corners"] == actual["corners"]:
            score += 10
        elif abs(prediction["corners"] - actual["corners"]) <= 2:
            score += 5

        # Yellow cards
        if prediction["yellow_cards"] == actual["yellow_cards"]:
            score += 10
        elif abs(prediction["yellow_cards"] - actual["yellow_cards"]) == 1:
            score += 5

        # Red cards
        if prediction["red_cards"] == actual["red_cards"]:
            score += 5

        return score * multiplier

    # --------------------------
    # SCORE FULL TOURNAMENT
    # --------------------------
    def score_tournament(self, predictions, actuals, rounds):
        total = 0

        for match_id in predictions:
            pred = predictions[match_id]
            act = actuals.get(match_id)

            if not act:
                continue

            round_name = rounds.get(match_id, "Group Stage")

            total += self.score_match(pred, act, round_name)

        return total