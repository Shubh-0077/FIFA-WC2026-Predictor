import streamlit as st

def render_champion(champion, match_results):

    st.markdown("---")
    st.subheader("👑 Champion Prediction")

    if not champion:
        st.info("Final match not decided yet")
        return

    st.success(f"🏆 FIFA World Cup 2026 Winner: {champion}")

    st.markdown("### 🔥 Tournament Impact Summary")

    wins = len([m for m in match_results.values() if m == champion])

    st.metric(label="Matches Won", value=wins)

    st.markdown("### 🧭 Path to Trophy")

    for mid, team in match_results.items():
        if team == champion:
            st.write(f"✔ Won Match {mid}")