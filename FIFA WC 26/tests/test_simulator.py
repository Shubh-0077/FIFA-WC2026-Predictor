from engines.tournament_simulator import TournamentSimulator

sim = TournamentSimulator()

matches = [
    {
        "match_id": 73,
        "teamA": "Argentina",
        "teamB": "France"
    }
]

print(sim.simulate_round(matches))