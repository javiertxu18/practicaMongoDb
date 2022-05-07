import src.main.scripts.functions.core.core as myCore
from src.main.scripts.functions.core.myExceptions import NoKaggleFound
from multipledispatch import dispatch
import os

# preparamos el logger
logger = myCore.getLogger("inOut")


@dispatch(object, str)
def getKaggleDataset(kaggleUrl, targetDir):
    """
    Descargamos de forma automática los datasets de kaggle. Si el parámetro kaggleUrl contiene una lista, se descargan
    todas las rutas que contenga.
    Parameters:
        - kaggleUrl: Contiene la/las url/s de kaggle, puede venir en string o en lsita si son varios.
        - targetDir: Ubicación destino en la que vamos a guardar los kaggle descargados
    """

    activeKaggle = kaggleUrl

    try:
        # Importamos la librería que nos va a permitir descargar datasets de kaggle
        import opendatasets as od

        if isinstance(kaggleUrl, list):
            for kUrl in kaggleUrl:
                logger.debug("Descargando dataset: " + str(kUrl) + " ....")
                activeKaggle = kUrl
                # Descargamos los datasets
                od.download(str(kUrl), force=True, data_dir=str(targetDir))
                logger.debug("Dataset descargado correctamente.")
        else:
            logger.debug("Descargando dataset: " + str(kaggleUrl) + " ....")
            # Descargamos los datasets
            od.download(str(kaggleUrl), force=True, data_dir=str(targetDir))
            logger.debug("Dataset descargado correctamente.")

        # Creamos una nueva sección en el config.ini para guardar las rutas a los ficheros en kaggle
        config = myCore.readConfig()  # Preparamos el config
        config["kaggle"] = {}  # Creamos un nueva sección en el fichero config
        config["kaggle"]["base_path"] = config["DEFAULT"]["root_path"] + os.sep + \
                                        os.sep.join(["src", "main", "res", "in", "raw", "kaggleData"])

        # Vamos añadiendo las rutas kaggles de cada carpeta
        for folder in os.listdir(config["kaggle"]["base_path"]):
            for file in os.listdir(config["kaggle"]["base_path"] + os.sep + folder):
                if file.split(".")[1] == "csv":
                    config["kaggle"][folder + "[]" + str(file.split(".")[0])] = config["kaggle"]["base_path"] + \
                                                                                  os.sep + os.sep.join([folder, file])

        # Añadimos una ruta donde se van a guardar los kaggle estandarizados
        config["kaggle"]["standarised_path"] = config["DEFAULT"]["root_path"] + os.sep + \
                                        os.sep.join(["src", "main", "res", "in", "standarised"])

        # Sobreescribimos el fichero y guardamos la info nueva
        with open(config['DEFAULT']['config_path'], 'w') as configfile:
            config.write(configfile)

    except ModuleNotFoundError:
        raise NoKaggleFound(str(activeKaggle))
