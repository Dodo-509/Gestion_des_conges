from dao.employe_dao import EmployeDAO

class AuthService:
    """
    Gère l'authentification et les droits d'accès.
    """
    _utilisateur_connecte = None  # Stocke l'objet Employe ou Responsable

    @staticmethod
    def login(matricule):
        """
        Simule une connexion par matricule.
        Récupère l'utilisateur en base via le DAO.
        """
        dao = EmployeDAO()
        user_data = dao.trouver_par_matricule(matricule)
        
        if user_data:
            # On pourrait ici transformer le Row en objet Employe ou Responsable
            AuthService._utilisateur_connecte = user_data
            print(f"Bienvenue, {user_data['prenom']} {user_data['nom']} !")
            return True
        else:
            print("Erreur : Matricule inconnu.")
            return False

    @staticmethod
    def logout():
        AuthService._utilisateur_connecte = None

    @staticmethod
    def est_responsable():
        """
        Vérifie si l'utilisateur a les droits de validation.
        Ici, on peut imaginer un champ 'role' ou tester le service 'RH'.
        """
        user = AuthService._utilisateur_connecte
        if user and (user['service'] == 'RH' or user['service'] == 'Direction'):
            return True
        return False

    @staticmethod
    def get_user_id():
        return AuthService._utilisateur_connecte['id'] if AuthService._utilisateur_connecte else None