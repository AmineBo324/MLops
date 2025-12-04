# 📁 Modèles ML - CallCenterAI

Ce dossier contient les modèles entraînés pour le projet CallCenterAI.

## ⚠️ Fichiers Non Inclus dans Git

Les fichiers de modèles suivants sont exclus du repository (trop volumineux):

- `ticket_classifier_model.pkl` - Modèle TF-IDF + SVM complet
- `tfidf_vectorizer.pkl` - Vectorizer TF-IDF
- `svm_model.pkl` - Modèle SVM
- `models/fine_tuned_model/` - Modèle Transformer fine-tuné

## 🔧 Entraînement des Modèles

Pour générer les modèles localement:

```bash
cd C:\Users\LENOVO\OneDrive\Desktop\cours\MLops\callcenterai
python create_models.py
```

## 📊 Informations

- **Précision TF-IDF**: ~89.7%
- **Format**: Pickle (scikit-learn)
- **Taille totale**: ~500 MB (avec modèle Transformer)

## 📥 Téléchargement

Si vous clonez ce projet, vous devez entraîner les modèles en utilisant le script `create_models.py`.
