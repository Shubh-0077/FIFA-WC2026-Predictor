class BracketResolver:

    def __init__(
        self,
        bracket_map,
        qualification_engine
    ):
        self.bracket_map = bracket_map
        self.qe = qualification_engine

    # ---------------------------------
    # GROUP LOOKUPS
    # ---------------------------------
    def get_group_winner(
        self,
        state,
        group
    ):
        return (
            state[group]
            ["rankings"]
            ["1st"]
        )

    def get_group_runner_up(
        self,
        state,
        group
    ):
        return (
            state[group]
            ["rankings"]
            ["2nd"]
        )

    # ---------------------------------
    # THIRD PLACE LOOKUPS
    # ---------------------------------
    def get_best_thirds(
        self,
        state
    ):
        return self.qe.get_best_third_places(
            state
        )

    # ---------------------------------
    # SLOT RESOLUTION
    # ---------------------------------
    def resolve_slot(
        self,
        slot,
        state,
        match_winners,
        third_pool
    ):

        if not slot:
            return None

        # Winner Group A
        if "Winner Group" in slot:

            group = slot.split()[-1]

            return self.get_group_winner(
                state,
                group
            )

        # Runner-up Group A
        if "Runner-up Group" in slot:

            group = slot.split()[-1]

            return self.get_group_runner_up(
                state,
                group
            )

        # Best Third
        if "Best 3rd" in slot:

            if len(third_pool) == 0:
                return None

            return third_pool.pop(0)

        # Winner Match 73
        if "Winner Match" in slot:

            match_id = int(
                slot.split()[-1]
            )

            return match_winners.get(
                match_id
            )

        return None

    # ---------------------------------
    # BUILD ROUND
    # ---------------------------------
    def build_round(
        self,
        round_name,
        state,
        match_winners,
        third_pool
    ):

        matches = []

        for match_id, row in self.bracket_map.items():

            if row["round"] != round_name:
                continue

            team_a = self.resolve_slot(
                row["home_slot"],
                state,
                match_winners,
                third_pool
            )

            team_b = self.resolve_slot(
                row["away_slot"],
                state,
                match_winners,
                third_pool
            )

            matches.append(
                {
                    "match_id": match_id,
                    "teamA": team_a,
                    "teamB": team_b
                }
            )

        return sorted(
            matches,
            key=lambda x: x["match_id"]
        )

    # ---------------------------------
    # FULL TOURNAMENT
    # ---------------------------------
    def build_round_of_32(
        self,
        state
    ):

        third_pool = [
            x["team"]
            for x in self.qe.get_best_third_places(
                state
            )
        ]

        return self.build_round(
            "Round of 32",
            state,
            {},
            third_pool
        )

    def build_round_of_16(
        self,
        state,
        winners
    ):

        return self.build_round(
            "Round of 16",
            state,
            winners,
            []
        )

    def build_quarterfinals(
        self,
        state,
        winners
    ):

        return self.build_round(
            "Quarter-final",
            state,
            winners,
            []
        )

    def build_semifinals(
        self,
        state,
        winners
    ):

        return self.build_round(
            "Semi-final",
            state,
            winners,
            []
        )

    def build_final(
        self,
        state,
        winners
    ):

        return self.build_round(
            "Final",
            state,
            winners,
            []
        )