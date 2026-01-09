from dao.connection import DBConnection
import sqlite3

class EmployeDAO:
    """
    Data Access Object pour la table employes.
    Gère la persistance des données des employés et de leur solde.
    """

    @staticmethod
    def ajouter(employe):
        """
        Insère un nouvel employé en base de données.
        'employe' est une instance de la classe Employe (modèle).
        """
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO employes (matricule, nom, prenom, service, solde_conges)
                VALUES (?, ?, ?, ?, ?)
            """, (
                employe.matricule,
                employe.nom,
                employe.prenom,
                employe.service,
                employe.solde_conges
            ))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Erreur : Le matricule '{employe.matricule}' existe déjà.")
            return None
        except sqlite3.Error as e:
            print(f"Erreur DAO (Ajout Employé) : {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def modifier_solde(id_employe, nouveau_solde):
        """
        Met à jour le nombre de jours restants pour un employé.
        Cette méthode est appelée lors de la validation d'un congé.
        """
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE employes SET solde_conges = ? WHERE id = ?", (nouveau_solde, id_employe))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur DAO (Mise à jour solde) : {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def trouver_par_id(id_employe):
        """Récupère les informations d'un employé par son ID unique (PK)."""
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employes WHERE id = ?", (id_employe,))
        row = cursor.fetchone()
        conn.close()
        return row

    @staticmethod
    def trouver_par_matricule(matricule):
        """Utile pour retrouver un employé via son identifiant 'métier'."""
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employes WHERE matricule = ?", (matricule,))
        row = cursor.fetchone()
        conn.close()
        return row

    @staticmethod
    def trouver_tout():
        """Récupère la liste de tous les employés."""
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employes ORDER BY nom ASC")
        rows = cursor.fetchall()
        conn.close()
        return rows