from engines.qualification_engine import QualificationEngine

engine = QualificationEngine()

sample_state = {
    "A": {
        "rankings": {
            "1st": "Argentina",
            "2nd": "Mexico",
            "3rd": "Poland",
            "4th": "Saudi Arabia"
        }
    },
    "B": {
        "rankings": {
            "1st": "France",
            "2nd": "Denmark",
            "3rd": "Tunisia",
            "4th": "Australia"
        }
    }
}

print("Winners")
print(
    engine.get_group_winners(
        sample_state
    )
)

print("\nRunners Up")
print(
    engine.get_group_runners_up(
        sample_state
    )
)

print("\nBest Third Places")
print(
    engine.get_best_third_places(
        sample_state
    )
)