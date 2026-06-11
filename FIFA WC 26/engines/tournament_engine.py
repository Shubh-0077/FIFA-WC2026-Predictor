from engines.slot_resolver import SlotResolver
from engines.tournament_simulator import TournamentSimulator
from utils.data_loader import load_knockout_data


class TournamentEngine:

    def __init__(self, group_state):

        self.group_state = group_state

        self.bracket = load_knockout_data()

        self.resolver = SlotResolver()

        self.simulator = TournamentSimulator()

    # ----------------------------------
    # BUILD ROUND
    # ----------------------------------
    def build_round(
        self,
        round_name,
        previous_results=None
    ):

        matches = []

        for match_id, match_data in self.bracket.items():

            if match_data["round"] != round_name:
                continue

            team_a = self.resolver.resolve(
                match_data["home_slot"],
                self.group_state,
                previous_results
            )

            team_b = self.resolver.resolve(
                match_data["away_slot"],
                self.group_state,
                previous_results
            )

            if team_a and team_b:

                matches.append(
                    {
                        "match_id": match_id,
                        "teamA": team_a,
                        "teamB": team_b
                    }
                )

        return matches

    # ----------------------------------
    # PLAY ROUND
    # ----------------------------------
    def play_round(self, matches):

        results = {}

        round_predictions = []

        for match in matches:

            prediction = (
                self.simulator.simulate_match(
                    match["teamA"],
                    match["teamB"]
                )
            )

            results[
                match["match_id"]
            ] = prediction["winner"]

            round_predictions.append(
                {
                    "match_id": match["match_id"],
                    "teamA": match["teamA"],
                    "teamB": match["teamB"],
                    "winner": prediction["winner"],
                    "probability": prediction["probability"]
                }
            )

        return results, round_predictions

    # ----------------------------------
    # FULL TOURNAMENT
    # ----------------------------------
    def simulate_tournament(self):

        tournament = {}

        # Round of 32

        r32_matches = self.build_round(
            "Round of 32"
        )

        r32_results, r32_predictions = (
            self.play_round(
                r32_matches
            )
        )

        tournament["r32"] = (
            r32_predictions
        )

        # Round of 16

        r16_matches = self.build_round(
            "Round of 16",
            r32_results
        )

        r16_results, r16_predictions = (
            self.play_round(
                r16_matches
            )
        )

        tournament["r16"] = (
            r16_predictions
        )

        # Quarter Finals

        qf_matches = self.build_round(
            "Quarter-final",
            r16_results
        )

        qf_results, qf_predictions = (
            self.play_round(
                qf_matches
            )
        )

        tournament["qf"] = (
            qf_predictions
        )

        # Semi Finals

        sf_matches = self.build_round(
            "Semi-final",
            qf_results
        )

        sf_results, sf_predictions = (
            self.play_round(
                sf_matches
            )
        )

        tournament["sf"] = (
            sf_predictions
        )

        # Final

        final_matches = self.build_round(
            "Final",
            sf_results
        )

        final_results, final_predictions = (
            self.play_round(
                final_matches
            )
        )

        tournament["final"] = (
            final_predictions
        )

        if final_predictions:

            tournament["champion"] = (
                final_predictions[0]["winner"]
            )

        else:

            tournament["champion"] = None

        return tournament