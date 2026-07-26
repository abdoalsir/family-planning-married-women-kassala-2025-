"""
Project  : Family Planning Among Married Women of Reproductive Age
           in Kassala City, Sudan – 2025
Script   : Figure Generation (all figures)
Author   : Abdulrahman Sirelkhatim
Date     : March 2026
Input    : 1_data/cleaned/cleaned_data.xlsx
Output   : 5_figures/ directory (PNG, 300 DPI)

Figures produced:
    fig01_age_group_distribution.png
    fig02_education_distribution.png
    fig03_occupation_distribution.png
    fig04_fp_use_prevalence.png
    fig05_contraceptive_method_distribution.png
    fig06_husband_reaction_distribution.png
    fig07_community_acceptability.png
    fig08_encouragement_factors.png
    fig09_avoidance_reasons.png
    fig10_satisfaction_distribution.png
    fig11_fp_use_by_education.png
    fig12_fp_use_by_occupation.png
    fig13_fp_use_by_husband_reaction.png
    fig14_fp_use_by_community_acceptability.png
    fig15_fp_use_by_influencer.png
    fig16_fp_use_by_counseling.png
    fig17_logistic_regression_forest_plot.png
    fig18_satisfaction_vs_fp_use_boxplot.png
"""

import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

DATA_PATH = "1_data/cleaned/cleaned_data.xlsx"
FIGURES_DIR = "5_figures/"

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11
plt.rcParams["figure.dpi"] = 200

PALETTE = sns.color_palette("Set2")
BLUE = "#0077B6"
CONTRAST = [sns.color_palette("Set2")[0], sns.color_palette("Set2")[3]]


def save_fig(fig, filename):
    fig.savefig(FIGURES_DIR + filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {filename}")


def donut_pie(ax, counts, title):
    ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=PALETTE,
        wedgeprops={"width": 0.4, "edgecolor": "white"},
        pctdistance=0.5,
        labeldistance=1.05,
    )
    ax.set_title(title, pad=12)


def fp_prevalence_bar(col, label_map, order, title, filename, p_label="", rotate=0):
    dep = (
        (df.groupby(col)["fp_use"].mean() * 100)
        .rename(index=label_map)
        .reindex(order)
        .dropna()
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(dep.index, dep.values, color=PALETTE[: len(dep)])
    for bar in bars:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + 1,
            f"{h:.1f}%",
            ha="center",
            fontsize=9,
        )
    ax.set_ylabel("FP Use Prevalence (%)")
    ax.set_title(f"{title}\n{p_label}")
    ax.set_ylim(0, 110)
    ax.tick_params(axis="x", rotation=rotate)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    save_fig(fig, filename)


df = pd.read_excel(DATA_PATH)
n = len(df)

# --- Figures 1–3: Demographic distributions ---
fig, ax = plt.subplots(figsize=(5, 5))
counts = df["age_group"].value_counts().reindex(["15-24", "25-34", "35-45"]).dropna()
donut_pie(ax, counts, f"Age Group Distribution (N={n})")
save_fig(fig, "fig01_age_group_distribution.png")

fig, ax = plt.subplots(figsize=(5, 5))
counts = (
    df["education"]
    .value_counts()
    .reindex(["None", "Primary", "Secondary", "Higher"])
    .dropna()
)
donut_pie(ax, counts, f"Education Level (N={n})")
save_fig(fig, "fig02_education_distribution.png")

fig, ax = plt.subplots(figsize=(5, 5))
counts = df["occupation"].value_counts()
donut_pie(ax, counts, f"Occupation Distribution (N={n})")
save_fig(fig, "fig03_occupation_distribution.png")

# --- Figure 4: FP use prevalence ---
fig, ax = plt.subplots(figsize=(5, 5))
counts = df["fp_use"].map({1: "Currently Using", 0: "Not Using"}).value_counts()
ax.pie(
    counts,
    labels=counts.index,
    autopct="%1.1f%%",
    colors=CONTRAST,
    wedgeprops={"width": 0.4, "edgecolor": "white"},
    pctdistance=0.5,
    labeldistance=1.05,
)
ax.set_title(f"Family Planning Use Prevalence (N={n})")
save_fig(fig, "fig04_fp_use_prevalence.png")

# --- Figure 5: Contraceptive method distribution (users only) ---
method_cols = {
    "method_pills": "Pills",
    "method_injectables": "Injectables",
    "method_implants": "Implants",
    "method_other": "Other",
    "method_iud": "IUD",
    "method_condoms": "Condoms",
}
users = df[df["fp_use"] == 1]
method_pcts = {label: users[col].mean() * 100 for col, label in method_cols.items()}
method_pcts = dict(sorted(method_pcts.items(), key=lambda x: x[1], reverse=True))

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(
    list(method_pcts.keys()),
    list(method_pcts.values()),
    color=PALETTE[: len(method_pcts)],
)
for bar in bars:
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2, h + 0.5, f"{h:.1f}%", ha="center", fontsize=9
    )
ax.set_ylabel("% of Current Users")
ax.set_title(f"Contraceptive Method Distribution — Current Users (n={len(users)})")
ax.set_ylim(0, 45)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig05_contraceptive_method_distribution.png")

# --- Figure 6: Husband reaction ---
fig, ax = plt.subplots(figsize=(5, 5))
hr_labels = {1: "Supports", 2: "Neutral", 3: "Does Not Know", 4: "Opposes"}
counts = df["husband_reaction_code"].map(hr_labels).value_counts()
donut_pie(ax, counts, f"Husband's Reaction to FP (N={n})")
save_fig(fig, "fig06_husband_reaction_distribution.png")

# --- Figure 7: Community acceptability ---
fig, ax = plt.subplots(figsize=(5, 5))
ca_order = ["Not acceptable", "Not sure", "Somewhat acceptable", "Very acceptable"]
counts = df["community_acceptability"].value_counts().reindex(ca_order).dropna()
donut_pie(ax, counts, f"Community Acceptability of FP (N={n})")
save_fig(fig, "fig07_community_acceptability.png")

# --- Figure 8: Encouragement factors ---
enc_cols = [c for c in df.columns if c.startswith("enc_")]
enc_labels = {
    "enc_hw_advice": "Health worker advice",
    "enc_work": "Work obligations",
    "enc_education": "Education/Study",
    "enc_health_risk": "Health risk concern",
    "enc_husband_support": "Husband/partner support",
    "enc_friends": "Friends/relatives influence",
    "enc_access": "Access to services",
    "enc_economic": "Economic reasons",
}
enc_pcts = {enc_labels.get(c, c): df[c].mean() * 100 for c in enc_cols}
enc_pcts = dict(sorted(enc_pcts.items(), key=lambda x: x[1]))

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(list(enc_pcts.keys()), list(enc_pcts.values()), color=BLUE)
for bar in bars:
    w = bar.get_width()
    ax.text(
        w + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{w:.1f}%",
        va="center",
        fontsize=9,
    )
ax.set_xlabel("% of All Participants (N=384)")
ax.set_title(f"Factors Encouraging FP Use (N={n})")
ax.set_xlim(0, 90)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig08_encouragement_factors.png")

# --- Figure 9: Avoidance reasons (non-users only) ---
avoid_cols = [c for c in df.columns if c.startswith("avoid_")]
avoid_labels = {
    "avoid_more_children": "Desire for more children",
    "avoid_side_effects": "Fear of side effects",
    "avoid_husband": "Husband disapproval",
    "avoid_religion": "Religious/cultural beliefs",
    "avoid_no_knowledge": "Lack of knowledge",
    "avoid_bad_exp": "Previous negative experience",
    "avoid_no_access": "Lack of access",
}
non_users = df[df["fp_use"] == 0]
avoid_pcts = {avoid_labels.get(c, c): non_users[c].mean() * 100 for c in avoid_cols}
avoid_pcts = dict(sorted(avoid_pcts.items(), key=lambda x: x[1]))

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(list(avoid_pcts.keys()), list(avoid_pcts.values()), color=BLUE)
for bar in bars:
    w = bar.get_width()
    ax.text(
        w + 0.3,
        bar.get_y() + bar.get_height() / 2,
        f"{w:.1f}%",
        va="center",
        fontsize=9,
    )
ax.set_xlabel(f"% of Non-Users (n={len(non_users)})")
ax.set_title(f"Reasons for Avoiding Family Planning — Non-Users (n={len(non_users)})")
ax.set_xlim(0, 40)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig09_avoidance_reasons.png")

# --- Figure 10: Satisfaction distribution ---
sat_order = [
    "Very dissatisfied",
    "Dissatisfied",
    "Neutral",
    "Satisfied",
    "Very satisfied",
]
fig, ax = plt.subplots(figsize=(7, 4))
counts = df["satisfaction_fp_info"].value_counts().reindex(sat_order).fillna(0)
bars = ax.bar(
    counts.index, counts.values / n * 100, color=sns.color_palette("RdYlGn", 5)
)
for bar in bars:
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2, h + 0.3, f"{h:.1f}%", ha="center", fontsize=9
    )
ax.set_ylabel("Percentage (%)")
ax.set_title(f"Satisfaction with FP Information (N={n})")
ax.tick_params(axis="x", rotation=20)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig10_satisfaction_distribution.png")

# --- Figures 11–16: FP use by categorical predictors ---
fp_prevalence_bar(
    "education_code",
    {1: "None", 2: "Primary", 3: "Secondary", 4: "Higher"},
    ["None", "Primary", "Secondary", "Higher"],
    f"FP Use by Education Level (N={n})",
    "fig11_fp_use_by_education.png",
    "χ²=9.818, p=0.020, V=0.160",
)

fp_prevalence_bar(
    "occupation",
    {o: o for o in ["Employed", "Student", "Housewife", "Other"]},
    ["Employed", "Student", "Housewife", "Other"],
    f"FP Use by Occupation (N={n})",
    "fig12_fp_use_by_occupation.png",
    "χ²=23.853, p<0.001, V=0.249",
)

fp_prevalence_bar(
    "husband_reaction_code",
    {1: "Supports", 2: "Neutral", 3: "Does Not Know", 4: "Opposes"},
    ["Supports", "Neutral", "Does Not Know", "Opposes"],
    f"FP Use by Husband's Reaction (N={n})",
    "fig13_fp_use_by_husband_reaction.png",
    "χ²=234.077, p<0.001, V=0.781",
)

fp_prevalence_bar(
    "community_acceptability",
    {
        ca: ca
        for ca in [
            "Not acceptable",
            "Not sure",
            "Somewhat acceptable",
            "Very acceptable",
        ]
    },
    ["Not acceptable", "Not sure", "Somewhat acceptable", "Very acceptable"],
    f"FP Use by Community Acceptability (N={n})",
    "fig14_fp_use_by_community_acceptability.png",
    "χ²=45.218, p<0.001, V=0.343",
    rotate=15,
)

fp_prevalence_bar(
    "main_influencer",
    {m: m for m in df["main_influencer"].unique() if pd.notna(m)},
    df["main_influencer"].value_counts().index.tolist(),
    f"FP Use by Main Decision Influencer (N={n})",
    "fig15_fp_use_by_influencer.png",
    "χ²=49.476, p<0.001, V=0.359",
    rotate=15,
)

fig, ax = plt.subplots(figsize=(5, 4))
dep_counseling = df.groupby("received_counseling")["fp_use"].mean() * 100
dep_counseling.index = dep_counseling.index.map(
    {0: "No Counseling", 1: "Received Counseling"}
)
bars = ax.bar(dep_counseling.index, dep_counseling.values, color=CONTRAST)
for bar in bars:
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2, h + 1, f"{h:.1f}%", ha="center", fontsize=10
    )
ax.set_ylabel("FP Use Prevalence (%)")
ax.set_title(f"FP Use by Health Worker Counseling (N={n})\nχ²=16.441, p<0.001, OR=4.58")
ax.set_ylim(0, 70)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig16_fp_use_by_counseling.png")


# --- Figure 17: Forest plot — logistic regression predictors ---
# OR and 95% CI from SPSS binary logistic regression output (Table 7 in results)
predictors = [
    "Education Level\n(per unit increase)",
    "Received Counseling\n(Yes vs No)",
    "Satisfaction with FP Info\n(per unit increase)",
    "Experienced Side Effects\n(Yes vs No)",
    "Community Acceptability\n(per unit increase)",
]
ors = [1.350, 3.171, 1.839, 1.243, 0.927]
ci_lower = [1.096, 1.360, 1.493, 0.744, 0.754]
ci_upper = [1.661, 7.393, 2.264, 2.078, 1.140]
p_vals = [0.005, 0.008, 0.001, 0.406, 0.472]

fig, ax = plt.subplots(figsize=(8, 5))
y_pos = np.arange(len(predictors))
colors = [BLUE if p < 0.05 else "#AAAAAA" for p in p_vals]
ax.errorbar(
    ors,
    y_pos,
    xerr=[np.array(ors) - np.array(ci_lower), np.array(ci_upper) - np.array(ors)],
    fmt="o",
    color=BLUE,
    capsize=5,
    markersize=7,
)
for i, (or_val, p, color) in enumerate(zip(ors, p_vals, colors)):
    p_text = f"p={p:.3f}" if p >= 0.001 else "p<0.001"
    ax.scatter(ors[i], i, color=color, zorder=5, s=60)
    ax.text(
        max(ci_upper[i], or_val) + 0.05,
        i,
        f"AOR={or_val:.3f}, {p_text}",
        va="center",
        fontsize=8,
    )
ax.axvline(1, color="red", linestyle="--", linewidth=1)
ax.set_yticks(y_pos)
ax.set_yticklabels(predictors, fontsize=9)
ax.set_xlabel("Adjusted Odds Ratio (95% CI)")
ax.set_title(
    f"Predictors of FP Use — Binary Logistic Regression (N={n})\n"
    "Nagelkerke R²=0.208 | Blue = significant, Grey = non-significant"
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig17_logistic_regression_forest_plot.png")


# --- Figure 18: Satisfaction score by FP use (boxplot) ---
fig, ax = plt.subplots(figsize=(5, 4))
groups = [
    df.loc[df["fp_use"] == 0, "satisfaction_code"].dropna(),
    df.loc[df["fp_use"] == 1, "satisfaction_code"].dropna(),
]
ax.boxplot(
    groups,
    labels=["Non-Users", "Current Users"],
    patch_artist=True,
    boxprops=dict(facecolor="steelblue", alpha=0.6),
)
ax.set_ylabel("Satisfaction Score (1=Very Dissatisfied → 5=Very Satisfied)")
ax.set_title("Satisfaction with FP Info by Use Status\nSpearman ρ=0.330, p<0.001")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save_fig(fig, "fig18_satisfaction_vs_fp_use_boxplot.png")

print(f"\nAll figures saved to: {FIGURES_DIR}")
