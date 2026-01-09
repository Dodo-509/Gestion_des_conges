from models.personne import Personne

class Employe(Personne):
    """
    Représente un employé dans le système.
    Hérite des attributs nom et prenom de la classe Personne.
    """

    def __init__(self, matricule, nom, prenom, service, solde_conges=22, id=None):
        # Appel du constructeur de la classe parente (Personne)
        super().__init__(nom, prenom)
        
        # Attributs spécifiques à l'employé
        self.id = id  # Sera défini par SQLite (PRIMARY KEY)
        self.matricule = matricule
        self.service = service
        # Encapsulation du solde
        self._solde_conges = solde_conges

    # --- Encapsulation et Intégrité ---
    @property
    def solde_conges(self):
        """Getter pour lire le solde."""
        return self._solde_conges

    @solde_conges.setter
    def solde_conges(self, valeur):
        """
        Setter qui protège l'intégrité des données.
        Empêche d'avoir un solde négatif au niveau de l'objet.
        """
        if valeur < 0:
            raise ValueError("Le solde de congés ne peut pas être négatif.")
        self._solde_conges = valeur

    # --- Implémentation de la méthode abstraite ---
    def __str__(self):
        """Représentation textuelle de l'employé."""
        return f"[{self.matricule}] {self.prenom} {self.nom} - Service: {self.service} (Solde: {self._solde_conges}j)"

    # --- Méthode métier simple ---
    def a_assez_de_solde(self, jours_demandes):
        """Vérifie si l'employé peut poser le nombre de jours demandés."""
        return self._solde_conges >= jours_demandes