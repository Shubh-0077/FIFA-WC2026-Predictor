import pandas as pd


class QualificationEngine:

    def __init__(self):

        self.rankings = pd.read_csv(
            "data/fifa_ranking_2026-06-08.csv"
        )

    def get_team_points(self, team):

        row = self.rankings[
            self.rankings["team"] == team
        ]

        if row.empty:
            return 0

        return float(
            row.iloc[0]["points"]
        )

    def get_group_winners(self, state):

        winners = []

        for group in sorted(state.keys()):

            team = (
                state[group]
                .get("rankings", {})
                .get("1st")
            )

            if team:
                winners.append(team)

        return winners

    def get_group_runners_up(self, state):

        runners_up = []

        for group in sorted(state.keys()):

            team = (
                state[group]
                .get("rankings", {})
                .get("2nd")
            )

            if team:
                runners_up.append(team)

        return runners_up

    def get_third_place_teams(self, state):

        third_places = []

        for group in sorted(state.keys()):

            team = (
                state[group]
                .get("rankings", {})
                .get("3rd")
            )

            if team:

                third_places.append(
                    {
                        "group": group,
                        "team": team,
                        "points": self.get_team_points(team)
                    }
                )

        return third_places

    def get_best_third_places(self, state):

        third_places = self.get_third_place_teams(
            state
        )

        third_places = sorted(
            third_places,
            key=lambda x: x["points"],
            reverse=True
        )

        return third_places[:8]

    def get_qualified_teams(self, state):

        winners = self.get_group_winners(
            state
        )

        runners_up = self.get_group_runners_up(
            state
        )

        best_thirds = [
            t["team"]
            for t in self.get_best_third_places(
                state
            )
        ]

        return {
            "winners": winners,
            "runners_up": runners_up,
            "best_third_places": best_thirds,
            "total_qualified":
                winners +
                runners_up +
                best_thirds
        }