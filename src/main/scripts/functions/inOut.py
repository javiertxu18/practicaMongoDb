import src.main.scripts.functions.core.core as myCore
from src.main.scripts.functions.core.myExceptions import NoKaggleFound
from multipledispatch import dispatch

# preparamos el logger
logger = myCore.getLogger("inOut")
config = myCore.readConfig()


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
            for x in kaggleUrl:
                logger.debug("Descargando dataset: " + str(x) + " ....")
                activeKaggle = x
                # Descargamos los datasets
                od.download(str(x), force=True, data_dir=str(targetDir))
                logger.debug("Dataset descargado correctamente.")
        else:
            logger.debug("Descargando dataset: " + str(kaggleUrl) + " ....")
            # Descargamos los datasets
            od.download(str(kaggleUrl), force=True, data_dir=str(targetDir))
            logger.debug("Dataset descargado correctamente.")
    except ModuleNotFoundError:
        raise NoKaggleFound(str(activeKaggle))


