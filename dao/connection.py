import sqlite3
import os

class DBConnection:
    """
    Gère la connexion à la base de données SQLite et l'initialisation du schéma.
    """
    DB_NAME = "data/conges.db"

    @staticmethod
    def get_connection():
        """
        Crée et retourne une connexion à la base SQLite avec row_factory.
        """
        # S'assurer que le dossier data existe
        os.makedirs(os.path.dirname(DBConnection.DB_NAME), exist_ok=True)
        
        conn = sqlite3.connect(DBConnection.DB_NAME)
        # Permet d'accéder aux colonnes par nom : row["nom"] au lieu de row[2]
        conn.row_factory = sqlite3.Row
        # Active le support des clés étrangères (important pour les FK)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    @staticmethod
    def initialiser_db():
        """
        Crée les tables employes et demandes_conge si elles n'existent pas.
        """
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            # Table des employés
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    matricule TEXT UNIQUE NOT NULL,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    service TEXT,
                    solde_conges INTEGER NOT NULL
                )
            """)

            # Table des demandes de congé
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS demandes_conge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employe_id INTEGER NOT NULL,
                    date_debut TEXT NOT NULL,
                    date_fin TEXT NOT NULL,
                    type_conge TEXT NOT NULL,
                    statut TEXT NOT NULL,
                    commentaire TEXT,
                    FOREIGN KEY (employe_id) REFERENCES employes (id)
                )
            """)

            conn.commit()
            print("Base de données initialisée avec succès.")
        except sqlite3.Error as e:
            print(f"Erreur lors de l'initialisation de la base : {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    # Test rapide de création
    DBConnection.initialiser_db()