# src/visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_clean_data(file_path='data/raw/cards.csv'):
    # Load the card data with the right encoding
    df = pd.read_csv(file_path, encoding='latin1')
    
    # Focus on minion cards only
    df_minions = df[df['type'].str.lower() == 'minion'].copy()
    
    # Turn cost, attack, and health into numbers, skip bad ones
    df_minions['cost'] = pd.to_numeric(df_minions['cost'], errors='coerce')
    df_minions['attack'] = pd.to_numeric(df_minions['attack'], errors='coerce')
    df_minions['health'] = pd.to_numeric(df_minions['health'], errors='coerce')
    
    # Remove rows with missing numbers
    df_minions = df_minions.dropna(subset=['cost', 'attack', 'health'])
    
    # Remove weird cards (too strong or test ones)
    df_minions = df_minions[(df_minions['cost'] <= 10) & 
                           (df_minions['health'] <= 15) & 
                           (df_minions['cost'] > 0)]
    df_minions = df_minions[~df_minions['name'].str.contains('Test|Cheat', case=False, na=False)]
    
    # Remove duplicates
    df_minions = df_minions.drop_duplicates(subset=['name', 'cost', 'attack', 'health'])
    return df_minions

def plot_attack_vs_cost(df_minions, output_path='outputs/figures/attack_vs_cost.png'):
    # Set up the graph size
    plt.figure(figsize=(12, 8))
    
    # Pick colors that work for dark or light screens
    palette = sns.color_palette("husl", n_colors=len(df_minions['playerClass'].unique()))
    
    # Make a scatter plot: cost vs attack, colored by class, size by health
    sns.scatterplot(data=df_minions, x='cost', y='attack', hue='playerClass', 
                    size='health', sizes=(50, 300), alpha=0.7, palette=palette)
    
    # Add a line for balanced cards (attack = cost)
    plt.axline((0, 1), slope=1, color='black', linestyle='--', linewidth=2, 
               label='Balanced Line (Attack ≈ Cost)')
    
    # Label the graph
    plt.xlabel('Mana Cost', fontsize=14)
    plt.ylabel('Attack', fontsize=14)
    plt.title('Hearthstone Minions: Attack vs. Cost by Class', fontsize=16)
    
    # Add a legend and grid
    plt.legend(title='Player Class', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle=':', alpha=0.7)
    
    # Save the graph and show it
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Load and clean the data
    df_minions = load_and_clean_data()
    
    # Make and save the graph
    plot_attack_vs_cost(df_minions)
