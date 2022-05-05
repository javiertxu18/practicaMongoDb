"""
Aquí guardaré mis propias excepciones, y podré importarlas y utilizarlas en diferentes .py
"""
import pymongo


class NoAccessFromFile(Exception):
    """
    Causa de la Excepción:
    Cuando se ejecuta una función desde un fichero que no está en la lista
    """

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


class NoBinFolderFound(Exception):
    """
    Causa de la Excepción:
    Cuando no se encuentra la carpeta bin en la ruta
    """

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


class ProjectPathNotFound(Exception):
    """
    Causa de la Excepción:
    No se ha encontrado la ruta del proyecto
    """

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


class NoKaggleFound(Exception):
    """
    Causa de la Excepción:
    Cuando se intenta descargar un kaggle que no existe
    """

    def __init__(self, kaggleUrl):
        self.message = "No se ha encontrado el kaggle en la ruta '" + str(kaggleUrl) + \
                       "'. Comprueba inOut.getKaggleDatasets()"

    def __str__(self):
        return self.message


class CoreConfigError(Exception):
    """
    Causa de la Excepción:
    Cuando se intenta descargar un kaggle que no existe
    """

    def __init__(self, desc):
        self.message = "Ha habido un error configurando el core: " + str(desc)

    def __str__(self):
        return self.message


class ConnNotFound(Exception):
    """
    Causa de la Excepción:
    No se ha encontrado el Id o Nombre de la conexión que estamos buscando.
    """

    def __init__(self, tipo):
        if isinstance(tipo, int):
            self.message = "No se ha encontrado la conexión con id " + str(tipo)
        elif isinstance(tipo, str):
            self.message = "No se ha encontrado la conexión con nombre " + str(tipo)
        elif isinstance(tipo, pymongo.mongo_client.MongoClient):
            self.message = "No se ha encontrado la conexión " + str(tipo)

    def __str__(self):
        return self.message


class DuplicatedConnName(Exception):
    """
    Causa de la Excepción:
    No se ha encontrado el Id o Nombre de la conexión que estamos buscando.
    """

    def __init__(self, nombre):
        self.message = "Ya existe una conexión con nombre " + str(nombre) + " no pueden duplicarse."

    def __str__(self):
        return self.message


class NotSameLenght(Exception):
    """
    Causa de la Excepción:
    Los elementos no tiene el mismo len
    """

    def __init__(self, lstElem):
        self.message = "Los siguientes elementos no tienen el mismo len(): " + str(lstElem)

    def __str__(self):
        return self.message
