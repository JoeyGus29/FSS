import streamlit as st
import pandas as pd

st.title("Player Comparison")
st.markdown("---")
st.subheader("Compare Two Players")

# Example: load all player names from your WR CSV (do the same for RB, QB, TE)
try:
    wr_df = pd.read_csv("wr_fss_rankings.csv")
    wr_players = wr_df["Player"].tolist()
except:
    wr_players = []

# You can extend this to all positions if you want
all_players = wr_players  # + rb_players + qb_players + te_players

player1 = st.selectbox("Player 1", all_players)
player2 = st.selectbox("Player 2", all_players, index=1 if len(all_players) > 1 else 0)

if player1 and player2 and player1 != player2:
    st.write(f"Comparing **{player1}** vs **{player2}**")
    # Add your player score display/comparison logic here
else:
    st.info("Select two different players to compare.")
