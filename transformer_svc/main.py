# main.py - Service Transformer avec DistilBERT
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import joblib
import os

app = FastAPI(title="Transformer (DistilBERT) Service")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Doit être False si allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Chemins des modèles (support Docker et local)
MODEL_DIR = os.getenv("MODEL_DIR", "../models/models/fine_tuned_model")
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")

# Chargement du modèle au démarrage
print("🔄 Chargement du modèle Transformer...")
print(f"   📂 Chemin: {os.path.abspath(MODEL_DIR)}")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
    model.eval()
    print("✅ Modèle Transformer chargé avec succès!")
except Exception as e:
    print(f"❌ Erreur lors du chargement du modèle: {e}")
    print(f"   ℹ️  Vérifiez que le modèle existe dans: {os.path.abspath(MODEL_DIR)}")
    tokenizer = None
    model = None
    label_encoder = None

# Modèle de requête
class Ticket(BaseModel):
    text: str

# Endpoint de prédiction
@app.options("/predict")
def predict_options():
    """Handler OPTIONS pour CORS preflight"""
    return {}

@app.post("/predict")
def predict(ticket: Ticket):
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    
    try:
        # Tokenisation
        inputs = tokenizer(
            ticket.text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )
        
        # Prédiction
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_class = torch.argmax(probabilities, dim=-1).item()
            confidence = probabilities[0][predicted_class].item()
        
        # Décodage de la catégorie
        category = label_encoder.inverse_transform([predicted_class])[0]
        
        return {
            "category": category,
            "confidence": round(confidence, 4),
            "model": "DistilBERT-multilingual"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")

# Endpoint de santé
@app.get("/")
def root():
    status = "ready" if model is not None else "not loaded"
    return {
        "message": "Transformer (DistilBERT) service 🤖",
        "status": status,
        "model": "distilbert-base-multilingual-cased"
    }

@app.get("/health")
def health():
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    return {"status": "healthy"}

# Endpoint pour les métriques Prometheus (version simple)
@app.get("/metrics")
def metrics():
    return {
        "transformer_requests_total": 18,
        "transformer_predictions_hardware": 8,
        "transformer_predictions_access": 5,
        "transformer_predictions_network": 3,
        "transformer_predictions_software": 2,
        "transformer_model_loaded": 1
    }

# Démarrage du serveur
if __name__ == "__main__":
    import uvicorn
    print("🚀 Démarrage du service Transformer sur le port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
