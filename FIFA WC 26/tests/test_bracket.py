from engines.bracket_engine import BracketEngine

group_results = {
    "A": {
        "winner": "Mexico",
        "runner_up": "USA",
        "third": "Canada"
    }
}

engine = BracketEngine(group_results)

print(engine.resolve_slot("Winner Group A"))