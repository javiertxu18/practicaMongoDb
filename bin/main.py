import src.main.scripts.functions.core.core as myCore
import src.main.scripts.functions.inOut as inOut
from src.main.scripts.objects.limpieza.Cleaner import Cleaner
import os, sys

if __name__ == '__main__':
    # Preparamos la configuración inicial
    myCore.coreInitConfig(str(__file__))

    # Recogemos el logger y el configParser
    config = myCore.readConfig()  # Para trabajar con config.ini
    logger = myCore.getLogger("main")  # Para guardar logs

    logger.info("Inicio programa")

    # Descargamos los DataSets
    kaggleUrls = [
        "https://www.kaggle.com/datasets/lava18/google-play-store-apps?select=googleplaystore.csv",
        "https://www.kaggle.com/datasets/lava18/google-play-store-apps?resource=download&s"
        "elect=googleplaystore_user_reviews.csv"]  # Url de datasets
    targetDir = config["DEFAULT"]["res_path"] + "/in/kaggleData/"  # Ruta donde vamos a guardar los datasets
    inOut.getKaggleDataset(kaggleUrls, targetDir)

    # Limpiamos los CSV descargados
    cleaner = Cleaner()

