from engines.evaluation_engine import EvaluationEngine

engine = EvaluationEngine()

prediction = {
    "winner": "Brazil",
    "home_goals": 2,
    "away_goals": 1,
    "corners": 8,
    "yellow_cards": 3,
    "red_cards": 0
}

actual = {
    "winner": "Brazil",
    "home_goals": 2,
    "away_goals": 1,
    "corners": 9,
    "yellow_cards": 3,
    "red_cards": 0
}

print(engine.score_match(prediction, actual, "Quarter-final"))