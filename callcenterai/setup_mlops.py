"""
Script de setup rapide pour Phase 5 - MLOps
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} - OK")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ERREUR")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║        🚀 Setup Phase 5 - MLOps CallCenterAI            ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # 1. Installation des dépendances
    print("\n📦 ÉTAPE 1 : Installation des dépendances MLOps")
    run_command(
        f"{sys.executable} -m pip install -r requirements-mlops.txt",
        "Installation DVC, MLflow, pytest..."
    )
    
    # 2. Initialisation DVC
    print("\n🔧 ÉTAPE 2 : Initialisation DVC")
    if not Path('.dvc').exists():
        run_command("dvc init", "Initialisation DVC")
    else:
        print("✅ DVC déjà initialisé")
    
    # 3. Vérification des fichiers
    print("\n📋 ÉTAPE 3 : Vérification des fichiers")
    
    required_files = [
        ('dvc.yaml', 'Pipeline DVC'),
        ('params.yaml', 'Paramètres DVC'),
        ('.github/workflows/ci-cd.yml', 'Workflow CI/CD'),
        ('scripts/prepare_data.py', 'Script de préparation'),
        ('scripts/train_tfidf.py', 'Script d\'entraînement'),
        ('scripts/mlflow_registry.py', 'Model Registry'),
    ]
    
    all_ok = True
    for file_path, description in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - MANQUANT")
            all_ok = False
    
    # 4. Tests
    print("\n🧪 ÉTAPE 4 : Exécution des tests")
    run_command(
        f"{sys.executable} -m pytest tests/ -v",
        "Tests unitaires"
    )
    
    # 5. Instructions finales
    print("""
    
╔══════════════════════════════════════════════════════════╗
║               ✅ Setup Terminé !                         ║
╚══════════════════════════════════════════════════════════╝

📚 PROCHAINES ÉTAPES :

1️⃣  Lancer MLflow UI :
   mlflow server --backend-store-uri sqlite:///mlflow.db --port 5000
   Accès : http://localhost:5000

2️⃣  Exécuter le pipeline DVC :
   dvc repro

3️⃣  Enregistrer le modèle dans MLflow :
   python scripts/mlflow_registry.py register

4️⃣  Promouvoir en Production :
   python scripts/mlflow_registry.py production

5️⃣  Pousser sur GitHub (déclenche CI/CD) :
   git add .
   git commit -m "✨ Phase 5 MLOps complète"
   git push origin main

📖 Documentation complète : MLOPS_GUIDE.md
    """)

if __name__ == "__main__":
    main()
