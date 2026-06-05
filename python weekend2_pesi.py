import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- load file ---
df = pd.read_csv(
    "AI_SCORING.csv",
    sep=";",
    decimal=","
)

companies = df["company"].tolist()
dims = ["material", "mobility", "king_safety", "center_control", "passed_pawns", "piece_coordination"]
scores = df[dims].values.astype(float)

# --- chess weights ---
chess_weights = {
    "material":           0.05,
    "mobility":           0.25,
    "king_safety":        0.10,
    "center_control":     0.25,
    "passed_pawns":       0.20,
    "piece_coordination": 0.15,
}

# --- business weights ---
business_weights = {
    "material":           0.25,
    "mobility":           0.10,
    "king_safety":        0.20,
    "center_control":     0.20,
    "passed_pawns":       0.05,
    "piece_coordination": 0.20,
}

def compute_total(scores, weights, dims):
    w = np.array([weights[d] for d in dims])
    return np.round(scores @ w, 2)

total_chess    = compute_total(scores, chess_weights,    dims)
total_business = compute_total(scores, business_weights, dims)

# --- print rankings ---
print("=" * 45)
print("CHESS RANKING")
print("=" * 45)
for i, j in enumerate(np.argsort(total_chess)[::-1]):
    print(f"  {i+1}. {companies[j]:<20} {total_chess[j]:.2f}")

print()
print("=" * 45)
print("BUSINESS RANKING")
print("=" * 45)
for i, j in enumerate(np.argsort(total_business)[::-1]):
    print(f"  {i+1}. {companies[j]:<20} {total_business[j]:.2f}")

print()
print("=" * 45)
print("CONVERGENCE MAP")
print("=" * 45)
print(f"{'Company':<20} {'Chess':>8} {'Business':>9} {'Delta':>7}")
print("-" * 45)
for i, c in enumerate(companies):
    delta = round(total_chess[i] - total_business[i], 2)
    sign = "+" if delta > 0 else ""
    print(f"{c:<20} {total_chess[i]:>8.2f} {total_business[i]:>9.2f} {sign+str(delta):>7}")

# --- dual radar chart ---
labels = ["Material", "Mobility", "King safety", "Center ctrl", "Passed pawns", "Coordination"]
N = len(labels)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]

colors = ["#378ADD","#1D9E75","#D85A30","#7F77DD","#EF9F27","#888780","#D4537E"]

fig, axes = plt.subplots(1, 2, figsize=(14, 6), subplot_kw=dict(polar=True))
titles   = ["Chess perspective", "Business perspective"]
weights_list = [chess_weights, business_weights]

for ax, title, weights in zip(axes, titles, weights_list):
    ax.set_title(title, size=13, pad=15, fontweight="bold")
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2","4","6","8","10"], size=8, color="gray")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=9)
    ax.grid(color="gray", alpha=0.3)

    for company, row, color in zip(companies, scores, colors):
        vals = row.tolist() + [row[0]]
        ax.plot(angles, vals, color=color, linewidth=1.8, label=company)
        ax.fill(angles, vals, color=color, alpha=0.04)

axes[0].legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=9)
plt.tight_layout()
plt.savefig("radar_weekend2.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nChart saved as radar_weekend2.png")