from models.personne import Personne

class Responsable(Personne):
    """
    Représente un utilisateur avec des droits de validation (RH / Manager).
    Hérite de Personne.
    """

    def __init__(self, nom, prenom, role="Responsable RH", id=None):
        # Appel du constructeur parent (Personne)
        super().__init__(nom, prenom)
        
        self.id = id
        self.role = role

    def __str__(self):
        """Implémentation de la méthode abstraite de Personne."""
        return f"[Accès {self.role}] {self.prenom} {self.nom}"

    def peut_valider(self):
        """
        Exemple de méthode logique : 
        Vérifie si ce profil a les droits de validation.
        """
        return True