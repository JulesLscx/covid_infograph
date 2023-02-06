import pymongo as pm
from urllib.parse import quote_plus


class SingletonMongoConnection:
    """Classe implémentant le design pattern Singleton pour une connexion MongoDB unique.

    Attributs:
        __instance (SingletonMongoConnection): L'instance unique de la classe.
        client (pymongo.MongoClient): La connexion MongoDB.

    """

    __instance = None
    client = None

    @staticmethod
    def get_instance():
        """Récupère l'instance unique de la classe SingletonMongoConnection.

        Retourne:
            SingletonMongoConnection: L'instance unique de la classe.

        """
        if SingletonMongoConnection.__instance is None:
            SingletonMongoConnection()
        return SingletonMongoConnection.__instance

    def __init__(self):
        """Initialise l'instance unique de la classe SingletonMongoConnection."""
        if SingletonMongoConnection.__instance is not None:
            raise Exception("Cette classe est un singleton !")
        else:

            client = pm.MongoClient(
                "mongodb+srv://Jules:C6IyTitjpiYeq4t4@sae.x1hujrr.mongodb.net/?retryWrites=true&w=majority")
            self.client = client
            SingletonMongoConnection.__instance = self

    @staticmethod
    def get_db():
        return SingletonMongoConnection.get_instance().client['covid_infograph']
