import src.main.scripts.functions.core.core as myCore
import src.main.scripts.functions.inOut as inOut
import sys

if __name__ == '__main__':
    sys.path[0]
    # Preparamos la configuración inicial
    myCore.coreInitConfig(str(__file__))

    # Recogemos el logger y el configParser
    config = myCore.readConfig()
    logger = myCore.getLogger("main")

    logger.info("Inicio programa")

    # Descargamos el dataset
    kaggleUrls = [
        "https://www.kaggle.com/datasets/lava18/google-play-store-apps?resource=download",
        "https://www.kaggle.com/datasets/lava18/google-play-store-apps?resource=download&s"
        "elect=googleplaystore_user_reviews.csv"]  # Url de datasets
    targetDir = config["DEFAULT"]["res_path"] + "/in/kaggleData/"  # Ruta donde vamos a guardar los datasets
    inOut.getKaggleDataset(kaggleUrls, targetDir)
