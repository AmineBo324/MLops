"""
Script de préparation des données pour DVC pipeline
"""
import pandas as pd
import yaml
import json
from pathlib import Path
from sklearn.model_selection import train_test_split

# Charger les paramètres
with open('params.yaml', 'r') as f:
    params = yaml.safe_load(f)

prepare_params = params['prepare']

# Créer les dossiers si nécessaire
Path('data/processed').mkdir(parents=True, exist_ok=True)

# Charger les données
print("📥 Chargement des données brutes...")
df = pd.read_csv('../all_tickets_processed_improved_v3.csv')

# Nettoyage basique
print("🧹 Nettoyage des données...")
df = df.dropna(subset=['text', 'category'])
df = df[df['text'].str.len() >= prepare_params['min_text_length']]
df = df[df['text'].str.len() <= prepare_params['max_text_length']]

# Split train/test
print("✂️ Séparation train/test...")
train_df, test_df = train_test_split(
    df,
    test_size=prepare_params['test_size'],
    random_state=prepare_params['random_state'],
    stratify=df['category']
)

# Sauvegarder
train_df.to_csv('data/processed/train.csv', index=False)
test_df.to_csv('data/processed/test.csv', index=False)

# Statistiques
stats = {
    'total_samples': len(df),
    'train_samples': len(train_df),
    'test_samples': len(test_df),
    'num_categories': df['category'].nunique(),
    'categories': df['category'].value_counts().to_dict(),
    'avg_text_length': float(df['text'].str.len().mean()),
    'test_size': prepare_params['test_size']
}

with open('data/processed/data_stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print(f"✅ Préparation terminée !")
print(f"   Train: {len(train_df)} échantillons")
print(f"   Test: {len(test_df)} échantillons")
print(f"   Catégories: {df['category'].nunique()}")
