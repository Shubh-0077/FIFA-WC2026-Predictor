from engines.bracket_resolver import BracketResolver
from engines.qualification_engine import QualificationEngine
from utils.data_loader import load_knockout_data

qe = QualificationEngine()

bracket = load_knockout_data()

resolver = BracketResolver(
    bracket,
    qe
)

print("Loaded Successfully")