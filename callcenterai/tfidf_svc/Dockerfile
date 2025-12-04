# Dockerfile pour le service TF-IDF + SVM
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système pour compiler scikit-learn
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copier les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code du service
COPY . .

# Exposer le port de FastAPI
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
