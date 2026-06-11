from engines.predictor import MatchPredictor

predictor = MatchPredictor()

result = predictor.predict_match(
    "Argentina",
    "Portugal"
)

print(result)