import streamlit as st

def render_bracket_tree(tree):

    st.subheader("🏆 FIFA 2026 Knockout Bracket")

    col1, col2, col3 = st.columns([2, 1, 2])

    # LEFT SIDE
    with col1:
        st.markdown("## 🔵 Left Bracket")

        st.markdown("### Round of 32")
        for i in ["L1", "L2", "L3", "L4"]:
            st.write(tree["R32"][i])

        st.markdown("### Round of 16")
        for i in ["L1", "L2", "L3", "L4"]:
            st.write(tree["R16"][i])

        st.markdown("### Quarter-Finals")
        for i in ["L1", "L2"]:
            st.write(tree["QF"][i])

    # CENTER
    with col2:
        st.markdown("## 🏆 FINAL")

        final = tree["FINAL"]

        if final == "TBD":
            st.warning("Final not decided yet")
        else:
            st.success(f"Champion: {final}")

    # RIGHT SIDE
    with col3:
        st.markdown("## 🔴 Right Bracket")

        st.markdown("### Round of 32")
        for i in ["R1", "R2", "R3", "R4"]:
            st.write(tree["R32"][i])

        st.markdown("### Round of 16")
        for i in ["R1", "R2", "R3", "R4"]:
            st.write(tree["R16"][i])

        st.markdown("### Quarter-Finals")
        for i in ["R1", "R2"]:
            st.write(tree["QF"][i])