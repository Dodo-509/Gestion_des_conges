from dao.connection import DBConnection
import sqlite3

class CongeDAO:
    """
    Data Access Object pour la table demandes_conge.
    Gère toutes les interactions SQL pour les congés.
    """

    @staticmethod
    def ajouter(demande):
        """
        Insère une nouvelle demande de congé en base.
        L'objet 'demande' doit avoir les attributs correspondant aux colonnes.
        """
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO demandes_conge (employe_id, date_debut, date_fin, type_conge, statut, commentaire)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                demande.employe_id, 
                demande.date_debut, 
                demande.date_fin, 
                demande.type_label, 
                demande.statut, 
                demande.commentaire
            ))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erreur DAO (Ajout Congé) : {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def modifier_statut(id_demande, nouveau_statut):
        """
        Met à jour le statut d'une demande (Accepté, Refusé, En attente).
        """
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE demandes_conge SET statut = ? WHERE id = ?", (nouveau_statut, id_demande))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur DAO (Modif Statut) : {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def trouver_tout():
        """Récupère toutes les demandes de la base."""
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM demandes_conge")
        resultats = cursor.fetchall()
        conn.close()
        return resultats

    @staticmethod
    def trouver_par_employe(id_employe):
        """Récupère toutes les demandes d'un employé spécifique."""
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM demandes_conge WHERE employe_id = ?", (id_employe,))
        resultats = cursor.fetchall()
        conn.close()
        return resultats

    @staticmethod
    def trouver_par_statut(statut):
        """Récupère les demandes filtrées par statut (ex: 'En attente')."""
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM demandes_conge WHERE statut = ?", (statut,))
        resultats = cursor.fetchall()
        conn.close()
        return resultats

    @staticmethod
    def trouver_par_id(id_demande):
        """Récupère une seule demande par son ID."""
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM demandes_conge WHERE id = ?", (id_demande,))
        resultat = cursor.fetchone()
        conn.close()
        return resultat