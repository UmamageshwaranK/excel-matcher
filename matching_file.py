# app.py
import re
import pandas as pd
import streamlit as st
from rapidfuzz import fuzz

# ---------- Normalize ----------
def normalize(s):
    if pd.isna(s):
        return ""
    return re.sub(r"[^A-Za-z0-9]", "", str(s)).lower()

# ---------- Match Function ----------
def match_data(master_df, messy_df, threshold=95):
    results = []
    seen_matches = {}  # Track duplicates

    for idx, messy_row in messy_df.iterrows():
        messy_str = normalize(messy_row["Messy_Data"])
        best_score = -1
        best_code = None
        best_original = None

        # Compare with master
        for _, master_row in master_df.iterrows():
            master_str = normalize(master_row["Original_Data"])
            score = fuzz.token_sort_ratio(messy_str, master_str)

            if score > best_score:
                best_score = score
                best_code = master_row["Unique_Code"]
                best_original = master_row["Original_Data"]

        # ---------- Decide Match Type ----------
        if best_score >= threshold:
            if best_code not in seen_matches:
                match_type = "Unique"
                seen_matches[best_code] = 1
            else:
                match_type = "Duplicate"
                seen_matches[best_code] += 1

            results.append({
                "Messy_Data": messy_row["Messy_Data"],
                "Matched_Unique_Code": best_code,
                "Matched_Original_Data": best_original,
                "Match_Type": match_type,
                "Match_Score": best_score,
                "Extra_Addon": None,
                "Suggested_Master": None
            })

        else:
            results.append({
                "Messy_Data": messy_row["Messy_Data"],
                "Matched_Unique_Code": None,
                "Matched_Original_Data": None,
                "Match_Type": "New Variant",
                "Match_Score": best_score,
                "Extra_Addon": messy_row["Messy_Data"],
                "Suggested_Master": best_original  # closest master even if score low
            })

    return pd.DataFrame(results)

# ---------- Streamlit UI ----------
st.title("Messy vs Master Data Matching")

uploaded_master = st.file_uploader("Upload Master Data (CSV)", type=["csv"])
uploaded_messy = st.file_uploader("Upload Messy Data (CSV)", type=["csv"])

threshold = st.slider("Match Threshold", 50, 100, 95)

if uploaded_master and uploaded_messy:
    master_df = pd.read_csv(uploaded_master)
    messy_df = pd.read_csv(uploaded_messy)

    if "Unique_Code" not in master_df.columns or "Original_Data" not in master_df.columns:
        st.error("Master CSV must have columns: Unique_Code, Original_Data")
    elif "Messy_Data" not in messy_df.columns:
        st.error("Messy CSV must have column: Messy_Data")
    else:
        output_df = match_data(master_df, messy_df, threshold)
        st.write("### Results", output_df)

        # Download button
        csv = output_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Results", csv, "results.csv", "text/csv")
