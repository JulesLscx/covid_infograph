import pymongo as pm
from urllib.parse import quote_plus


class SingletonMongoConnection:
    """Classe implémentant le design pattern Singleton pour une connexion MongoDB unique.

    Attributs:
        __instance (SingletonMongoConnection): L'instance unique de la classe.
        client (pymongo.MongoClient): La connexion MongoDB.

    """

    __instance = None

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
            username = quote_plus('<Jules>')
            password = quote_plus('<C6IyTitjpiYeq4t4>')
            cluster = '<SAE>'
            uri = 'mongodb+srv://' + username + ':' + password + '@' + cluster + \
                '.x1hujrr.mongodb.net'
            self.client = pm.MongoClient(uri)
            SingletonMongoConnection.__instance = self


def connection():
    """Récupère la collection test de la connexion MongoDB.

    Retourne:
        pymongo.collection.Collection: La collection test de la connexion MongoDB.

    """
    return SingletonMongoConnection.get_instance().client.test
