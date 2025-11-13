from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import sys
import time
from datetime import datetime

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__, 
           static_folder='.',
           static_url_path='')
CORS(app)

# Configuration des services
SERVICES = {
    'tfidf': 'http://localhost:8000',
    'transformer': 'http://localhost:8001',
    'agent': 'http://localhost:8003'
}

# Statistiques globales
stats = {
    'total_predictions': 0,
    'total_latency': 0,
    'categories_count': {},
    'service_usage': {},
    'start_time': datetime.now()
}

@app.route('/')
def index():
    """Page d'accueil avec l'interface web"""
    return send_from_directory('.', 'index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint unifié pour toutes les prédictions"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        service = data.get('service', 'agent')  # Par défaut: agent
        
        if not text:
            return jsonify({'error': 'Texte requis'}), 400
            
        start_time = time.time()
        
        # Définir l'endpoint selon le service
        if service == 'tfidf':
            url = f"{SERVICES['tfidf']}/predict"
        elif service == 'transformer':
            url = f"{SERVICES['transformer']}/predict"
        elif service == 'agent':
            url = f"{SERVICES['agent']}/route"
        else:
            return jsonify({'error': 'Service non supporté'}), 400
        
        # Faire la requête au service
        response = requests.post(url, 
                               json={'text': text},
                               timeout=30)
        
        latency = (time.time() - start_time) * 1000  # en ms
        
        if response.status_code == 200:
            result = response.json()
            
            # Extraire la prédiction (pour l'agent, c'est dans 'prediction')
            prediction = result.get('prediction', result)
            
            # Mettre à jour les statistiques
            update_stats(prediction, service, latency)
            
            return jsonify({
                'prediction': prediction,
                'service': service,
                'latency_ms': round(latency, 2),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'error': f'Erreur du service {service}: {response.status_code}'
            }), response.status_code
            
    except requests.RequestException as e:
        return jsonify({
            'error': f'Erreur de connexion au service {service}: {str(e)}'
        }), 503
    except Exception as e:
        return jsonify({
            'error': f'Erreur interne: {str(e)}'
        }), 500

@app.route('/api/health')
def health():
    """Vérifier l'état des services"""
    service_status = {}
    
    for service_name, url in SERVICES.items():
        try:
            response = requests.get(f"{url}/health", timeout=5)
            service_status[service_name] = {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'response_time': response.elapsed.total_seconds() * 1000
            }
        except Exception as e:
            service_status[service_name] = {
                'status': 'unreachable',
                'error': str(e)
            }
    
    return jsonify({
        'web_interface': 'healthy',
        'services': service_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stats')
def get_stats():
    """Retourner les statistiques d'utilisation"""
    uptime = datetime.now() - stats['start_time']
    
    avg_latency = 0
    if stats['total_predictions'] > 0:
        avg_latency = stats['total_latency'] / stats['total_predictions']
    
    most_common_category = None
    if stats['categories_count']:
        most_common_category = max(stats['categories_count'].items(), 
                                 key=lambda x: x[1])[0]
    
    return jsonify({
        'total_predictions': stats['total_predictions'],
        'avg_latency_ms': round(avg_latency, 2),
        'categories_count': stats['categories_count'],
        'service_usage': stats['service_usage'],
        'most_common_category': most_common_category,
        'uptime_seconds': uptime.total_seconds(),
        'uptime_readable': str(uptime).split('.')[0]  # Format HH:MM:SS
    })

@app.route('/api/examples')
def get_examples():
    """Retourner des exemples de textes pour chaque catégorie"""
    examples = {
        'facturation': [
            'Ma facture est incorrecte ce mois-ci',
            'Je n\'ai pas reçu ma facture',
            'Il y a une erreur sur ma facturation',
            'Je veux contester ma facture',
            'Problème avec le montant facturé'
        ],
        'technique': [
            'Je n\'arrive pas à me connecter',
            'L\'application ne fonctionne plus',
            'Problème de connexion réseau',
            'Mon mot de passe ne marche plus',
            'Bug lors de la synchronisation'
        ],
        'support': [
            'J\'ai besoin d\'aide pour configurer',
            'Comment utiliser cette fonctionnalité ?',
            'Guide d\'installation requis',
            'Aide pour la première configuration',
            'Support technique général'
        ],
        'commercial': [
            'Je veux changer d\'offre',
            'Information sur vos tarifs',
            'Upgrade vers premium',
            'Demande de devis personnalisé',
            'Négociation de contrat'
        ]
    }
    
    return jsonify(examples)

@app.route('/api/demo')
def demo_mode():
    """Mode démo avec prédictions simulées"""
    try:
        # Importer et utiliser le modèle local si disponible
        from training_testing_models.tf_idf_model import load_model, predict_category
        
        text = request.args.get('text', 'Exemple de texte pour la démo')
        
        # Simuler une prédiction avec des données réalistes
        categories = ['facturation', 'technique', 'support', 'commercial']
        confidences = [0.89, 0.76, 0.92, 0.84]
        
        import random
        category = random.choice(categories)
        confidence = random.choice(confidences)
        
        result = {
            'category': category,
            'confidence': confidence,
            'model': 'demo-mode',
            'demo': True
        }
        
        return jsonify({
            'prediction': result,
            'service': 'demo',
            'latency_ms': random.randint(50, 200),
            'timestamp': datetime.now().isoformat()
        })
        
    except ImportError:
        return jsonify({
            'error': 'Mode démo non disponible - modèles non trouvés'
        }), 503

def update_stats(prediction, service, latency):
    """Mettre à jour les statistiques globales"""
    stats['total_predictions'] += 1
    stats['total_latency'] += latency
    
    # Compter les catégories
    category = prediction.get('category', 'unknown')
    stats['categories_count'][category] = stats['categories_count'].get(category, 0) + 1
    
    # Compter l'usage des services
    stats['service_usage'][service] = stats['service_usage'].get(service, 0) + 1

if __name__ == '__main__':
    print("🌐 Démarrage de l'interface web CallCenterAI...")
    print("📍 Interface disponible sur: http://localhost:5001")
    print("🔄 Services attendus:")
    for service, url in SERVICES.items():
        print(f"   • {service.upper()}: {url}")
    
    print("\n💡 Pour tester sans services externes:")
    print("   • Utilisez l'endpoint /api/demo")
    print("   • Vérifiez l'état: /api/health")
    
    app.run(
        debug=True, 
        host='0.0.0.0', 
        port=5001,
        threaded=True
    )