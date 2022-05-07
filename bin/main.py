import src.main.scripts.functions.core.core as myCore
import src.main.scripts.functions.inOut.in_.kaggle as inKaggle
import src.main.scripts.functions.inOut.out_.toMongo as mongoFunc
import src.main.scripts.functions.consultas.consultasMongoDb as consultasMongo
from src.main.scripts.objects.limpieza.Cleaner import Cleaner
from src.main.scripts.objects.db.ConnManager import ConnManager
import os


if __name__ == '__main__':
    # Preparamos la configuración inicial
    myCore.coreInitConfig(str(__file__))

    # Recogemos el logger y el configParser
    config = myCore.readConfig()  # Para trabajar con config.ini
    logger = myCore.getLogger("main")  # Para guardar logs

    logger.info("Inicio programa")

    # ------------------ Descargar Datasets Inicio -------------------

    # Descargamos los DataSets
    kaggleUrls = [
        "https://www.kaggle.com/datasets/lava18/google-play-store-apps?select=googleplaystore.csv",
        "https://www.kaggle.com/datasets/lava18/google-play-store-apps?resource=download&s"
        "elect=googleplaystore_user_reviews.csv"]  # Url de datasets
    targetDir = config["DEFAULT"]["res_path"] + os.sep + str(os.sep).join(["in", "raw", "kaggleData"])  # savePath
    inKaggle.getKaggleDataset(kaggleUrls, targetDir)

    # ------------------ Descargar Datasets Fin -------------------

    # ------------------ Limpieza de CSV Inicio -------------------
    config = myCore.readConfig()  # Actualizamos la variable config

    # Preparamos la lista que contiene las url de los csv
    lstCsvPaths = list([
        config["kaggle"]['google-play-store-apps[]googleplaystore'],
        config["kaggle"]['google-play-store-apps[]googleplaystore_user_reviews']
    ])

    cleaner = Cleaner(lstCsvPaths)  # Instanciamos la clase Cleaner
    cleaner.limpiarTodo()  # Llamamos a la función que limpia todos los CSV

    # ------------------ Limpieza de CSV Fin -------------------

    # ------------------ Carga de datos Inicio -------------------

    # ------------------ Carga de datos en CSV Inicio

    # Guardamos los dataframes en csv
    cleaner.saveOnCsv(config["kaggle"]["standarised_path"] + os.sep) # Csv

    # ------------------ Carga de datos en CSV Fin

    # ------------------ Carga de datos en MongoDB Inicio

    connData = mongoFunc.getConnInfo() # Preparamos los datos de conexión
    connManager = ConnManager()  # Llamamos a nuestro objeto que gestiona las conexiones a bases de datos
    conn = connManager.newConn_MongoDB(connData[0], host=connData[1], port=int(connData[2]))  # Creamos una conexión
    mongoFunc.pandasToMongo(conn, cleaner.lstDf, ["googleStore", "googleStore"],
                            ["googleplaystore", "googleplaystore_user_reviews"])  # Guardamos los dataframes

    # ------------------ Carga de datos en MongoDB Fin

    # ------------------ Carga de datos Fin -------------------

    # ------------------ Consultas práctica Inicio -------------------

    consultasMongo.consultasPracticas(conn)

    # ------------------ Consultas práctica Fin -------------------

    logger.info("Fin programa")
