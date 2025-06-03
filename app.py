# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fantasy Success Score Dashboard", layout="wide")
st.title("🏈 GridironIQ\nFantasy Success Score (FSS) Dashboard")

tabs = st.tabs(["Log In or Sign Up", "WR Rankings", "RB Rankings", "TE Rankings", "QB Rankings", "About Us / Contact Us", "Terms of Use & Privacy Policy"])

# Map each tab to its raw-CSV filename (must be in the same folder as app.py)
csv_paths = {
    "WR Rankings": "wr_fss_rankings.csv",
    "RB Rankings": "rb_fss_rankings.csv",
    "TE Rankings": "te_fss_rankings.csv",
    "QB Rankings": "qb_fss_rankings.csv"
}

def load_and_rescale(csv_file):
    """
    1) Load raw FSS CSV (columns: ['Player','FSS']).
    2) Rescale 'FSS' into [50,99] via min-max on that column.
    3) Return a DataFrame with columns ['Player','Raw_FSS','Scaled_FSS'].
    """
    df = pd.read_csv(csv_file)
    if "FSS" not in df.columns:
        st.warning(f"CSV {csv_file} missing 'FSS' column.")
        return pd.DataFrame(columns=["Player", "Raw_FSS", "Scaled_FSS"])
    
    df = df[["Player", "FSS"]].dropna()
    df = df.rename(columns={"FSS": "Raw_FSS"})
    raw_min = df["Raw_FSS"].min()
    raw_max = df["Raw_FSS"].max()
    
    # If raw_min == raw_max, map everyone to 99 (or 50). Here we'll map all to 75 if no spread.
    if raw_max == raw_min:
        df["Scaled_FSS"] = 75.0
    else:
        df["Scaled_FSS"] = df["Raw_FSS"].apply(
            lambda x: ((x - raw_min) / (raw_max - raw_min)) * (99 - 50) + 50
        )
    df["Scaled_FSS"] = df["Scaled_FSS"].round(1)
    return df

for i, pos in enumerate(["WR Rankings", "RB Rankings", "QB Rankings", "TE Rankings"]):
    with tabs[i]:
        st.subheader(f"Rescaled FSS Rankings – {pos}")

        csv_file = csv_paths[pos]
        try:
            df = load_and_rescale(csv_file)

            if df.empty:
                st.info(f"No data yet for {pos}.")
            else:
                # Sort by Scaled_FSS descending
                df = df.sort_values("Scaled_FSS", ascending=False).reset_index(drop=True)
                
                # Plot the bar chart
                fig, ax = plt.subplots(figsize=(8, max(4, len(df)*0.2)))
                ax.barh(df["Player"], df["Scaled_FSS"], color="steelblue")
                ax.invert_yaxis()
                ax.set_xlabel("Rescaled FSS (50–99)")
                ax.set_title(f"{pos} – First‐Round (Raw  -> Rescaled 50–99)")

                # Annotate each bar with its scaled value
                for bar in ax.patches:
                    width = bar.get_width()
                    ax.annotate(f"{width:.1f}",
                                xy=(width, bar.get_y() + bar.get_height() / 2),
                                xytext=(3, 0),
                                textcoords="offset points",
                                ha="left", va="center")

                st.pyplot(fig)

                # Show a small table if there are fewer than, say, 10 players,
                # otherwise show just top 10 and let user scroll.
                num_display = min(len(df), 10)
                st.dataframe(df.head(num_display)[["Player", "Raw_FSS", "Scaled_FSS"]])

                # Download button for the full rescaled table
                csv_bytes = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label=f"Download {pos} FSS (Rescaled 50–99) CSV",
                    data=csv_bytes,
                    file_name=f"{pos.lower()}_fss_rescaled.csv",
                    mime="text/csv"
                )

        except FileNotFoundError:
            st.warning(f"Could not find `{csv_file}`. Upload the CSV to this folder and refresh.")
