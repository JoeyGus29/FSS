import streamlit as st

st.markdown("---")
st.subheader("Compare Two Players")
player1 = st.text_input("Player 1", "")
player2 = st.text_input("Player 2", "")

if player1 and player2:
    st.write(f"Comparison coming soon between **{player1}** and **{player2}**.")
    st.info("This feature will break down differences by trait grade, film score, and fantasy projection.")
