from engines.qualification_engine import (
    QualificationEngine
)


class SlotResolver:

    def __init__(self):

        self.qualifier_engine = (
            QualificationEngine()
        )

    def resolve(
        self,
        slot,
        group_state,
        match_results=None
    ):

        if not slot:
            return None

        rankings = group_state

        # Winner Group A
        if "Winner Group" in slot:

            group = slot.split()[-1]

            return (
                rankings[group]
                ["rankings"]
                ["1st"]
            )

        # Runner-up Group A
        if "Runner-up Group" in slot:

            group = slot.split()[-1]

            return (
                rankings[group]
                ["rankings"]
                ["2nd"]
            )

        # Match 73
        if "Match" in slot:

            if match_results is None:
                return None

            match_id = int(
                slot.split()[-1]
            )

            return match_results.get(
                match_id
            )

        # Best 3rd (...)
        if "Best 3rd" in slot:

            allowed_groups = (
                slot
                .split("(")[1]
                .replace(")", "")
                .replace("Groups", "")
                .strip()
                .split("/")
            )

            best_thirds = (
                self.qualifier_engine
                .get_best_third_places(
                    rankings
                )
            )

            eligible = []

            for team_data in best_thirds:

                if (
                    team_data["group"]
                    in allowed_groups
                ):
                    eligible.append(
                        team_data
                    )

            if not eligible:
                return None

            eligible = sorted(
                eligible,
                key=lambda x: x["points"],
                reverse=True
            )

            return eligible[0]["team"]

        return None
    