"""
Project  : Family Planning Among Married Women of Reproductive Age
           in Kassala City, Sudan – 2025
Script   : Data Cleaning & Recoding
Author   : Abdulrahman Sirelkhatim
Date     : March 2026
Input    : 1_data/raw/raw.xlsx
Output   : 1_data/cleaned/cleaned_data.xlsx
           1_data/cleaned/qualitative_data.xlsx (open-ended responses, separate)
"""

import pandas as pd
import numpy as np

INPUT_FILE = "1_data/raw/raw.xlsx"
OUTPUT_QUANT = "1_data/cleaned/cleaned_data.xlsx"
OUTPUT_QUAL = "1_data/cleaned/qualitative_data.xlsx"

df = pd.read_excel(INPUT_FILE)
print(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")

df.drop(columns=[df.columns[0], df.columns[1]], inplace=True)

rename_map = {
    df.columns[0]: "age",
    df.columns[1]: "education",
    df.columns[2]: "occupation",
    df.columns[3]: "fp_use",
    df.columns[4]: "fp_method",
    df.columns[5]: "fp_duration",
    df.columns[6]: "fp_why",
    df.columns[7]: "husband_reaction",
    df.columns[8]: "husband_concerns",
    df.columns[9]: "fp_encouragement",
    df.columns[10]: "fp_avoidance_reasons",
    df.columns[11]: "received_counseling",
    df.columns[12]: "experienced_side_effects",
    df.columns[13]: "satisfaction_fp_info",
    df.columns[14]: "side_effects_details",
    df.columns[15]: "main_influencer",
    df.columns[16]: "community_acceptability",
    df.columns[17]: "fp_concerns",
}
df.rename(columns=rename_map, inplace=True)

qual_cols = ["fp_why", "husband_concerns", "side_effects_details", "fp_concerns"]
df[qual_cols].to_excel(OUTPUT_QUAL, index=False)
print(f"Saved qualitative columns → {OUTPUT_QUAL}")

df.drop(columns=qual_cols + ["fp_duration"], inplace=True)

df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["age_group"] = pd.cut(
    df["age"], bins=[15, 24, 34, 45], labels=["15-24", "25-34", "35-45"], right=True
)

edu_clean = {
    "None": "None",
    "none": "None",
    "Primary": "Primary",
    "Secondary": "Secondary",
    "Higher": "Higher",
}
df["education"] = df["education"].map(edu_clean)
df["education_code"] = df["education"].map(
    {"None": 1, "Primary": 2, "Secondary": 3, "Higher": 4}
)

standard_occ = {"Housewife", "Employed", "Student"}
df["occupation"] = df["occupation"].apply(
    lambda x: x.strip()
    if isinstance(x, str) and x.strip() in standard_occ
    else ("Other" if isinstance(x, str) else np.nan)
)

df["fp_use"] = df["fp_use"].str.strip().map({"Yes": 1, "No": 0})

df["husband_reaction_code"] = df["husband_reaction"].map(
    {"Supports it": 1, "Neutral": 2, "Does not know about it": 3, "Opposes it": 4}
)

df["received_counseling"] = (
    df["received_counseling"].str.strip().map({"Yes": 1, "No": 0})
)
df["experienced_side_effects"] = (
    df["experienced_side_effects"].str.strip().map({"Yes": 1, "No": 0})
)

df["satisfaction_code"] = df["satisfaction_fp_info"].map(
    {
        "Very dissatisfied": 1,
        "Dissatisfied": 2,
        "Neutral": 3,
        "Satisfied": 4,
        "Very satisfied": 5,
    }
)

df["community_acceptability_code"] = df["community_acceptability"].map(
    {"Not acceptable": 1, "Not sure": 2, "Somewhat acceptable": 3, "Very acceptable": 4}
)

standard_methods = {"Condoms", "Pills", "Injectables", "IUD", "Implants"}
method_options = {
    "method_condoms": "Condoms",
    "method_pills": "Pills",
    "method_injectables": "Injectables",
    "method_iud": "IUD",
    "method_implants": "Implants",
}
for col_name, keyword in method_options.items():
    df[col_name] = df["fp_method"].apply(
        lambda x: 1 if isinstance(x, str) and keyword in x else 0
    )
df["method_other"] = df["fp_method"].apply(
    lambda x: 1
    if isinstance(x, str)
    and any(m.strip() not in standard_methods for m in x.split(","))
    else 0
)


def multi_match(val, keywords):
    if not isinstance(val, str):
        return 0
    if isinstance(keywords, str):
        keywords = [keywords]
    return 1 if any(kw.lower() in val.lower() for kw in keywords) else 0


encourage_map = {
    "enc_hw_advice": "Health worker advice",
    "enc_work": "Work",
    "enc_health_risk": ["Concern about health risks", "High risk frequent pregnancies"],
    "enc_education": ["Education about family planning", "I am studying", "Studding"],
    "enc_husband_support": "Husband/partner support",
    "enc_friends": "Influence from friends or relatives",
    "enc_access": "Access to services",
    "enc_economic": "Economic reasons",
}
for col_name, keywords in encourage_map.items():
    df[col_name] = df["fp_encouragement"].apply(lambda x: multi_match(x, keywords))

avoid_map = {
    "avoid_more_children": "Desire for more children",
    "avoid_side_effects": "Fear of side effects",
    "avoid_husband": "Husband/partner disapproval",
    "avoid_religion": "Religious or cultural beliefs",
    "avoid_no_knowledge": ["Lack of knowledge", "Studding"],
    "avoid_bad_exp": "Previous negative experience",
    "avoid_no_access": "Lack of access to services",
}
for col_name, keywords in avoid_map.items():
    df[col_name] = df["fp_avoidance_reasons"].apply(lambda x: multi_match(x, keywords))

enc_cols = [c for c in df.columns if c.startswith("enc_")]
avoid_cols = [c for c in df.columns if c.startswith("avoid_")]
df["total_encouragement_factors"] = df[enc_cols].sum(axis=1)
df["total_avoidance_reasons"] = df[avoid_cols].sum(axis=1)

df.drop(columns=["fp_method", "fp_encouragement", "fp_avoidance_reasons"], inplace=True)

df.to_excel(OUTPUT_QUANT, index=False)
print(f"Saved cleaned dataset → {OUTPUT_QUANT}")
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"FP use prevalence: {df['fp_use'].mean() * 100:.1f}%")
