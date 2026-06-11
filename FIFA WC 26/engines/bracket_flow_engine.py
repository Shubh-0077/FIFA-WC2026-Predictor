class BracketFlowEngine:
    def __init__(self, tournament_engine, bracket_map):
        """
        tournament_engine → handles match results
        bracket_map → knockout_slots.csv parsed structure
        """
        self.tournament_engine = tournament_engine
        self.bracket_map = bracket_map

    # --------------------------
    # RESOLVE SLOT INTO TEAM
    # --------------------------
    def resolve(self, slot):
        if "Match" in slot:
            match_id = int(slot.split()[-1])
            return self.tournament_engine.get_winner(match_id)

        if "Group" in slot:
            # fallback placeholder (later connect BracketEngine)
            return slot

        return slot

    # --------------------------
    # BUILD FULL MATCH
    # --------------------------
    def build_match(self, match_id):
        match = self.bracket_map[match_id]

        teamA = self.resolve(match["home_slot"])
        teamB = self.resolve(match["away_slot"])

        return {
            "match_id": match_id,
            "teamA": teamA,
            "teamB": teamB
        }

    # --------------------------
    # BUILD ROUND
    # --------------------------
    def build_round(self, match_ids):
        return [self.build_match(mid) for mid in match_ids]