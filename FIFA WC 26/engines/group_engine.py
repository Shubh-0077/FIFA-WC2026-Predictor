class GroupEngine:
    def __init__(self, group_data):
        """
        group_data format:
        {
            "A": ["Mexico", "USA", "Canada", "Germany"],
            ...
        }
        """
        self.group_data = group_data

    def initialize_state(self):
        """
        Creates empty ranking structure for UI
        """
        state = {}

        for group, teams in self.group_data.items():
            state[group] = {
                "teams": teams,
                "rankings": {
                    "1st": None,
                    "2nd": None,
                    "3rd": None,
                    "4th": None
                }
            }

        return state

    def update_ranking(self, state, group, position, team):
        """
        Updates ranking safely
        """
        state[group]["rankings"][position] = team
        return state

    def get_group_rankings(self, state, group):
        """
        Returns current rankings of a group
        """
        return state[group]["rankings"]

    def validate_group(self, state, group):
        """
        Ensures no duplicates inside a group
        """
        rankings = state[group]["rankings"].values()
        filled = [t for t in rankings if t is not None]

        return len(filled) == len(set(filled))

    def get_all_rankings(self, state):
        """
        Returns full tournament group stage result
        """
        return {g: v["rankings"] for g, v in state.items()}