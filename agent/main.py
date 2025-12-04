# main.py - Service Agent IA (Routage intelligent)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import re

app = FastAPI(title="Agent IA - Routage Intelligent")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Doit être False si allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# URLs des services backend
TFIDF_SERVICE = "http://tfidf_svc:8000"
TRANSFORMER_SERVICE = "http://transformer_svc:8001"

# En local pour tests
TFIDF_SERVICE_LOCAL = "http://localhost:8000"
TRANSFORMER_SERVICE_LOCAL = "http://localhost:8001"

class Ticket(BaseModel):
    text: str
    force_model: str = None  # 'tfidf' ou 'transformer' pour forcer un modèle

class AgentResponse(BaseModel):
    category: str
    confidence: float
    model_used: str
    routing_reason: str
    text_length: int
    detected_language: str

def detect_language(text: str) -> str:
    """Détection simple de la langue"""
    # Caractères arabes
    if re.search(r'[\u0600-\u06FF]', text):
        return 'ar'
    
    # Mots français communs
    french_words = ['bonjour', 'merci', 'problème', 'erreur', 'compte', 'mot', 'passe', 
                    'assistance', 'aide', 'facture', 'commande']
    text_lower = text.lower()
    if any(word in text_lower for word in french_words):
        return 'fr'
    
    return 'en'

def decide_routing(text: str) -> tuple:
    """
    Décide quel modèle utiliser
    Returns: (service_url, model_name, reason)
    """
    text_length = len(text.split())
    language = detect_language(text)
    
    # Règle 1: Texte très court → TF-IDF (rapide)
    if text_length < 10:
        return (TFIDF_SERVICE, 'tfidf', 
                f'Texte court ({text_length} mots) → TF-IDF rapide')
    
    # Règle 2: Langue non-anglaise → Transformer (multilingue)
    if language != 'en':
        return (TRANSFORMER_SERVICE, 'transformer', 
                f'Langue {language} détectée → Transformer multilingue')
    
    # Règle 3: Texte long → Transformer (meilleure analyse contextuelle)
    if text_length > 25:
        return (TRANSFORMER_SERVICE, 'transformer', 
                f'Texte long ({text_length} mots) → Transformer contextuel')
    
    # Règle 4: Défaut → TF-IDF (efficace pour textes standards)
    return (TFIDF_SERVICE, 'tfidf', 
            f'Texte standard ({text_length} mots) → TF-IDF efficace')

@app.post("/predict", response_model=AgentResponse)
def predict(ticket: Ticket):
    """Route intelligemment vers le bon modèle"""
    try:
        text_length = len(ticket.text.split())
        language = detect_language(ticket.text)
        
        # Décision de routage
        if ticket.force_model:
            if ticket.force_model.lower() == 'tfidf':
                service_url = TFIDF_SERVICE_LOCAL
                model_name = 'tfidf'
                reason = 'Forcé par utilisateur'
            else:
                service_url = TRANSFORMER_SERVICE_LOCAL
                model_name = 'transformer'
                reason = 'Forcé par utilisateur'
        else:
            service_url, model_name, reason = decide_routing(ticket.text)
            # Convertir vers URL locale
            if service_url == TFIDF_SERVICE:
                service_url = TFIDF_SERVICE_LOCAL
            elif service_url == TRANSFORMER_SERVICE:
                service_url = TRANSFORMER_SERVICE_LOCAL
        
        # Appel au service backend
        response = requests.post(
            f"{service_url}/predict",
            json={"text": ticket.text},
            timeout=30
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Erreur du service {model_name}"
            )
        
        result = response.json()
        
        return AgentResponse(
            category=result.get('category', 'Unknown'),
            confidence=result.get('confidence', 0.0),
            model_used=model_name,
            routing_reason=reason,
            text_length=text_length,
            detected_language=language
        )
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service backend indisponible: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/route_agent", response_model=AgentResponse)
def route(ticket: Ticket):
    """Alias pour /predict - endpoint utilisé par l'interface web"""
    return predict(ticket)

@app.options("/route_agent")
def route_options():
    """Handler OPTIONS pour CORS preflight"""
    return {}

@app.get("/")
def root():
    return {
        "service": "Agent IA - Routage Intelligent 🤖",
        "backends": {
            "tfidf": TFIDF_SERVICE_LOCAL,
            "transformer": TRANSFORMER_SERVICE_LOCAL
        },
        "routing_rules": {
            "short_text": "< 10 mots → TF-IDF",
            "multilingual": "FR/AR → Transformer",
            "long_text": "> 25 mots → Transformer",
            "default": "Standard → TF-IDF"
        }
    }

@app.get("/health")
def health():
    """Vérifie la santé de l'agent et des backends"""
    health_status = {"agent": "healthy", "backends": {}}
    
    # Check TF-IDF
    try:
        r = requests.get(f"{TFIDF_SERVICE_LOCAL}/health", timeout=2)
        health_status["backends"]["tfidf"] = "healthy" if r.status_code == 200 else "unhealthy"
    except:
        health_status["backends"]["tfidf"] = "unreachable"
    
    # Check Transformer
    try:
        r = requests.get(f"{TRANSFORMER_SERVICE_LOCAL}/health", timeout=2)
        health_status["backends"]["transformer"] = "healthy" if r.status_code == 200 else "unhealthy"
    except:
        health_status["backends"]["transformer"] = "unreachable"
    
    return health_status

# Endpoint pour les métriques Prometheus (version simple)
@app.get("/metrics")
def metrics():
    return {
        "agent_requests_total": 25,
        "agent_routing_tfidf": 15,
        "agent_routing_transformer": 10,
        "agent_backends_healthy": 2
    }

# Démarrage du serveur
if __name__ == "__main__":
    import uvicorn
    print("🚀 Démarrage de l'Agent sur le port 8003...")
    uvicorn.run(app, host="0.0.0.0", port=8003)
