class BracketEngine:
    def __init__(self, group_results):
        self.group_results = group_results
        self.match_results = {}

    # --------------------------
    # GROUP SLOT RESOLUTION
    # --------------------------
    def resolve_group_slot(self, slot):
        parts = slot.lower().split()

        if "group" not in parts:
            return None

        group = slot.split()[-1]

        if "winner" in parts:
            return self.group_results[group]["winner"]

        if "runner-up" in slot.lower() or "runner" in parts:
            return self.group_results[group]["runner_up"]

        if "third" in parts:
            return self.group_results[group]["third"]

        return None

    # --------------------------
    # MATCH SLOT RESOLUTION
    # --------------------------
    def resolve_match_slot(self, slot):
        try:
            match_id = int(slot.split()[-1])
            return self.match_results.get(match_id)
        except:
            return None

    # --------------------------
    # MASTER RESOLVER
    # --------------------------
    def resolve_slot(self, slot):
        if "Group" in slot:
            return self.resolve_group_slot(slot)

        if "Match" in slot:
            return self.resolve_match_slot(slot)

        return None

    # --------------------------
    # STORE MATCH RESULT
    # --------------------------
    def set_match_result(self, match_id, winner):
        self.match_results[match_id] = winner