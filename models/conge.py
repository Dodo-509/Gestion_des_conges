from abc import ABC, abstractmethod
from datetime import datetime

class DemandeConge(ABC):
    """
    Classe de base Abstraite pour tous les types de congés.
    Illustre l'Héritage et l'Abstraction.
    """
    def __init__(self, employe_id, date_debut, date_fin, commentaire="", id=None):
        self.id = id
        self.employe_id = employe_id
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.commentaire = commentaire
        self.statut = "En attente"

    def calculer_duree(self):
        """Calcule le nombre de jours calendaires entre deux dates."""
        fmt = "%Y-%m-%d"
        debut = datetime.strptime(self.date_debut, fmt)
        fin = datetime.strptime(self.date_fin, fmt)
        return (fin - debut).days + 1

    @abstractmethod
    def jours_a_deduire(self):
        """
        MÉTHODE POLYMORPHE : Chaque type de congé définit 
        combien de jours sont retirés du solde annuel.
        """
        pass

    @property
    @abstractmethod
    def type_label(self):
        """Retourne le nom du type de congé pour la base de données."""
        pass


class CongeAnnuel(DemandeConge):
    """Congé classique qui impacte le solde (22j)."""
    @property
    def type_label(self):
        return "Annuel"

    def jours_a_deduire(self):
        # Pour un congé annuel, on déduit la totalité des jours
        return self.calculer_duree()


class CongeMaladie(DemandeConge):
    """Congé maladie : n'impacte pas le solde annuel de l'employé."""
    @property
    def type_label(self):
        return "Maladie"

    def jours_a_deduire(self):
        # La maladie est justifiée, on ne touche pas au solde de 22j
        return 0


class CongeExceptionnel(DemandeConge):
    """Ex: Mariage, Naissance. Peut avoir un forfait fixe ou 0."""
    @property
    def type_label(self):
        return "Exceptionnel"

    def jours_a_deduire(self):
        # Souvent offert par l'entreprise
        return 0