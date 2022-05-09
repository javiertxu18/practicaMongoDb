import os
import json
from multipledispatch import dispatch
import pymongo
import src.main.scripts.functions.core.core as myCore

"""
Aquí van a ir las funciones para realizar las consultas a mongodb de las prácticas.
"""

# Recogemos el logger y el configParser
config = myCore.readConfig()  # Para trabajar con config.ini
logger = myCore.getLogger("main")  # Para guardar logs

# ------------------ Consultas Inicio -------------------


def saveQueryJson(cursor, fileObj):
    """
    Esta función guarda la query de mongo en el json pasado por parámetros
    Parameters:
        - cursor: Cursor del que se va a sacar la información para guardar en el json
        - fileObj: Fichero json donde se va a guardar el resultado de la query.
    Return:
        - True si todo_ ha ido bien.
        - False: Si ha habido algún error.
    """
    try:
        logger.debug("Guardando información de mongo a fichero json ....")

        with open(fileObj, 'w') as file:
            file.write('[')
            for document in cursor:
                file.write(json.dumps(document))
                file.write(',')
            file.write(']')

        logger.debug("Información guardada correctamente.")

        # Retornamos True si todo_ ha ido bien
        return True
    except Exception as e:
        logger.error("Error a la hora de guardar la info del json en " + str(fileObj) + ". Error: " + str(e))
        return False


@dispatch(pymongo.mongo_client.MongoClient)
def consultasPracticas(mongoConn):
    """
    Esta fucnión contiene las consultas que se piden en la práctica.
    """
    global config
    config = myCore.readConfig()  # Actualizamos

    # Añadimos ruta de la carpeta donde vamos aguardar las consultas a config.ini
    config["queries"] = {}
    config["queries"]["folder_path"] = config["DEFAULT"]["res_path"] + os.sep + os.sep.join(["out", "resultConsultas"])

    # Sobreescribimos el fichero y guardamos la info nueva
    with open(config['DEFAULT']['config_path'], 'w') as configfile:
        config.write(configfile)

    # Preparamos las colecciones
    db = mongoConn["googleStore"]
    colStore = db["googleplaystore"]
    colUser = db["googleplaystore_user_reviews"]

    logger.info("Empezamos con las consultas ....")

    # ------------------ Ejer 1 Inicio

    logger.debug("Consulta 1 Inicio ....")

    print("\nEjercicio 1: ¿Cuántas User Reviews (del csv Googleplaystore_user_reviews) tienen cada una de las Apps del "
          "CSV GooglePlayStore?\n")  # Enunciado

    # Mostramos una parte por consola
    res = colUser.aggregate([
        {'$group': {"_id": "$App", "Cant User Reviews": {'$sum': 1}}},
        {"$sort": {"_id": 1}},
        {"$limit": 3}
    ])
    for x in res:
        print(x)

    print("\t.....\nConsulta completa en la siguiente ruta: " + str(config["queries"]["folder_path"]))

    # Guardamos consulta en carpeta de consultas
    cursor = colUser.aggregate([
        {'$group': {"_id": "$App", "Cant User Reviews": {'$sum': 1}}},
        {"$sort": {"_id": 1}}
    ])  # Cursor con la consulta sin el limit
    saveQueryJson(cursor, str(config["queries"]["folder_path"] + os.sep + "consulta1.json"))  # Llamamos a función.

    logger.debug("Consulta 1 Fin.")

    # ------------------ Ejer 1 Fin

    # ------------------ Ejer 2 Inicio

    logger.debug("Consulta 2 Inicio ....")

    print("\nEjercicio 2: Del User Reviews, ¿cuántos tipos de sentimientos hay y su frecuencia? Mostrar además, la "
          "aplicación que recibe más comentarios por tipo de sentimiento.\n")  # Enunciado

    # Premaramos consulta
    res = colUser.aggregate([
        {'$group': {"_id": "$Sentiment", "Frecuencia": {'$sum': 1}, "App más frecuente": {"$max": "$App"}}},
        {"$sort": {"_id": pymongo.DESCENDING}},
        {"$limit": 3}
    ])
    # Mostramos consulta por consola
    for x in res:
        print(x)

    print("\t.....\nConsulta completa en la siguiente ruta: " + str(config["queries"]["folder_path"]))

    # Guardamos consulta en carpeta de consultas
    cursor = colUser.aggregate([
        {'$group': {"_id": "$Sentiment", "Frecuencia": {'$sum': 1}, "App más frecuente": {"$max": "$App"}}},
        {"$sort": {"_id": pymongo.DESCENDING}}
    ])  # Cursor con la consulta sin el limit
    saveQueryJson(cursor, str(config["queries"]["folder_path"] + os.sep + "consulta2.json"))  # Llamamos a función.

    logger.debug("Consulta 2 Fin.")

    # ------------------ Ejer 2 Fin

    # ------------------ Ejer 3 Inicio

    logger.debug("Consulta 3 Inicio ....")

    print("\nEjercicio 3: Calcular la media de Rating por categoría cuyas Reviews son mayores o iguales a "
          "diez mil.\n")  # Enunciado

    # Premaramos consulta
    res = colStore.aggregate([
        {"$match" : {"Reviews" : {"$gt": 10000}}},
        {'$group': {"_id": "$Category", "avg Rating": {'$avg': "$Rating"}}},
        {"$limit": 3}
    ])
    for x in res:
        print(x)

    print("\t.....\nConsulta completa en la siguiente ruta: " + str(config["queries"]["folder_path"]))

    # Guardamos consulta en carpeta de consultas
    cursor = colStore.aggregate([
        {"$match" : {"Reviews" : {"$gt": 10000}}},
        {'$group': {"_id": "$Category", "avg Rating": {'$avg': "$Rating"}}}
    ])  # Cursor con la consulta sin el limit
    saveQueryJson(cursor, str(config["queries"]["folder_path"] + os.sep + "consulta3.json"))  # Llamamos a función.

    logger.debug("Consulta 3 Fin.")

    # ------------------ Ejer 3 Fin

    # ------------------ Ejer 4 Inicio

    logger.debug("Consulta 4 Inicio ....")

    print("\nEjercicio 4: Añadir un campo nuevo (usando la función Split, en el que se separe el año de la "
          "fecha.\n")  # Enunciado

    # Preparamos consulta
    res = colStore.aggregate([
        {"$addFields": {"Fecha separada": {"$substr": ["$Last Updated", 0, 4]}}},
        {"$limit": 3}
    ])
    for x in res:
        print(x)

    print("\t.....\nConsulta completa en la siguiente ruta: " + str(config["queries"]["folder_path"]))

    # Guardamos consulta en carpeta de consultas
    cursor = colStore.aggregate([
        {"$addFields": {"Fecha separada": {"$substr": ["$Last Updated", 0, 4]}}}
    ])  # Cursor con la consulta sin el limit
    saveQueryJson(cursor, str(config["queries"]["folder_path"] + os.sep + "consulta4.json"))  # Llamamos a función.

    logger.debug("Consulta 4 Fin.")

    # ------------------ Ejer 4 Fin

    # ------------------ Ejer 5 Inicio

    logger.debug("Consulta 5 Inicio ....")

    print("\nEjercicio 5: Mostrar el número de Apps por año de actualización y la media del precio.\n")  # Enunciado

    # Preparamos consulta
    res = colStore.aggregate([
        {"$addFields": {"Fecha separada": {"$substr": ["$Last Updated", 0, 4]}}},
        {"$group": {"_id": "$Fecha Separada", "avg Precio": {"$avg": "$Price"}}},
        {"$limit": 3}
    ])
    for x in res:
        print(x)

    print("\t.....\nConsulta completa en la siguiente ruta: " + str(config["queries"]["folder_path"]))

    # Guardamos consulta en carpeta de consultas
    cursor = colStore.aggregate([
        {"$addFields": {"Fecha separada": {"$substr": ["$Last Updated", 0, 4]}}},
        {"$group": {"_id": "$Fecha Separada", "avg Precio": {"$avg": "$Price"}}},
    ])  # Cursor con la consulta sin el limit
    saveQueryJson(cursor, str(config["queries"]["folder_path"] + os.sep + "consulta5.json"))  # Llamamos a función.

    logger.debug("Consulta 5 Fin.")

    # ------------------ Ejer 5 Fin

    # ------------------ Ejer 6 Inicio

    logger.debug("Consulta 6 Inicio ....")

    print("\nEjercicio 6: Clasificar los Ratings por grupos: 1-2, 2-3, 3-4, 4-5 con el "
          "recuento de Apps.\n")  # Enunciado

    # Preparamos consulta
    res = colStore.aggregate([
        {"$bucket": {
            "groupBy": "$Rating",
            "boundaries": [1.0, 2.0, 3.0, 4.0, 5.1],
            "default": "Out",
            "output": {
                "Recuento Ratings/Apps": {"$sum": 1}
            }
        }}
    ])
    for x in res:
        print(x)

    print("\nConsulta completa en la siguiente ruta: " + str(config["queries"]["folder_path"]))

    # Guardamos consulta en carpeta de consultas
    cursor = colStore.aggregate([
        {"$bucket": {
            "groupBy": "$Rating",
            "boundaries": [1.0, 2.0, 3.0, 4.0, 5.1],
            "default": "Out",
            "output": {
                "Recuento Ratings/Apps": {"$sum": 1}
            }
        }}
    ])  # Cursor con la consulta sin el limit
    saveQueryJson(cursor, str(config["queries"]["folder_path"] + os.sep + "consulta6.json"))  # Llamamos a función.

    logger.debug("Consulta 6 Fin.")

    # ------------------ Ejer 6 Fin

    logger.info("Fin de consultas.")

    print("\nRevisar el fichero /.log para obtener información extendida del programa y su funcionamiento.")

# ------------------ Consultas Fin -------------------
