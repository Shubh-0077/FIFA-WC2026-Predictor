from engines.slot_resolver import (
    SlotResolver
)

resolver = SlotResolver()

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

print(
    resolver.resolve(
        "Winner Group A",
        sample_state
    )
)

print(
    resolver.resolve(
        "Runner-up Group B",
        sample_state
    )
)

print(
    resolver.resolve(
        "Best 3rd (Groups A/B)",
        sample_state
    )
)