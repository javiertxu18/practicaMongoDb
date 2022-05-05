import pymongo
import src.main.scripts.functions.core.core as myCore
from multipledispatch import dispatch
from src.main.scripts.functions.core.myExceptions import ConnNotFound, DuplicatedConnName


# Recogemos el logger y el configParser
config = myCore.readConfig()
logger = myCore.getLogger("Conn Manager")


class ConnManager:
    """
    Este objeto se encarga de gestionar las conexiones a las distintas bases de datos si las hubiera.
    """

    # ------------------ Métodos de conexión Inicio -------------------

    # ------------------ Crear conexión Inicio -------------------

    def newConn_MongoDB(self, name, host="localhost", port=27017):
        """
        Este método crea una nueva conexión con MongoDb
        Parameters:
            - host: Dirección donde está ubicado mongoDB
            - port: Puerto por el que nos conectaremos a mongoDB
        Return:
            - object: Devuelve la conexión
            - None: Devuelve vacío
        """

        try:
            logger.info("Creando nueva conexión a MongoDB con id " + str(self.lastId + 1) + " y nombre " + str(name))

            # Comprobamos que no existe otra conexión con el nombre introducido por parámetros
            for x in range(len(self.lstConnInfo)):
                if str(name) == str(self.lstConnInfo[x][3]):
                    raise DuplicatedConnName(name)

            newId = self.lastId + 1

            # Guardamos la conexión en una lista junto a la información de la misma
            self.lstConnInfo.append([newId, pymongo.MongoClient(host, port), "MongoDB", str(name)])

            self.lastId += 1  # Incrementamos el lastId

            logger.info("Conexión a mongoDb con id " + str(newId) + " creada correctamente.")

            # Retornamos la conexión
            return self.getConn(newId)
        except Exception as e:
            logger.error("Error al crear conexión. Error: " + str(e))
            return None

    # ------------------ Crear conexión Fin -------------------

    # ------------------ Obtener conexión Inicio -------------------

    @dispatch(int)
    def getConn(self, connId):
        """
        Esta función retorna la conexión asociada al id insertado por parámetros
        Parameters:
            - id: La id de la conexión que vamos a retornar
        Return:
            - object: Devuelve el objeto de conexión a x base de datos.
        """
        try:
            logger.debug("Recuperando conexión con id " + str(connId))
            for x in self.lstConnInfo:
                if x[0] == int(connId):
                    logger.debug("Conexión con id " + str(connId) + " encontrada y retornada.")
                    return x[1]

            # Si no se ha encontrado, saltamos excepción
            raise ConnNotFound(connId)
        except Exception as e:
            logger.error("No se ha encontrado la conexión con id " + str(connId) + ". Error: " + str(e))
            logger.error("Mostrando conexiones guardadas: " + self.toString())
            pass

    @dispatch(str)
    def getConn(self, connName):
        """
        Esta función retorna la conexión asociada al nombre insertado por parámetros
        Parameters:
            - connName: La id de la conexión que vamos a retornar
        Return:
            - object: Devuelve el objeto de conexión a x base de datos.
        """
        try:
            logger.debug("Recuperando conexión con nombre " + str(connName))
            for x in self.lstConnInfo:
                if x[3] == str(connName):
                    logger.debug("Conexión con nombre " + str(connName) + " encontrada y retornada.")
                    return x[1]

            # Si no se ha encontrado, saltamos excepción
            raise ConnNotFound(connName)
        except Exception as e:
            logger.error("No se ha encontrado la conexión con nombre " + str(connName) + ". Error: " + str(e))
            logger.error("Mostrando conexiones guardadas: " + self.toString())
            pass

    @dispatch(pymongo.mongo_client.MongoClient)
    def getConn(self, conn):
        """
        Esta función retorna la conexión pasada por parámetros si existe
        Parameters:
            - conn: Conexión de tipo pymongo.mongo_client.MongoClient
        Return:
            - object: Devuelve el objeto de conexión a x base de datos.
        """
        try:
            logger.debug("Recuperando conexión " + str(conn))
            for x in self.lstConnInfo:
                if x[1] == conn:
                    logger.debug("Conexión " + str(conn) + " encontrada y retornada.")
                    return x[1]

            # Si no se ha encontrado, saltamos excepción
            raise ConnNotFound(conn)
        except Exception as e:
            logger.error("No se ha encontrado la conexión " + str(conn) + ". Error: " + str(e))
            logger.error("Mostrando conexiones guardadas: " + self.toString())
            pass

    # ------------------ Obtener conexión Fin -------------------

    # ------------------ Métodos de conexión Fin -------------------

    # ------------------ toString Inicio -------------------

    def toString(self):
        """
        Devuelve un string con la información de las conexiones existentes
        """

        if len(self.lstConnInfo) > 0:
            dev = "Actualmente hay " + str(len(self.lstConnInfo)) + " conexion/es:"

            for x in range(len(self.lstConnInfo)):
                dev += f"\n\t- Id: {self.lstConnInfo[x][0]} || Nombre: {self.lstConnInfo[x][3]} || Tipo:" \
                       f" {self.lstConnInfo[x][2]} || Conexión: {self.lstConnInfo[x][1]}"
        else:
            dev = "Actualmente no hay ninguna conexión establecida."

        return dev

    # ------------------ toString Fin -------------------

    # ------------------ Constructores Inicio -------------------

    def __init__(self):
        logger.debug("Instanciando ConnManager ....")
        self.lstConnInfo = []  # Lista en la que vamos a guardar la información de las conexiones realizadas.
        self.lastId = -1  # Id que se va a ir incrementando cada conexión que creemos.
        logger.debug("ConnManager instanciado correctamente.")

    # ------------------ Constructores Fin -------------------
