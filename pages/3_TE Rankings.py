import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Rescaled FSS Rankings – TE Rankings")

csv_file = "te_fss_rankings.csv"

def load_and_rescale(csv_file):
    df = pd.read_csv(csv_file)
    if "FSS" not in df.columns and "Raw_FSS" not in df.columns:
        st.warning(f"CSV {csv_file} missing 'FSS' column.")
        return pd.DataFrame(columns=["Player", "Raw_FSS", "Scaled_FSS"])
    if "Raw_FSS" not in df.columns:
        df = df.rename(columns={"FSS": "Raw_FSS"})
    df = df[["Player", "Raw_FSS"]].dropna()
    raw_min = df["Raw_FSS"].min()
    raw_max = df["Raw_FSS"].max()
    if raw_max == raw_min:
        df["Scaled_FSS"] = 75.0
    else:
        df["Scaled_FSS"] = df["Raw_FSS"].apply(
            lambda x: ((x - raw_min) / (raw_max - raw_min)) * (99 - 50) + 50
        )
    df["Scaled_FSS"] = df["Scaled_FSS"].round(1)
    return df

try:
    df = load_and_rescale(csv_file)
    if df.empty:
        st.info("No data yet for TEs.")
    else:
        df = df.sort_values("Scaled_FSS", ascending=False).reset_index(drop=True)
        fig, ax = plt.subplots(figsize=(8, max(4, len(df)*0.22)))
        ax.barh(df["Player"], df["Scaled_FSS"], color="mediumpurple")
        ax.invert_yaxis()
        ax.set_xlabel("Rescaled FSS (50–99)")
        ax.set_title("TE – First-Round (Raw  -> Rescaled 50–99)")
        for bar in ax.patches:
            width = bar.get_width()
            ax.annotate(f"{width:.1f}", xy=(width, bar.get_y() + bar.get_height()/2),
                        xytext=(3, 0), textcoords="offset points",
                        ha="left", va="center")
        st.pyplot(fig)
        st.dataframe(df[["Player", "Raw_FSS", "Scaled_FSS"]])
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download TE FSS (Rescaled 50–99) CSV",
            data=csv_bytes,
            file_name="te_fss_rescaled.csv",
            mime="text/csv"
        )
except FileNotFoundError:
    st.warning(f"Could not find `{csv_file}`. Upload the CSV and refresh.")
