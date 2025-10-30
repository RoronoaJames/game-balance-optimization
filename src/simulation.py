import pandas as pd
import numpy as np

# -------------------------------------------------
# 1. Load & clean data
# -------------------------------------------------
df = pd.read_csv('data/raw/cards.csv', encoding='latin1')
df_minions = df[df['type'].str.lower() == 'minion'].copy()
for col in ['cost', 'attack', 'health']:
    df_minions[col] = pd.to_numeric(df_minions[col], errors='coerce')
df_minions = df_minions.dropna(subset=['cost', 'attack', 'health'])
df_minions = df_minions[(df_minions['cost'] <= 10) & (df_minions['health'] <= 15) & (df_minions['cost'] > 0)]

print("Card Count by Class:")
print(df_minions['playerClass'].value_counts())

# -------------------------------------------------
# 2. Match simulation
# -------------------------------------------------
def simulate_match(deck1, deck2):
    power1 = (deck1['attack'] * 0.6 + deck1['health'] * 0.4).sum()
    power2 = (deck2['attack'] * 0.6 + deck2['health'] * 0.4).sum()
    return 1 if power1 > power2 else 0

# -------------------------------------------------
# 3. Run many matches + **fair weighting**
# -------------------------------------------------
num_matches = 500
class_counts = df_minions['playerClass'].value_counts()
max_cards   = class_counts.max()                 # 758 (NEUTRAL)
wins = {cls: 0.0 for cls in class_counts.index}

for _ in range(num_matches):
    deck1 = df_minions.sample(n=5)
    deck2 = df_minions.sample(n=5)
    winner = simulate_match(deck1, deck2)

    # Give every *unique* class in the winning deck a weighted point
    winning_deck = deck1 if winner == 1 else deck2
    for cls in winning_deck['playerClass'].dropna().unique():
        weight = max_cards / class_counts[cls]      # rare classes get BIG boost
        wins[cls] += weight / 5.0                  # split across 5 cards

# -------------------------------------------------
# 4. Normalise to win-rates (0-1)
# -------------------------------------------------
total_weighted = sum(wins.values())
win_rates = {cls: wins[cls] / total_weighted for cls in wins}

print("\nWin Rates by Class:")
for cls, rate in sorted(win_rates.items(), key=lambda x: -x[1]):
    print(f"{cls:8}: {rate:.4f}")

# -------------------------------------------------
# 5. Jain’s fairness index (higher = fairer)
# -------------------------------------------------
rates = np.array(list(win_rates.values()))
jain = (rates.sum()**2) / (len(rates) * (rates**2).sum())
print(f"\nJain Fairness Index: {jain:.4f}  (1.0 = perfect)")

# -------------------------------------------------
# 6. Simple variance (lower = fairer)
# -------------------------------------------------
variance = np.var(rates)
print(f"Variance of win-rates: {variance:.6f}")
