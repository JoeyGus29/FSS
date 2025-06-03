import streamlit as st
import pandas as pd

st.title("Player Comparison")
st.markdown("---")
st.subheader("Compare Two Players")

# Example: load all player names from your WR CSV (you can expand this to RB/QB/TE as needed)
try:
    wr_df = pd.read_csv("wr_fss_rankings.csv")
    wr_players = wr_df["Player"].tolist()
except:
    wr_players = []

player1 = st.selectbox("Player 1", wr_players)
player2 = st.selectbox("Player 2", wr_players, index=1 if len(wr_players) > 1 else 0)

if player1 and player2 and player1 != player2:
    st.write(f"Comparing **{player1}** vs **{player2}**")
    # Add player comparison details here
else:
    st.info("Select two different players to compare.")
