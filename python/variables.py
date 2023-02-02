from typing import final
from enum import Enum


@final
class Keywords(Enum):
    """Classe contenant tous les mots clés éviter toutes chaines de caractères.
    Utiliser au maximum ces mots clés pour la modularité du code
    """
    T_CLINICALTRIALS_OBS = "clinicalTrials_obsStudies"
    """
    constante pour le nom de la collection mongo des Clinicals Trials Observals Studies
    """

    T_CLINICALTRIALS_RAND = "clinicalTrials_randTrials"
    """
    constante pour le nom de la collection mongo des Clinicals Trials Randoms Studies
    """

    T_PUBLICATION_OBS = "publication_obsStudies"
    """
    constante pour le nom de la collection mongo des publications des Observals Studies
    """

    T_PUBLICATION_RAND = "publication_randTrials"
    """
    constante pour le nom de la collection mongo des publications des Randoms Trials
    """

    WS_README = "readme"
    """
    constante pour le nom de la Worksheet Excel du readMe
    """
    WS_CLINICALTRIALS_OBS = "1 - ClinicalTrials_ObsStudies"
    """
    constante pour le nom de la Worksheet Excel des Clinicals Trials Observals Studies
    """

    WS_CLINICALTRIALS_RAND = "2 - ClinicalTrials_RandTrials"
    """
    constante pour le nom de la Worksheet Excel des Clinicals Trials Randoms Studies
    """

    WS_PUBLICATION_OBS = "3 - Publications_ObsStudies"
    """
    constante pour le nom de la Worksheet Excel des publications des Observals Studies
    """

    WS_PUBLICATION_RAND = "4 - Publications_RandTrials"
    """
    constante pour le nom de la Worksheet Excel des publications des Randoms Trials
    """
