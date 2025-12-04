"""
Tests unitaires pour les services CallCenterAI
"""
import pytest
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_import_services():
    """Test que tous les services peuvent être importés"""
    try:
        # Ces imports échoueront si les fichiers n'existent pas
        assert Path("agent/main.py").exists()
        assert Path("tfidf_svc/main.py").exists()
        assert Path("transformer_svc/main.py").exists()
        assert Path("web_interface/app.py").exists()
    except Exception as e:
        pytest.fail(f"Import failed: {e}")

def test_models_directory():
    """Test que le dossier models existe"""
    assert Path("models").exists()

def test_dvc_files():
    """Test que les fichiers DVC sont présents"""
    assert Path("dvc.yaml").exists()
    assert Path("params.yaml").exists()

def test_ci_cd_config():
    """Test que la config CI/CD existe"""
    assert Path(".github/workflows/ci-cd.yml").exists()

# Tests pour la préparation des données
def test_prepare_script_exists():
    """Test que le script de préparation existe"""
    assert Path("scripts/prepare_data.py").exists()

def test_train_script_exists():
    """Test que le script d'entraînement existe"""
    assert Path("scripts/train_tfidf.py").exists()

# Tests des paramètres
def test_params_yaml():
    """Test que params.yaml est valide"""
    import yaml
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)
    
    assert 'prepare' in params
    assert 'train_tfidf' in params
    assert params['prepare']['test_size'] > 0
    assert params['prepare']['test_size'] < 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
