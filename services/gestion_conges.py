from dao.employe_dao import EmployeDAO
from dao.conge_dao import CongeDAO
from services.auth_service import AuthService
from models.constants import StatutConge, TypeConge
from models.conge import CongeAnnuel, CongeMaladie, CongeExceptionnel

class GestionConges:
    def __init__(self):
        self.employe_dao = EmployeDAO()
        self.conge_dao = CongeDAO()

    def soumettre_demande(self, demande):
        # On peut appeler la méthode de calcul de l'objet ici
        if demande.calculer_duree() <= 0:
            return False
        return self.conge_dao.ajouter(demande)

    def traiter_demande(self, id_demande, decision):
        """
        Action réservée au Responsable RH.
        """
        if not AuthService.est_responsable():
            return False
        
        demande_row = self.conge_dao.trouver_par_id(id_demande)
        if not demande_row:
            return False

        # Mapping pour reconstruire l'objet métier
        mapping = {
            TypeConge.ANNUEL.value: CongeAnnuel,
            TypeConge.MALADIE.value: CongeMaladie,
            TypeConge.EXCEPTIONNEL.value: CongeExceptionnel
        }
        
        classe_conge = mapping.get(demande_row["type_conge"], CongeAnnuel)
        demande_obj = classe_conge(
            demande_row["employe_id"], 
            demande_row["date_debut"], 
            demande_row["date_fin"]
        )

        id_emp = demande_row["employe_id"]
        employe_row = self.employe_dao.trouver_par_id(id_emp)
        
        if decision == StatutConge.ACCEPTE.value:
            jours = demande_obj.jours_a_deduire()
            if employe_row["solde_conges"] >= jours:
                nouveau_solde = employe_row["solde_conges"] - jours
                self.employe_dao.modifier_solde(id_emp, nouveau_solde)
                self.conge_dao.modifier_statut(id_demande, StatutConge.ACCEPTE.value)
                return True
        else:
            self.conge_dao.modifier_statut(id_demande, StatutConge.REFUSE.value)
            return True
        return False