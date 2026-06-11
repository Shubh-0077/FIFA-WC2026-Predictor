from engines.predictor import MatchPredictor


class TournamentSimulator:

    def __init__(self):
        self.predictor = MatchPredictor()

    def simulate_match(self, team_a, team_b):

        result = self.predictor.predict_match(
            team_a,
            team_b
        )

        return {
            "teamA": team_a,
            "teamB": team_b,
            "winner": result["winner"],
            "probability": result["probability"]
        }

    def simulate_round(self, matches):

        results = []

        for match in matches:

            team_a = match["teamA"]
            team_b = match["teamB"]

            if not team_a or not team_b:
                continue

            result = self.simulate_match(
                team_a,
                team_b
            )

            result["match_id"] = match["match_id"]

            results.append(result)

        return results