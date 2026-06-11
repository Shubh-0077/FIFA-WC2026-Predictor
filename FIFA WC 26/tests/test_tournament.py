from engines.tournament_engine import TournamentEngine

group_results = {
    "A": {
        "winner": "Mexico",
        "runner_up": "USA",
        "third": "Canada"
    }
}

engine = TournamentEngine(group_results)

engine.set_result(73, "Mexico")
engine.set_result(74, "Brazil")

round_32 = [
    (73, "Mexico", "France"),
    (74, "Brazil", "Argentina")
]

print(engine.build_round(round_32))