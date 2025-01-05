from pymongo import MongoClient
from config import environment as E


class MongoDBConnection:
    """
    Clase para manejar conexiones a MongoDB.
    Garantiza la apertura y el cierre de conexiones de forma segura.
    """

    def __init__(self, uri: str = E.CLIENT_):
        self.uri = uri
        self.client = None

    def __enter__(self):
        # Crear y devolver la conexión
        self.client = MongoClient(self.uri)
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cerrar la conexión al salir del contexto
        if self.client:
            self.client.close()


def get_mongo_collection(db_name: str, collection_name: str):
    """
    Devuelve una colección de MongoDB utilizando un contexto seguro.

    :param db_name: Nombre de la base de datos.
    :param collection_name: Nombre de la colección.
    :return: Objeto de la colección de MongoDB.
    """
    try:
        with MongoDBConnection() as client:
            db = client[db_name]
            collection = db[collection_name]
            return collection
    except Exception as e:
        raise ConnectionError(f"Error al conectar a MongoDB: {str(e)}")

