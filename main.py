import os
import sys

# Ajout du répertoire courant au PATH pour éviter les erreurs d'importation
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dao.connection import DBConnection
from ui.app_gui import CongesApp

def bootstrap():
    """
    Prépare l'environnement avant le lancement de l'application.
    """
    print("--- Initialisation du Système de Gestion des Congés ---")
    
    # 1. Création de la base de données et des tables si nécessaire
    try:
        DBConnection.initialiser_db()
    except Exception as e:
        print(f"Erreur critique lors de l'initialisation de la base : {e}")
        sys.exit(1)

def main():
    # Lancement de la configuration
    bootstrap()
    
    # Lancement de l'application graphique
    print("Lancement de l'interface graphique...")
    app = CongesApp()
    app.mainloop()

if __name__ == "__main__":
    main()