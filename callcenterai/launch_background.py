#!/usr/bin/env python3
"""
Script simple pour lancer les services CallCenterAI en arrière-plan
"""
import subprocess
import sys
import os
import time

def launch_services():
    """Lancer les 3 services en parallèle"""
    print("🚀 DÉMARRAGE CALLCENTERAI SERVICES")
    print("=" * 50)
    
    services = [
        ("TF-IDF Service", "tfidf_svc", 8000),
        ("Transformer Service", "transformer_svc", 8001), 
        ("Agent Service", "agent", 8003)
    ]
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    processes = []
    
    for service_name, service_dir, port in services:
        service_path = os.path.join(script_dir, service_dir)
        main_py = os.path.join(service_path, "main.py")
        
        if os.path.exists(main_py):
            print(f"🚀 Lancement {service_name} sur port {port}...")
            
            # Lancer le service avec CREATE_NEW_CONSOLE pour Windows
            if os.name == 'nt':  # Windows
                process = subprocess.Popen(
                    [sys.executable, "main.py"],
                    cwd=service_path,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:  # Linux/Mac
                process = subprocess.Popen(
                    [sys.executable, "main.py"],
                    cwd=service_path
                )
            
            processes.append((process, service_name))
            print(f"✅ {service_name} démarré (PID: {process.pid})")
            time.sleep(1)  # Petite pause entre les démarrages
        else:
            print(f"❌ Script non trouvé: {main_py}")
    
    if processes:
        print(f"\n🎉 {len(processes)} service(s) lancé(s) en arrière-plan!")
        print("\n📍 Services disponibles:")
        print("   • TF-IDF Service: http://localhost:8000")
        print("   • Transformer Service: http://localhost:8001")
        print("   • Agent Service: http://localhost:8003")
        print("\n💡 Pour tester:")
        print("   • Interface Web: cd web_interface && python launch_web.py")
        print("   • Vérif santé: python test_local.py")
        print("\n🛑 Pour arrêter: fermez les fenêtres des services ou Task Manager")
    else:
        print("❌ Aucun service démarré!")

if __name__ == "__main__":
    launch_services()