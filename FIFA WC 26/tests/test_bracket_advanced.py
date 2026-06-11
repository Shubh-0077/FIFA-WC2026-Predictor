from engines.bracket_engine import BracketEngine

group_results = {
    "A": {
        "winner": "Mexico",
        "runner_up": "USA",
        "third": "Canada"
    }
}

engine = BracketEngine(group_results)

print("Winner:", engine.resolve_slot("Winner Group A"))
print("Runner:", engine.resolve_slot("Runner-up Group A"))
print("Third:", engine.resolve_slot("Third Group A"))

engine.set_match_result(73, "Brazil")

print("Match 73:", engine.resolve_slot("Winner Match 73"))