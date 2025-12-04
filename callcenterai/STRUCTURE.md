# 📁 Structure du Projet CallCenterAI

## Architecture Simplifiée

```
callcenterai/
│
├── 🤖 agent/                      # Service d'agent intelligent
│   └── main.py                    # Routage intelligent TF-IDF/Transformer
│
├── 📊 tfidf_svc/                  # Service TF-IDF (rapide)
│   └── main.py                    # Classification avec SVM
│
├── 🧠 transformer_svc/            # Service Transformer (précis)
│   └── main.py                    # Classification avec DistilBERT
│
├── 🌐 web_interface/              # Interface web chatbot
│   ├── app.py                     # Backend Flask
│   ├── index.html                 # Frontend chatbot
│   ├── launch_web.py              # Script de lancement
│   └── requirements.txt           # Dépendances web
│
├── 💾 models/                     # Modèles ML entraînés
│   ├── ticket_classifier_model.pkl         # Modèle TF-IDF + SVM
│   └── models/fine_tuned_model/            # Modèle Transformer fine-tuné
│
├── 🚀 launch_background.py        # Lancement des 3 microservices
├── 🔧 create_models.py            # Script d'entraînement
├── 📝 README.md                   # Documentation principale
└── ⚙️  .env                       # Variables d'environnement

```

## 🎯 Composants Essentiels

### Services Backend (Ports)
- **TF-IDF Service**: Port 8000 - Classification rapide
- **Transformer Service**: Port 8001 - Classification précise
- **Agent Service**: Port 8003 - Routage intelligent

### Interface Web
- **Flask App**: Port 5001 - Interface chatbot

## 🚀 Commandes de Lancement

### 1. Lancer les services backend
```powershell
cd C:\Users\LENOVO\OneDrive\Desktop\cours\MLops\callcenterai
python launch_background.py
```

### 2. Lancer l'interface web
```powershell
cd C:\Users\LENOVO\OneDrive\Desktop\cours\MLops\callcenterai\web_interface
python launch_web.py
```

### 3. Accéder à l'application
Ouvrir dans le navigateur: **http://localhost:5001**

## 📦 Fichiers Supprimés (Non Essentiels)
- ❌ `create_chatbot.py` - Script de génération (obsolète)
- ❌ `build_docker_web.py` - Build Docker (non utilisé)
- ❌ `docker-compose.yml` - Orchestration Docker (non utilisé)
- ❌ `DOCKER_README.md` - Documentation Docker (non utilisé)
- ❌ `pytest.ini` - Configuration tests (non utilisé)
- ❌ `monitoring/` - Dossier monitoring (non utilisé)
- ❌ `index_backup.html` - Backup interface (non utilisé)
- ❌ `Dockerfile` - Build Docker frontend (non utilisé)
- ❌ `__pycache__/` - Cache Python (généré automatiquement)

## 🎯 Workflow de Développement

1. **Entraîner le modèle** (si nécessaire):
   ```powershell
   python create_models.py
   ```

2. **Lancer les services**:
   ```powershell
   python launch_background.py
   ```

3. **Lancer l'interface**:
   ```powershell
   cd web_interface
   python launch_web.py
   ```

4. **Tester l'application**:
   - Ouvrir http://localhost:5001
   - Envoyer des messages dans le chatbot
   - Vérifier les classifications

## 🔧 Maintenance

### Arrêter tous les services
```powershell
Get-Process python | Stop-Process -Force
```

### Nettoyer le cache Python
```powershell
Get-ChildItem -Recurse -Directory "__pycache__" | Remove-Item -Recurse -Force
```

### Vérifier les services actifs
```powershell
netstat -ano | findstr "8000 8001 8003 5001"
```
