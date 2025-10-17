import pandas as pd

# Load your card data
df = pd.read_csv('data/raw/cards.csv', encoding='latin1')
df_minions = df[df['type'].str.lower() == 'minion'].copy()
df_minions['cost'] = pd.to_numeric(df_minions['cost'], errors='coerce')
df_minions['attack'] = pd.to_numeric(df_minions['attack'], errors='coerce')
df_minions['health'] = pd.to_numeric(df_minions['health'], errors='coerce')
df_minions = df_minions.dropna(subset=['cost', 'attack', 'health'])
df_minions = df_minions[(df_minions['cost'] <= 10) & (df_minions['health'] <= 15) & (df_minions['cost'] > 0)]

# Simple game test
print("Testing 10 random card matches...")
total_wins = 0
for i in range(10):
    deck1 = df_minions.sample(n=5)['attack'].sum()
    deck2 = df_minions.sample(n=5)['attack'].sum()
    if deck1 > deck2:
        total_wins += 1
    print(f"Match {i+1}: Deck1={deck1:.1f} vs Deck2={deck2:.1f}, Win rate so far: {total_wins/(i+1):.2f}")
print(f"\nFinal Win Rate: {total_wins/10:.2f} (should be close to 0.5 for balance)")
