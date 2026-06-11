# ⚽ FIFA World Cup 2026 Prediction System

<p align="center">
  <img width="980" height="547" alt="FIFA World Cup 2026 Prediction" src="https://github.com/user-attachments/assets/8f53897d-2789-4909-85cc-60ca97c58419" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Scikit--Learn-RandomForest-F7931E?style=flat&logo=scikit-learn&logoColor=white" alt="Scikit-learn"/>
  <img src="https://img.shields.io/badge/Matches%20Analyzed-964-1D9E75?style=flat" alt="Matches Analyzed"/>
  <img src="https://img.shields.io/badge/Teams%20Covered-211-7F77DD?style=flat" alt="Teams Covered"/>
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat" alt="License"/>
</p>

---

## Executive Summary

A machine learning-powered tournament simulation platform that predicts the FIFA World Cup 2026. The application uniquely **combines human football knowledge with automated ML prediction** — users control the group stage outcomes, and a trained Random Forest model automatically simulates the entire knockout bracket from Round of 32 through to the Final.

Built on 964 historical World Cup matches (1930–2022) and current FIFA rankings for 211 national teams, this system demonstrates the full data science lifecycle: data engineering, feature engineering, model training, and interactive deployment via Streamlit.

---

## Business Problem

Predicting a 48-team tournament is complex because:

- Team strength changes continuously over time
- FIFA rankings evolve between qualifiers and the tournament
- Historical performance at major tournaments differs from regular internationals
- Human bracketology is subject to bias and recency effects
- The bracket structure creates unique, non-repeatable matchups

**This project addresses those challenges by:** separating the human-judgment component (group stage prediction) from the ML-driven component (knockout simulation), ensuring the system is both engaging for users and grounded in statistical evidence.

---

## Project Objectives

1. Train a binary match outcome classifier on historical World Cup data
2. Engineer features that capture relative team strength effectively
3. Build a modular, engine-driven simulation architecture
4. Create an interactive Streamlit application that simulates a full 48-team tournament
5. Demonstrate how ML can be embedded within a decision-support system

---

## Dataset Overview

| Dataset | Records | Description |
|---|---|---|
| `matches_1930_2022.csv` | 964 matches | Historical FIFA World Cup results |
| `fifa_ranking_2026-06-08.csv` | 211 teams | Current FIFA rankings, points, confederation |
| `fifa_ranking_2022-10-06.csv` | 211 teams | 2022 ranking snapshot for historical alignment |
| `group_fixtures.csv` | 48 teams / 12 groups | Official FIFA 2026 group stage draw |
| `knockout_slots.csv` | 32 slots | Official FIFA 2026 knockout bracket positions |
| `world_cup.csv` | Supporting reference | Historical tournament metadata |

---

## Data Validation & Cleaning Summary

- **Team name standardisation:** Historical match data uses legacy country names (e.g. "West Germany", "Czechoslovakia"). A dedicated `phase2_team_matching.ipynb` notebook resolves these to current FIFA naming conventions before feature joins.
- **Ranking joins:** Matches are joined to the ranking dataset via cleaned team name keys. Teams without a current FIFA ranking are handled with fallback rank values.
- **Target encoding:** Match outcomes are encoded as binary (1 = home win, 0 = away win/draw). Draws in knockout rounds are treated as the eventual match winner progressing.
- **Era flag:** A `modern_era` binary flag distinguishes pre-1990 football (fewer data points, different tactical environment) from the modern game.

---

## Exploratory Data Analysis Summary

Key insights from `01_data_exploration.ipynb`:

- Historically, higher-ranked teams win approximately **62% of knockout matches** — providing a naive baseline against which the model is evaluated
- Top-10 FIFA-ranked teams show a significantly higher win rate in knockout matches vs. group stage encounters
- Points difference (not rank difference alone) is a stronger predictor of match outcomes
- Experience (rated match count) has diminishing returns beyond ~150 matches

---

## Methodology

```
Raw Data → Name Standardisation → Feature Engineering → Model Training
    ↓                                                           ↓
Group Stage Input (user)                            Random Forest Classifier
    ↓                                                           ↓
Qualification Engine                                   Match Predictor
    ↓                                                           ↓
Bracket Resolver                              Confidence Score (probability)
    ↓                                                           ↓
Tournament Simulator ──────────────────────────────────────────┘
    ↓
Champion + Full Bracket Output
```

---

## Feature Engineering

The model uses **8 engineered features** derived from raw FIFA rankings and match data:

| Feature | Formula | Rationale |
|---|---|---|
| `rank_diff` | `home_rank − away_rank` | Relative ranking strength |
| `points_diff` | `home_points − away_points` | FIFA points advantage |
| `experience_diff` | `home_rated_matches − away_rated_matches` | International experience gap |
| `home_rank_inv` | `1 / home_rank` | Non-linear reward for top-ranked teams |
| `away_rank_inv` | `1 / away_rank` | Non-linear reward for top-ranked teams |
| `home_top10` | `1 if home_rank ≤ 10` | Elite team indicator |
| `away_top10` | `1 if away_rank ≤ 10` | Elite team indicator |
| `modern_era` | `1 if year ≥ 1990` | Era normalisation flag |
| `round_encoded` | ordinal encoding | Tournament stage weight |


> **See:** `phase3_build_training_data.ipynb` for full feature construction pipeline

---

## Machine Learning Model

### Model Selected: Random Forest Classifier

**Why Random Forest?**

- Handles non-linear feature interactions (e.g. rank_inv features)
- Robust to the class imbalance present in knockout match data
- Provides probability estimates for confidence scoring
- Interpretable via feature importance

### Training Configuration

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
```

## Application Architecture

### Core Engines

| Engine | File | Responsibility |
|---|---|---|
| Group Engine | `engines/group_engine.py` | Group initialisation, user ranking, state management |
| Qualification Engine | `engines/qualification_engine.py` | Determines 32 qualified teams (12 winners + 12 runners-up + 8 best 3rd) |
| Bracket Resolver | `engines/bracket_resolver.py` | Maps official FIFA slot codes to actual qualified teams |
| Slot Resolver | `engines/slot_resolver.py` | Handles slot ambiguity for best third-place slots |
| Match Predictor | `engines/predictor.py` | Feature creation + model inference + probability output |
| Tournament Simulator | `engines/tournament_simulator.py` | Round-by-round simulation, winner progression |
| Bracket Engine | `engines/bracket_engine.py` | Bracket state and match generation |
| Evaluation Engine | `engines/evaluation_engine.py` | Post-simulation scoring |

### Simulation Flow

```
User selects group rankings (12 groups × 4 positions)
            ↓
Qualification Engine → 32 qualified teams
            ↓
Bracket Resolver → Official matchups (e.g. Runner-up A vs Winner C)
            ↓
Round of 32 → Predictor → Winners advance
            ↓
Round of 16 → Predictor → Winners advance
            ↓
Quarter-Finals → Predictor → Winners advance
            ↓
Semi-Finals → Predictor → Winners advance
            ↓
Final → Predictor → 🏆 Champion + Confidence Score
```

---

## Key Findings

1. **Points difference is the most predictive single feature** — more informative than rank difference alone, as ranking positions can be deceptively close at the top
2. **Top-10 flag provides significant signal** — teams ranked 1–10 win knockout matches at a materially higher rate than teams ranked 11–20
3. **Era normalisation matters** — pre-1990 results introduce noise; the `modern_era` flag improves both precision and recall on post-2000 matches
4. **Experience gap is most predictive in early rounds** — its importance diminishes in semi-finals and finals, where all teams are highly experienced
5. **Model confidence correlates with rank gap** — Argentina vs Saudi Arabia produces >85% confidence; historically close matchups (Brazil vs France) sit near 55%

---

## Technologies Used

| Category | Technology |
|---|---|
| Language | Python 3.10+ |
| Web framework | Streamlit |
| ML library | Scikit-Learn |
| Data processing | Pandas, NumPy |
| Model serialisation | Joblib |
| Testing | Pytest (12 test files) |
| Version control | Git / GitHub |

---

## Installation Instructions

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/fifa-wc26-predictor.git
cd fifa-wc26-predictor

# Create virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

---

## How to Reproduce the Project

1. **Data exploration:** Run `notebooks/01_data_exploration.ipynb`
2. **Data audit:** Run `notebooks/phase1_data_audit.ipynb`
3. **Team name matching:** Run `notebooks/phase2_team_matching.ipynb`
4. **Build training data & train model:** Run `notebooks/phase3_build_training_data.ipynb`
5. **Run tests:** `pytest tests/`
6. **Launch app:** `streamlit run app.py`

---

## Repository Structure

```
fifa-wc26-predictor/
│
├── data/                          # All datasets (gitignored if large)
│   ├── fifa_ranking_2022-10-06.csv
│   ├── fifa_ranking_2026-06-08.csv
│   ├── group_fixtures.csv
│   ├── knockout_slots.csv
│   ├── matches_1930_2022.csv
│   └── world_cup.csv
│
├── engines/                       # Core simulation engines
│   ├── bracket_engine.py
│   ├── bracket_flow_engine.py
│   ├── bracket_resolver.py
│   ├── evaluation_engine.py
│   ├── group_engine.py
│   ├── predictor.py
│   ├── qualification_engine.py
│   ├── slot_resolver.py
│   ├── tournament_engine.py
│   └── tournament_simulator.py
│
├── components/                    # Streamlit UI components
│   ├── bracket_tree.py
│   └── champion_card.py
│
├── models/                        # Serialised trained model
│   └── winner_model.pkl
│
├── notebooks/                     # EDA, feature engineering, training
│   ├── 01_data_exploration.ipynb
│   ├── phase1_data_audit.ipynb
│   ├── phase2_team_matching.ipynb
│   └── phase3_build_training_data.ipynb
│
├── tests/                         # Pytest test suite (12 files)
│   ├── test_bracket_advanced.py
│   ├── test_bracket_flow.py
│   ├── test_bracket_resolver.py
│   ├── test_bracket.py
│   ├── test_engine.py
│   ├── test_evaluation.py
│   ├── test_predictor.py
│   ├── test_qualification.py
│   ├── test_simulator.py
│   ├── test_slot_resolver.py
│   └── test_tournament.py
│
├── utils/                         # Shared utilities
│   └── data_loader.py
│
├── images/                        # README visuals and screenshots
│   ├── banner.png
│   ├── app_demo.png
│   ├── bracket_view.png
│   ├── champion_card.png
│   ├── confusion_matrix.png
│   ├── feature_importance.png
│   ├── eda_win_rates.png
│   └── rank_vs_outcome.png
│
├── app.py                         # Streamlit entry point
├── requirements.txt
├── .gitignore
└── README.md
```


## Author

**Shubham Malkar**  <br>
B.Com (Final Year) | Mithibai College, Mumbai  <br> 
Data Science & Analytics | ML 

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](http://www.linkedin.com/in/shubhammalkar)
[![GitHub](https://img.shields.io/badge/GitHub-Portfolio-181717?style=flat&logo=github)](https://github.com/Shubh-0077)

---

*Built with historical FIFA data. Not affiliated with FIFA.*
