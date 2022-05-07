from multipledispatch import dispatch
import pymongo
import src.main.scripts.functions.core.core as myCore
from src.main.scripts.functions.core.myExceptions import NotSameLenght

"""
En este fichero van a ir las fucniones asociadas a mongoDb
"""

# Recogemos el logger y el configParser
config = myCore.readConfig()
logger = myCore.getLogger("Conn Manager")


# ------------------ Funciones de carga Inicio -------------------

@dispatch(pymongo.mongo_client.MongoClient, list, list, list)
def pandasToMongo(mongoConn, lstDf, lstDbNames, lstCollNames):
    """
    Esta función guarda la información de un pandas.DataFrame en mongoDb. Cada dataframe se va a guardar en la base
    de datos y colección que esté en la misma posición que él.
    Parameters:
        - mongoConn: Variable de conexión a mongoDB pymongo.mongo_client.MongoClient
        - lstDf: Lista de dataframes de pandas que queremos guardar en mongo
        - lstDbNames: Lista de nombres de las bases de datos en los que vamos a guardar los dataframes
        - lstCollNames: Lista de nombres de las colecciones en las que vamos a guardar los dataframes
    """

    logger.info("Guardando información ded dataframes a mongoDB ....")

    # Comprobamos que todas las listas tienen el mismo tamaño
    logger.debug("Comprobando que las 3 listas tienen el mismo tamaño ....")
    if len(lstDbNames) != len(lstCollNames) or len(lstDf) != len(lstCollNames):
        logger.critical("Las listas no tienen el mismo tamaño.")
        raise NotSameLenght([lstDf, lstDbNames, lstCollNames])
    logger.debug("Las listas tienen el mismo tamaño.")

    for x in range(len(lstDf)):
        logger.debug("Guardando contenido " + str(x) + " en db " + str(lstDbNames[x]) + " y colección " +
                     str(lstCollNames[x]) + " ....")
        db = mongoConn[str(lstDbNames[x])]  # Creamos si no existe la base de datos
        coll = db[str(lstCollNames[x])]  # Creamos si no existe la colección
        coll.insert_many(lstDf[x].to_dict("records"))  # Insertamos el dataframe pasado a diccionario
        logger.debug("Contenido " + str(x) + " guardado correctamente.")

    logger.info("Información guardada en mongoDB correctamente.")

# ------------------ Funciones de carga Fin -------------------

# ------------------ Comprobaciones Inicio -------------------


@dispatch()
def getConnInfo():
    # Actualizamos config
    global config
    config = myCore.readConfig()
    # Preparamos los datos de conexión a la base de datos mongoDb
    try:
        # Intentamos recuperar los datos del fichero config.ini
        logger.info("Recuperando datos de conexión a mongoDB ....")
        return [str(config["mongodb"]["name"]), str(config["mongodb"]["host"]), str(config["mongodb"]["port"])]
    except Exception:
        # En caso de no estar saltará el error, por lo que pedimos los datos de conexión al usuario
        logger.debug("No se han encontrado datos de conexión en config.ini, solicitando info a usuario ....")
        print("No se han encontrado datos de conexión a mongoDB, por favor, insértelos ahora:\n")
        name = input("\t- Nombre de conexión: ")
        host = input("\t- Host de conexión [localhost]: ")
        port = input("\t- Port de conexión [27017]: ")

        # Guardamos la info en config.ini
        config["mongodb"] = {}
        config["mongodb"]["name"] = str(name)
        config["mongodb"]["host"] = str(host)
        config["mongodb"]["port"] = str(port)

        with open(config['DEFAULT']['config_path'], 'w') as configfile:
            config.write(configfile)

        logger.debug("Información solicitada y guardada correctamente.")
        logger.info("Datos de conexión recuperados correctamente.")

        # Retornamos la info en la lista
        return [str(config["mongodb"]["name"]), str(config["mongodb"]["host"]), str(config["mongodb"]["port"])]

# ------------------ Comprobaciones Fin -------------------
