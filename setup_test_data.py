from dao.connection import DBConnection
from dao.employe_dao import EmployeDAO
from dao.conge_dao import CongeDAO
from models.employe import Employe

def charger_donnees_test():
    """
    Script de démonstration : 
    Initialise la DB et crée un jeu de données cohérent.
    """
    print("Initialisation des données de test...")
    DBConnection.initialiser_db()
    
    emp_dao = EmployeDAO()
    conge_dao = CongeDAO()

    # 1. Création des employés (Modèles)
    # Un employé standard
    ali = Employe("E001", "Dupont", "Ali", "Informatique", 22)
    # Un responsable RH
    admin = Employe("R001", "Zili", "Hicham", "RH", 30)

    # 2. Insertion en base via le DAO
    id_ali = emp_dao.ajouter(ali)
    id_admin = emp_dao.ajouter(admin)

    if id_ali and id_admin:
        print(f"Employés créés : Ali (ID:{id_ali}) et Hicham (ID:{id_admin})")
        
        # 3. Création d'une demande de test pour Ali (via un dictionnaire pour le DAO)
        from collections import namedtuple
        Demande = namedtuple('Demande', ['employe_id', 'date_debut', 'date_fin', 'type_conge', 'statut', 'commentaire'])
        
        demande_test = Demande(
            employe_id=id_ali,
            date_debut="2024-06-01",
            date_fin="2024-06-05", # 5 jours
            type_conge="Annuel",
            statut="En attente",
            commentaire="Vacances d'été"
        )
        
        conge_dao.ajouter(demande_test)
        print("Demande de test créée pour Ali (5 jours, En attente).")
        print("--- Système prêt pour la démo ---")
        print("Identifiants de test :")
        print(" - Employé : E001")
        print(" - Responsable RH : R001")
    else:
        print("Note : Les données existent peut-être déjà (Matricules uniques).")

if __name__ == "__main__":
    charger_donnees_test()