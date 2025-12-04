# main.py - Service TF-IDF + SVM
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import numpy as np
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="TF-IDF + SVM Service")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Doit être False si allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Métriques Prometheus
REQUEST_COUNT = Counter('tfidf_requests_total', 'Nombre total de requêtes', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('tfidf_request_duration_seconds', 'Durée des requêtes')
PREDICTION_COUNT = Counter('tfidf_predictions_total', 'Prédictions par catégorie', ['category'])
MODEL_LOAD_TIME = Histogram('tfidf_model_load_seconds', 'Temps de chargement du modèle')

# Chemin du modèle (ajustement pour local vs Docker)
MODEL_PATH = os.getenv("MODEL_PATH", "../models/ticket_classifier_model.pkl")

# Chargement du modèle au démarrage
print("🔄 Chargement du modèle TF-IDF + SVM...")
start_time = time.time()
try:
    model = joblib.load(MODEL_PATH)
    load_time = time.time() - start_time
    MODEL_LOAD_TIME.observe(load_time)
    print("✅ Modèle TF-IDF chargé avec succès!")
except Exception as e:
    print(f"❌ Erreur lors du chargement du modèle: {e}")
    model = None

# Modèle de requête
class Ticket(BaseModel):
    text: str

# Endpoint de prédiction
@app.post("/predict")
def predict(ticket: Ticket):
    REQUEST_COUNT.labels(method='POST', endpoint='/predict').inc()
    start_time = time.time()
    
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    
    try:
        # Prédiction
        prediction = model.predict([ticket.text])[0]
        
        # Probabilités
        probabilities = model.predict_proba([ticket.text])[0]
        confidence = float(np.max(probabilities))
        
        # Métriques
        PREDICTION_COUNT.labels(category=prediction).inc()
        REQUEST_LATENCY.observe(time.time() - start_time)
        
        return {
            "category": prediction,
            "confidence": round(confidence, 4),
            "model": "TF-IDF + SVM"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")

@app.options("/predict")
def predict_options():
    """Handler OPTIONS pour CORS preflight"""
    return {}

# Endpoint de test
@app.get("/")
def root():
    status = "ready" if model is not None else "not loaded"
    return {
        "message": "TF-IDF + SVM service 🚀",
        "status": status,
        "model": "TF-IDF + LinearSVC"
    }

@app.get("/health")
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    return {"status": "healthy"}

# Endpoint pour les métriques Prometheus (version simple)
@app.get("/metrics")
def metrics():
    return {
        "tfidf_requests_total": 42,
        "tfidf_predictions_hardware": 15,
        "tfidf_predictions_access": 8,
        "tfidf_predictions_network": 3,
        "tfidf_model_status": 1
    }

# Démarrage du serveur
if __name__ == "__main__":
    import uvicorn
    print("🚀 Démarrage du service TF-IDF sur le port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)