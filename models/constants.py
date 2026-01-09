from enum import Enum

class StatutConge(Enum):
    EN_ATTENTE = "En attente"
    ACCEPTE = "Accepté"
    REFUSE = "Refusé"

class TypeConge(Enum):
    ANNUEL = "Annuel"
    MALADIE = "Maladie"
    EXCEPTIONNEL = "Exceptionnel"

class ServiceName(Enum):
    INFORMATIQUE = "Informatique"
    RH = "RH"
    COMPTABILITE = "Comptabilité"
    DIRECTION = "Direction"