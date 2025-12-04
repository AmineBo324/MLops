"""
Script de gestion du MLflow Model Registry
Enregistre et promeut les modèles entre Staging et Production
"""
import mlflow
from mlflow.tracking import MlflowClient

# Configuration
TRACKING_URI = "http://localhost:5000"
MODEL_NAME = "callcenterai-tfidf-classifier"

mlflow.set_tracking_uri(TRACKING_URI)
client = MlflowClient()

def register_best_model():
    """Enregistre le meilleur modèle dans le registry"""
    print("🔍 Recherche du meilleur modèle...")
    
    # Récupérer l'expérience
    experiment = client.get_experiment_by_name("callcenterai-tfidf-classification")
    if not experiment:
        print("❌ Aucune expérience trouvée")
        return
    
    # Récupérer les runs triés par test_accuracy
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.test_accuracy DESC"],
        max_results=1
    )
    
    if not runs:
        print("❌ Aucun run trouvé")
        return
    
    best_run = runs[0]
    run_id = best_run.info.run_id
    test_accuracy = best_run.data.metrics.get('test_accuracy', 0)
    
    print(f"✅ Meilleur modèle trouvé:")
    print(f"   Run ID: {run_id}")
    print(f"   Test Accuracy: {test_accuracy:.4f}")
    
    # Enregistrer le modèle
    model_uri = f"runs:/{run_id}/model"
    
    try:
        # Vérifier si le modèle existe déjà
        try:
            client.get_registered_model(MODEL_NAME)
            print(f"📦 Modèle '{MODEL_NAME}' existe déjà")
        except:
            # Créer le modèle
            client.create_registered_model(
                MODEL_NAME,
                description="Modèle TF-IDF + SVM pour classification de tickets call center"
            )
            print(f"📦 Modèle '{MODEL_NAME}' créé")
        
        # Enregistrer la nouvelle version
        model_version = client.create_model_version(
            name=MODEL_NAME,
            source=model_uri,
            run_id=run_id,
            description=f"Version avec accuracy={test_accuracy:.4f}"
        )
        
        version_number = model_version.version
        print(f"✅ Version {version_number} enregistrée")
        
        return version_number
        
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement: {e}")
        return None

def promote_to_staging(version=None):
    """Promouvoir un modèle en Staging"""
    if version is None:
        # Récupérer la dernière version
        model_versions = client.search_model_versions(f"name='{MODEL_NAME}'")
        if not model_versions:
            print("❌ Aucune version trouvée")
            return
        version = model_versions[0].version
    
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=version,
        stage="Staging"
    )
    print(f"🔄 Version {version} promue en Staging")

def promote_to_production(version=None):
    """Promouvoir un modèle en Production"""
    if version is None:
        # Récupérer la version en Staging
        versions = client.get_latest_versions(MODEL_NAME, stages=["Staging"])
        if not versions:
            print("❌ Aucun modèle en Staging")
            return
        version = versions[0].version
    
    # Archiver l'ancienne version en Production
    prod_versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
    for pv in prod_versions:
        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=pv.version,
            stage="Archived"
        )
        print(f"📦 Version {pv.version} archivée")
    
    # Promouvoir en Production
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=version,
        stage="Production"
    )
    print(f"🚀 Version {version} promue en Production")

def list_models():
    """Lister tous les modèles et leurs versions"""
    print(f"\n📋 Modèles enregistrés:")
    try:
        model = client.get_registered_model(MODEL_NAME)
        print(f"\n🏷️  {MODEL_NAME}")
        print(f"   Description: {model.description}")
        
        versions = client.search_model_versions(f"name='{MODEL_NAME}'")
        for v in sorted(versions, key=lambda x: int(x.version), reverse=True):
            print(f"\n   Version {v.version} - Stage: {v.current_stage}")
            print(f"   Run ID: {v.run_id}")
            print(f"   Created: {v.creation_timestamp}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python mlflow_registry.py register    # Enregistrer le meilleur modèle")
        print("  python mlflow_registry.py staging     # Promouvoir en Staging")
        print("  python mlflow_registry.py production  # Promouvoir en Production")
        print("  python mlflow_registry.py list        # Lister les modèles")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action == "register":
        version = register_best_model()
        if version:
            promote_to_staging(version)
    elif action == "staging":
        promote_to_staging()
    elif action == "production":
        promote_to_production()
    elif action == "list":
        list_models()
    else:
        print(f"❌ Action inconnue: {action}")
