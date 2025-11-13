# Interface Web CallCenterAI

Interface web moderne et interactive pour tester le système de classification CallCenterAI.

## 🌟 Fonctionnalités

- **Interface moderne** avec design responsive
- **3 modes de prédiction** : TF-IDF, Transformer, Agent intelligent
- **Statistiques temps réel** : prédictions, confiance, latence
- **Exemples prêts à tester** pour chaque catégorie
- **Mode démo** si les services ne sont pas disponibles
- **Monitoring des services** avec vérification de santé

## 🚀 Démarrage Rapide

### Option 1: Lancement automatique
```bash
python launch_web.py
```

### Option 2: Lancement manuel
```bash
# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'interface web
python app.py
```

L'interface sera disponible sur: http://localhost:5000

## 🔧 Configuration

### Services requis (optionnels)
- **TF-IDF Service**: http://localhost:8000
- **Transformer Service**: http://localhost:8001  
- **Agent Service**: http://localhost:8002

Si ces services ne sont pas disponibles, l'interface fonctionne en mode démo.

### Démarrer tous les services
```bash
# Depuis le répertoire racine du projet
python start.py
```

## 📱 Utilisation

1. **Saisir un message** dans la zone de texte
2. **Choisir un mode de prédiction** :
   - ⚡ **TF-IDF (Rapide)** : Modèle classique, réponse instantanée
   - 🧠 **Transformer (Précis)** : Modèle avancé, plus précis
   - 🎯 **Agent (Auto)** : Routage intelligent automatique
3. **Voir les résultats** avec catégorie, confiance, et détails
4. **Consulter les statistiques** en temps réel

## 📊 Exemples de Messages

### 💳 Facturation
- "Ma facture est incorrecte"
- "Je n'ai pas reçu ma facture"
- "Problème avec le montant facturé"

### 🔧 Technique  
- "Je n'arrive pas à me connecter"
- "L'application ne fonctionne plus"
- "Bug lors de la synchronisation"

### 🆘 Support
- "J'ai besoin d'aide pour configurer"
- "Comment utiliser cette fonctionnalité ?"
- "Guide d'installation requis"

### 💼 Commercial
- "Je veux changer d'offre"
- "Information sur vos tarifs"
- "Upgrade vers premium"

## 🔍 API Endpoints

- `GET /` - Interface web principale
- `POST /api/predict` - Prédiction unifié
- `GET /api/health` - État des services
- `GET /api/stats` - Statistiques d'utilisation
- `GET /api/examples` - Exemples par catégorie
- `GET /api/demo` - Mode démo avec simulation

## 📈 Statistiques Affichées

- **Nombre total** de prédictions
- **Confiance moyenne** des prédictions
- **Latence moyenne** des réponses
- **Catégorie la plus populaire**
- **Usage des services** (TF-IDF, Transformer, Agent)

## 🛠️ Structure des Fichiers

```
web_interface/
├── index.html          # Interface web principale
├── app.py             # Serveur Flask
├── launch_web.py      # Script de lancement
├── requirements.txt   # Dépendances Python
└── README.md         # Cette documentation
```

## 🔐 Sécurité

- CORS configuré pour développement local
- Validation des entrées utilisateur
- Timeout des requêtes aux services
- Gestion d'erreurs robuste

## 📱 Responsive Design

L'interface s'adapte automatiquement :
- **Desktop** : Layout en 2 colonnes
- **Mobile** : Layout en 1 colonne
- **Tablette** : Layout adaptatif

## 🎨 Thème Visuel

- **Couleurs** : Gradient bleu-violet moderne
- **Police** : Segoe UI (native Windows)
- **Animations** : Transitions fluides
- **Icônes** : Emojis pour facilité d'usage

## 🚨 Dépannage

### Service non accessible
- Vérifiez que les services sont démarrés
- Utilisez `python start.py` depuis la racine
- Consultez l'endpoint `/api/health`

### Erreur de dépendances
- Utilisez `pip install -r requirements.txt`
- Vérifiez votre version Python (3.8+)

### Interface ne charge pas
- Vérifiez le port 5000 disponible
- Essayez http://127.0.0.1:5000
- Consultez les logs Flask

## 📞 Support

Pour toute question ou problème, consultez :
1. Les logs de l'application Flask
2. L'endpoint `/api/health` pour l'état des services
3. La documentation du projet principal