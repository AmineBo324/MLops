# 🚀 Phase 5 : MLOps - Guide Complet

## 📋 Vue d'ensemble

Cette phase implémente les pratiques MLOps avec :
- **DVC** : Pipeline de données et versioning
- **MLflow** : Tracking d'expériences et Model Registry
- **CI/CD** : GitHub Actions avec tests, build Docker et scan sécurité

## 1️⃣ DVC (Data Version Control)

### Installation
```bash
pip install dvc mlflow pyyaml
```

### Initialisation
```bash
cd callcenterai
dvc init
```

### Configuration du Remote Storage (optionnel)
```bash
# Exemple avec Google Drive
dvc remote add -d storage gdrive://your-folder-id

# Exemple avec S3
dvc remote add -d storage s3://your-bucket/path
```

### Exécution du Pipeline
```bash
# Exécuter tout le pipeline
dvc repro

# Exécuter un stage spécifique
dvc repro train_tfidf

# Visualiser le pipeline
dvc dag
```

### Métriques et Plots
```bash
# Afficher les métriques
dvc metrics show

# Comparer les métriques entre branches
dvc metrics diff

# Afficher les plots
dvc plots show models/confusion_matrix.csv
```

## 2️⃣ MLflow

### Démarrage du serveur MLflow
```bash
# Terminal 1 : Lancer MLflow UI
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5000
```

Accès : http://localhost:5000

### Tracking des expériences

Le tracking est automatiquement intégré dans `scripts/train_tfidf.py` :
```python
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("callcenterai-tfidf-classification")

with mlflow.start_run():
    mlflow.log_params(params)
    mlflow.log_metrics(metrics)
    mlflow.sklearn.log_model(model, "model")
```

### Model Registry

```bash
# Enregistrer le meilleur modèle
python scripts/mlflow_registry.py register

# Promouvoir en Staging
python scripts/mlflow_registry.py staging

# Promouvoir en Production
python scripts/mlflow_registry.py production

# Lister les modèles
python scripts/mlflow_registry.py list
```

### Charger un modèle depuis le Registry
```python
import mlflow.sklearn

# Charger depuis Production
model = mlflow.sklearn.load_model(
    f"models:/callcenterai-tfidf-classifier/Production"
)

# Charger depuis Staging
model = mlflow.sklearn.load_model(
    f"models:/callcenterai-tfidf-classifier/Staging"
)
```

## 3️⃣ CI/CD avec GitHub Actions

### Workflow `.github/workflows/ci-cd.yml`

Le workflow s'exécute automatiquement sur :
- Push sur `main` ou `develop`
- Pull Request vers `main`

### Jobs du Pipeline

1. **🔍 Lint & Tests**
   - Black (formatage)
   - Flake8 (linting)
   - Pytest (tests unitaires)
   - Coverage report

2. **🔒 Security Scan**
   - Bandit (analyse sécurité Python)
   - Safety (vulnérabilités dépendances)

3. **🐳 Build & Push Docker**
   - Build des 4 services (tfidf, transformer, agent, web)
   - Push vers GitHub Container Registry
   - Trivy scan (vulnérabilités images)

4. **🚀 Deploy Staging**
   - Déploiement automatique en staging

### Configuration requise

#### Secrets GitHub
Aucun secret supplémentaire requis pour le registry GitHub (utilise `GITHUB_TOKEN`).

Pour d'autres registries :
```yaml
Settings → Secrets → Actions → New repository secret
- DOCKER_USERNAME
- DOCKER_PASSWORD
```

### Lancer localement

```bash
# Installer act (pour tester GitHub Actions en local)
choco install act  # Windows

# Exécuter le workflow
act push
```

## 4️⃣ Workflow Complet

### Développement local
```bash
# 1. Modifier les paramètres
nano params.yaml

# 2. Lancer MLflow
mlflow server --backend-store-uri sqlite:///mlflow.db --port 5000

# 3. Exécuter le pipeline DVC
dvc repro

# 4. Visualiser les résultats
mlflow ui  # http://localhost:5000
dvc metrics show
dvc plots show

# 5. Enregistrer le modèle
python scripts/mlflow_registry.py register

# 6. Promouvoir en Production
python scripts/mlflow_registry.py production
```

### Déploiement CI/CD
```bash
# 1. Commit et push
git add .
git commit -m "✨ New model version"
git push origin main

# 2. GitHub Actions s'exécute automatiquement :
#    - Tests
#    - Build Docker
#    - Security scan
#    - Deploy staging

# 3. Vérifier dans GitHub Actions tab
```

## 5️⃣ Structure des Fichiers

```
callcenterai/
├── dvc.yaml              # Pipeline DVC
├── params.yaml           # Hyperparamètres
├── .dvcignore           # Fichiers ignorés par DVC
├── .github/
│   └── workflows/
│       └── ci-cd.yml    # Pipeline CI/CD
├── scripts/
│   ├── prepare_data.py  # Stage 1: Préparation données
│   ├── train_tfidf.py   # Stage 2: Entraînement
│   └── mlflow_registry.py  # Gestion Model Registry
├── data/
│   ├── raw/             # Données brutes
│   └── processed/       # Données traitées
├── models/              # Modèles entraînés
└── mlruns/             # Artefacts MLflow
```

## 6️⃣ Commandes Utiles

### DVC
```bash
dvc status              # Statut du pipeline
dvc repro               # Rejouer le pipeline
dvc metrics diff        # Comparer métriques
dvc plots diff          # Comparer plots
dvc push                # Pousser les données vers remote
dvc pull                # Récupérer les données depuis remote
```

### MLflow
```bash
mlflow ui               # Interface web
mlflow experiments list # Lister expériences
mlflow runs list        # Lister runs
mlflow models list      # Lister modèles registry
```

### Git
```bash
git add dvc.yaml params.yaml dvc.lock
git commit -m "🔧 Update pipeline"
git push
```

## 7️⃣ Troubleshooting

### DVC ne trouve pas les données
```bash
# Vérifier le chemin dans dvc.yaml
# Ajuster le chemin relatif dans scripts/prepare_data.py
```

### MLflow connexion refusée
```bash
# Vérifier que le serveur MLflow est lancé
mlflow server --port 5000

# Vérifier l'URL dans les scripts
# TRACKING_URI = "http://localhost:5000"
```

### GitHub Actions échoue
```bash
# Vérifier les logs dans l'onglet Actions
# Tester localement avec act
act push -j lint-and-test
```

## 📊 Résultat Attendu

✅ **DVC** : Pipeline automatisé `prepare → train_tfidf`
✅ **MLflow** : Tracking de tous les runs avec métriques
✅ **Model Registry** : Modèles en Staging/Production
✅ **CI/CD** : Tests + Build + Security scan automatiques
✅ **Trivy** : Scan de sécurité des images Docker

## 🎯 Prochaines Étapes

1. Ajouter des tests unitaires dans `tests/`
2. Configurer un remote storage DVC (S3/GDrive)
3. Ajouter monitoring avec Prometheus/Grafana
4. Implémenter CD avec Kubernetes
