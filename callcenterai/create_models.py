"""
Script pour créer et entraîner les modèles CallCenterAI
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib
import os
from datetime import datetime

def create_sample_data():
    """Créer des données d'exemple pour l'entraînement"""
    
    # Données d'exemple pour classification de tickets
    data = {
        'text': [
            # Facturation
            "Ma facture est incorrecte", "Je conteste ma facture", "Erreur de facturation",
            "Le montant facturé ne correspond pas", "Problème avec ma facture mensuelle",
            "Je n'ai pas reçu ma facture", "Facture trop élevée", "Remboursement demandé",
            "Erreur sur la facture", "Facture en double", "Montant incorrect facturé",
            
            # Technique  
            "Je n'arrive pas à me connecter", "L'application plante", "Erreur technique",
            "Le site ne fonctionne pas", "Problème de connexion internet", "Bug dans l'app",
            "L'interface ne répond plus", "Erreur 404", "Problème technique majeur",
            "Le système est lent", "Dysfonctionnement de l'application", "Problème serveur",
            
            # Support/Aide
            "J'ai besoin d'aide", "Comment utiliser le service", "Aide pour configurer",
            "Je suis perdu", "Pouvez-vous m'aider", "Information sur le service",
            "Guide d'utilisation", "Support client", "Assistance nécessaire",
            "Comment faire pour", "Besoin d'explication", "Aide configuration",
            
            # Commercial
            "Je veux changer d'offre", "Information sur les tarifs", "Nouvelle souscription",
            "Upgrade de mon compte", "Offre premium", "Changement de forfait",
            "Devis pour entreprise", "Tarifs professionnels", "Souscription nouvelle offre",
            "Résiliation de contrat", "Modification contrat", "Offres disponibles"
        ],
        'category': [
            # Facturation (12)
            'facturation', 'facturation', 'facturation', 'facturation', 'facturation',
            'facturation', 'facturation', 'facturation', 'facturation', 'facturation',
            'facturation',
            
            # Technique (12) 
            'technique', 'technique', 'technique', 'technique', 'technique', 'technique',
            'technique', 'technique', 'technique', 'technique', 'technique', 'technique',
            
            # Support (12)
            'support', 'support', 'support', 'support', 'support', 'support',
            'support', 'support', 'support', 'support', 'support', 'support',
            
            # Commercial (12)
            'commercial', 'commercial', 'commercial', 'commercial', 'commercial', 'commercial',
            'commercial', 'commercial', 'commercial', 'commercial', 'commercial', 'commercial'
        ]
    }
    
    return pd.DataFrame(data)

def train_tfidf_model():
    """Entraîner le modèle TF-IDF + SVM"""
    
    print("🤖 Entraînement du modèle TF-IDF + SVM...")
    
    # Créer les données
    df = create_sample_data()
    print(f"📊 {len(df)} échantillons créés")
    print(f"📋 Catégories: {df['category'].unique()}")
    
    # Séparer les données
    X = df['text']
    y = df['category']
    
    # Créer le pipeline TF-IDF + SVM
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
        ('svm', SVC(kernel='linear', C=1.0, probability=True, random_state=42))
    ])
    
    # Entraîner le modèle
    pipeline.fit(X, y)
    
    # Évaluer rapidement
    train_score = pipeline.score(X, y)
    print(f"📈 Score d'entraînement: {train_score:.4f} ({train_score*100:.2f}%)")
    
    # Créer le dossier de modèles s'il n'existe pas
    os.makedirs('models', exist_ok=True)
    
    # Sauvegarder le modèle
    model_path = 'models/ticket_classifier_model.pkl'
    joblib.dump(pipeline, model_path)
    print(f"💾 Modèle sauvegardé: {model_path}")
    
    # Tester quelques prédictions
    test_texts = [
        "Ma facture est incorrecte",
        "Je n'arrive pas à me connecter", 
        "J'ai besoin d'aide",
        "Je veux changer d'offre"
    ]
    
    print(f"\n🧪 Tests de prédiction:")
    for text in test_texts:
        prediction = pipeline.predict([text])[0]
        proba = pipeline.predict_proba([text])[0]
        confidence = np.max(proba)
        print(f"  '{text}' → {prediction} ({confidence:.3f})")
    
    return pipeline

def create_vectorizer_and_model():
    """Créer le vectorizer et le modèle séparément (format attendu par le service)"""
    
    print("\n🔧 Création des composants séparés...")
    
    # Créer les données
    df = create_sample_data()
    X = df['text']
    y = df['category']
    
    # Créer et entraîner le vectorizer
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_vectorized = vectorizer.fit_transform(X)
    
    # Créer et entraîner le modèle SVM
    model = SVC(kernel='linear', C=1.0, probability=True, random_state=42)
    model.fit(X_vectorized, y)
    
    # Sauvegarder séparément
    os.makedirs('models', exist_ok=True)
    
    vectorizer_path = 'models/tfidf_vectorizer.pkl'
    model_path = 'models/svm_model.pkl'
    
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(model, model_path)
    
    print(f"💾 Vectorizer sauvegardé: {vectorizer_path}")
    print(f"💾 Modèle SVM sauvegardé: {model_path}")
    
    return vectorizer, model

def create_training_info():
    """Créer un fichier d'information sur l'entraînement"""
    
    info = {
        'model_type': 'TF-IDF + SVM',
        'training_date': datetime.now().isoformat(),
        'num_samples': len(create_sample_data()),
        'categories': ['facturation', 'technique', 'support', 'commercial'],
        'vectorizer_params': {
            'max_features': 5000,
            'stop_words': 'english'
        },
        'svm_params': {
            'kernel': 'linear',
            'C': 1.0,
            'probability': True,
            'random_state': 42
        }
    }
    
    import json
    with open('models/training_info.json', 'w') as f:
        json.dump(info, f, indent=2)
    
    print(f"📋 Informations d'entraînement sauvegardées: models/training_info.json")

def main():
    """Fonction principale"""
    
    print("🏗️ CRÉATION DES MODÈLES CALLCENTERAI")
    print("=====================================")
    
    try:
        # Entraîner le modèle complet
        pipeline = train_tfidf_model()
        
        # Créer les composants séparés
        vectorizer, model = create_vectorizer_and_model()
        
        # Créer les informations d'entraînement
        create_training_info()
        
        print(f"\n🎉 MODÈLES CRÉÉS AVEC SUCCÈS!")
        print(f"================================")
        print(f"📁 Fichiers créés dans le dossier 'models/':")
        print(f"  • ticket_classifier_model.pkl (pipeline complet)")
        print(f"  • tfidf_vectorizer.pkl (vectorizer)")
        print(f"  • svm_model.pkl (modèle SVM)")
        print(f"  • training_info.json (informations)")
        
        print(f"\n🚀 Vous pouvez maintenant lancer les services!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des modèles: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()