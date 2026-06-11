from engines.tournament_engine import TournamentEngine
from engines.bracket_flow_engine import BracketFlowEngine

# simulate match results
tournament = TournamentEngine({})

tournament.set_result(73, "Brazil")
tournament.set_result(74, "Argentina")

# bracket map (simplified)
bracket_map = {
    89: {
        "home_slot": "Winner Match 73",
        "away_slot": "Winner Match 74"
    }
}

engine = BracketFlowEngine(tournament, bracket_map)

print(engine.build_round([89]))