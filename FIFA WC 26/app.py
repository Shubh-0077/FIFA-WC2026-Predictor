import streamlit as st

from engines.group_engine import GroupEngine
from engines.qualification_engine import QualificationEngine
from engines.bracket_resolver import BracketResolver
from engines.tournament_simulator import TournamentSimulator

from utils.data_loader import load_knockout_data

from components.bracket_tree import render_bracket_tree
from components.champion_card import render_champion


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="FIFA World Cup 2026 Predictor",
    layout="wide"
)

st.title("⚽ FIFA World Cup 2026 Predictor")


# =====================================
# GROUP DATA
# =====================================

GROUPS = {
    "A": ["Mexico", "South Africa", "Korea Republic", "Czechia"],
    "B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["USA", "Paraguay", "Australia", "Türkiye"],
    "E": ["Germany", "Curaçao", "Côte d'Ivoire", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "IR Iran", "New Zealand"],
    "H": ["Spain", "Cabo Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "Congo DR", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"]
}


# =====================================
# ENGINE INIT
# =====================================

group_engine = GroupEngine(GROUPS)

qualification_engine = QualificationEngine()

bracket_map = load_knockout_data()

resolver = BracketResolver(
    bracket_map,
    qualification_engine
)

simulator = TournamentSimulator()


# =====================================
# SESSION STATE
# =====================================

if "group_state" not in st.session_state:
    st.session_state.group_state = (
        group_engine.initialize_state()
    )

state = st.session_state.group_state


# =====================================
# GROUP STAGE UI
# =====================================

st.subheader("🏆 Group Stage Predictions")

for group in sorted(state.keys()):

    st.markdown(f"### Group {group}")

    teams = state[group]["teams"]

    cols = st.columns(4)

    positions = [
        "1st",
        "2nd",
        "3rd",
        "4th"
    ]

    for i, pos in enumerate(positions):

        selected = set(
            state[group]["rankings"].values()
        )

        selected.discard(None)

        current = (
            state[group]["rankings"][pos]
        )

        available = [
            t for t in teams
            if t not in selected
        ]

        if current:
            available.append(current)

        options = ["Select"] + sorted(
            list(set(available))
        )

        default_index = 0

        if current in options:
            default_index = options.index(
                current
            )

        choice = cols[i].selectbox(
            pos,
            options,
            index=default_index,
            key=f"{group}_{pos}"
        )

        if choice != "Select":
            state = (
                group_engine.update_ranking(
                    state,
                    group,
                    pos,
                    choice
                )
            )

st.session_state.group_state = state

st.markdown("---")


# =====================================
# TOURNAMENT SIMULATION
# =====================================

if st.button("🚀 Simulate Tournament"):

    # -------------------------
    # ROUND OF 32
    # -------------------------

    r32_matches = (
        resolver.build_round_of_32(
            state
        )
    )

    r32_results = (
        simulator.simulate_round(
            r32_matches
        )
    )

    match_winners = {
        r["match_id"]: r["winner"]
        for r in r32_results
    }

    # -------------------------
    # ROUND OF 16
    # -------------------------

    r16_matches = (
        resolver.build_round_of_16(
            state,
            match_winners
        )
    )

    r16_results = (
        simulator.simulate_round(
            r16_matches
        )
    )

    match_winners.update({
        r["match_id"]: r["winner"]
        for r in r16_results
    })

    # -------------------------
    # QUARTER FINALS
    # -------------------------

    qf_matches = (
        resolver.build_quarterfinals(
            state,
            match_winners
        )
    )

    qf_results = (
        simulator.simulate_round(
            qf_matches
        )
    )

    match_winners.update({
        r["match_id"]: r["winner"]
        for r in qf_results
    })

    # -------------------------
    # SEMI FINALS
    # -------------------------

    sf_matches = (
        resolver.build_semifinals(
            state,
            match_winners
        )
    )

    sf_results = (
        simulator.simulate_round(
            sf_matches
        )
    )

    match_winners.update({
        r["match_id"]: r["winner"]
        for r in sf_results
    })

    # -------------------------
    # FINAL
    # -------------------------

    final_matches = (
        resolver.build_final(
            state,
            match_winners
        )
    )

    final_results = (
        simulator.simulate_round(
            final_matches
        )
    )

    match_winners.update({
        r["match_id"]: r["winner"]
        for r in final_results
    })

    final_prediction = final_results[0]

    champion = (
        final_prediction["winner"]
    )

    confidence = (
        final_prediction["probability"]
    )

    # =================================
    # CHAMPION DISPLAY
    # =================================

    st.success(
        f"🏆 Predicted Champion: "
        f"{champion}"
    )

    st.info(
        f"Prediction Confidence: "
        f"{confidence:.1%}"
    )

    render_champion(
        champion,
        match_winners
    )

    # =================================
    # FINAL MATCH
    # =================================

    st.subheader(
        "⚽ Final Match Prediction"
    )

    st.write(
        f"**{final_prediction['teamA']}** "
        f"vs "
        f"**{final_prediction['teamB']}**"
    )

    st.write(
        f"Winner: "
        f"**{champion}**"
    )

    st.write(
        f"Confidence: "
        f"**{confidence:.1%}**"
    )

    # =================================
    # BRACKET TREE
    # =================================

    tree = {

        "R32": {
            "L1": (
                match_winners.get(73, "TBD"),
                match_winners.get(74, "TBD")
            ),
            "L2": (
                match_winners.get(75, "TBD"),
                match_winners.get(76, "TBD")
            ),
            "L3": (
                match_winners.get(77, "TBD"),
                match_winners.get(78, "TBD")
            ),
            "L4": (
                match_winners.get(79, "TBD"),
                match_winners.get(80, "TBD")
            ),
            "R1": (
                match_winners.get(81, "TBD"),
                match_winners.get(82, "TBD")
            ),
            "R2": (
                match_winners.get(83, "TBD"),
                match_winners.get(84, "TBD")
            ),
            "R3": (
                match_winners.get(85, "TBD"),
                match_winners.get(86, "TBD")
            ),
            "R4": (
                match_winners.get(87, "TBD"),
                match_winners.get(88, "TBD")
            )
        },

        "R16": {
            "L1": match_winners.get(89, "TBD"),
            "L2": match_winners.get(90, "TBD"),
            "L3": match_winners.get(91, "TBD"),
            "L4": match_winners.get(92, "TBD"),
            "R1": match_winners.get(93, "TBD"),
            "R2": match_winners.get(94, "TBD"),
            "R3": match_winners.get(95, "TBD"),
            "R4": match_winners.get(96, "TBD")
        },

        "QF": {
            "L1": match_winners.get(97, "TBD"),
            "L2": match_winners.get(98, "TBD"),
            "R1": match_winners.get(99, "TBD"),
            "R2": match_winners.get(100, "TBD")
        },

        "SF": {
            "L": match_winners.get(101, "TBD"),
            "R": match_winners.get(102, "TBD")
        },

        "FINAL": champion
    }

    st.markdown("---")
    st.subheader("🏟 Tournament Bracket")

    render_bracket_tree(tree)