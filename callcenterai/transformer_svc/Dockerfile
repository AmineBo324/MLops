# Dockerfile pour le service Transformer
# Use an official PyTorch CPU image to avoid downloading large torch wheels during build
# Use slim Python base and make pip more resilient for large packages (torch)
FROM python:3.11-slim

WORKDIR /app

# Préinstaller paquets système utiles (compilation, SSL, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	gcc \
	libffi-dev \
	libssl-dev \
	curl \
 && rm -rf /var/lib/apt/lists/*

# Copier les dépendances
COPY requirements.txt .
# Installer torch CPU SEULEMENT (évite tous les packages CUDA/nvidia)
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.9.0+cpu

# Installer le reste SANS torch pour éviter conflits
RUN pip install --no-cache-dir fastapi uvicorn transformers joblib scikit-learn

# Copier le code du service
COPY . .

# Exposer le port de FastAPI
EXPOSE 8001

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
