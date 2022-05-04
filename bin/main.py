import src.main.scripts.functions.core.core as myCore
import src.main.scripts.functions.inOut.in_.kaggle as inKaggle
from src.main.scripts.objects.limpieza.Cleaner import Cleaner
import src.main.scripts.functions.limpieza.limpieza as limp
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
    targetDir = config["DEFAULT"]["res_path"] + os.sep + str(os.sep).join(["in", "raw", "kaggleData"])   # Ruta de guardado
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

    # Llamamos a la función que limpia todos los CSV
    cleaner.limpiarTodo()

    # Guardamos los dataframes en csv
    cleaner.saveOnCsv(config["kaggle"]["standarised_path"] + os.sep)

    # ------------------ Limpieza de CSV Fin -------------------

    logger.info("Fin programa")
