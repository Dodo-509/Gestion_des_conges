from abc import ABC, abstractmethod

class Personne(ABC):
    """
    Classe abstraite représentant une personne physique.
    Elle ne peut pas être instanciée directement.
    """

    def __init__(self, nom, prenom):
        # Encapsulation : attributs protégés (accessibles par les classes filles)
        self._nom = nom
        self._prenom = prenom

    # --- Getters ---
    @property
    def nom(self):
        return self._nom

    @property
    def prenom(self):
        return self._prenom

    # --- Setters ---
    @nom.setter
    def nom(self, valeur):
        if not valeur:
            raise ValueError("Le nom ne peut pas être vide.")
        self._nom = valeur

    @prenom.setter
    def prenom(self, valeur):
        if not valeur:
            raise ValueError("Le prénom ne peut pas être vide.")
        self._prenom = valeur

    # --- Méthode Abstraite ---
    @abstractmethod
    def __str__(self):
        """
        Force les classes filles (Employe, Responsable) à définir 
        leur propre méthode de présentation.
        """
        pass