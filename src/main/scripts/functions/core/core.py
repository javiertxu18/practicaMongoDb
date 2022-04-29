import logging, configparser, os, sys
from multipledispatch import dispatch
from src.main.scripts.functions.core.myExceptions import NoAccessFromFile, NoBinFolderFound


# -------------------------------------- coreInitConfig Inicio ---------------------------------

@dispatch(str)
def coreInitConfig(initPath):
    """
    Conjunto de funciones que preparan el entorno para trabajar cómodamente. Se preparan las siguientes cosas:

        - Acceso: Controlamos para que solo tengan acceso a esta función desde las carpetas que queramos.
        - rootPath: Se prepara para que el valor de esta variable, sea el path absoluto a la raíz del proyecto.
        - ConfigParser: Para guardar información en el archivo config.ini
        - Logger: Una herramienta que nos permite guardar un log de lo que vayamos necesitando.

    :return:
    """

    # Controlamos el acceso a la función, para que solo se ejecute en los .py que queramos
    accessControl(initPath)

    # Preparamos rootPath
    rootPath = setRootPath(initPath)

    # Preparamos el ConfigParser
    initConfigParser(rootPath)

    # Iniciamos el logger
    loggerInit = getLogger("INIT")
    loggerInit.info("Inicio de logger.")


@dispatch(str)
def accessControl(initPath):
    """
    Controlamos el acceso a la función, para que solo se ejecute en los .py que queramos
    Dentro de la lista, guardaremos otra lista con 2 elementos, el primero es la carpeta del
    fichero con permisos de ejecución, y el segundo, el nombre del fichero
    """

    pyList = [["bin", "main.py"], ["scripts", "+.py"]]
    if str(initPath).split(os.sep)[-2:] not in pyList:
        raise NoAccessFromFile(f"Solo puedes ejecutar esta función desde los ficheros con acceso.")


@dispatch(str)
def setRootPath(mainPath):
    """
    Prepara el valor de la variable de sys.path[0] para que sea la ruta absoluta del proyecto.
    :return:
    """
    try:
        # Sacamos la posición de la carpeta bin de la lista
        binIndex = int(os.path.abspath(os.path.dirname(mainPath)).split(os.sep).index("bin"))

        # Sacamos la ruta root y la retornamos
        rootPath = str(os.sep).join(os.path.abspath(os.path.dirname(mainPath)).split(os.sep)[:binIndex])

        # Actualizamos el valor de sys.path[0] con el path absoluto del proyecto
        sys.path.insert(0, rootPath)

        return rootPath
    except:
        raise NoBinFolderFound("No se ha encontrado la carpeta 'bin' en la ruta " + str(mainPath))


@dispatch(str)
def initConfigParser(rootPath, logger_level=30):
    """
    Configuración inicial de el ConfigParser para poder leer y escribir en el fichero config.ini
    :parameters:
        rootPath: Path de la carpeta del proyecto
        logger_level: Nivel del logger, por defecto 30
    :return:
        - True: Si todo_ ha ido bien
        - exit(1): Si algo ha ido mal
    """
    try:
        # Preparamos el configParser
        conf = configparser.ConfigParser()
        # Leemos el fichero config.ini en la carpeta raíz.
        conf.read(str(rootPath) + os.sep + "config.ini")

        # Escribimos en el configParser (No en el fichero)
        conf['DEFAULT']['os_name'] = os.name
        conf['DEFAULT']['root_path'] = rootPath
        conf['DEFAULT']['config_path'] = str(rootPath) + os.sep + "config.ini"
        conf['DEFAULT']['res_path'] = str(rootPath) + f"{os.sep}src{os.sep}main{os.sep}res"
        conf['DEFAULT']['logger_level'] = str(logger_level)  # Nivel del logger por defecto

        # Sobreescribimos el fichero y guardamos la info nueva
        with open(conf['DEFAULT']['config_path'], 'w') as configfile:
            conf.write(configfile)

        return True

    except Exception as e:
        # Este error lo mostramos por pantalla ya que el logger no está configurado aún.
        print("Error en la configuración inicial del ConfiParser " + str(e))
        exit(1)


@dispatch()
def readConfig():
    """
    Devuelve el ConfigParser para poder trabajar con el fichero config.ini
    Return:
        configparser.ConfigParser: objeto
    """
    try:
        # Preparamos el configParser
        conf = configparser.ConfigParser()
        # Leemos el fichero config.ini
        conf.read(sys.path[0] + os.sep + "config.ini")
        # Retornamos el configParser
        return conf
    except Exception as e:
        logger = getLogger("inOutFunctions")
        logger.error(str(e))
        return False


@dispatch()
def setLogger():
    """
    Prepara el logger, su formato y la ubicación del archivo .log
    Parameters:
        - rootPath: Variable que contiene la ruta absoluta de la raíz del proyecto
    Return:
        - True: Si todo_ ha ido bien
        - exit(1): Si ha habido algún error
    """
    try:
        logging.basicConfig(
            filename=sys.path[0] + "/.log",  # Fichero donde vamos a guardar la info
            filemode="a",  # Modo en el que vamos a guardar la info (append)
            format='%(asctime)s %(levelname)s(%(name)s) '
                   '%(filename)s:line(%(lineno)s) '
                   '-> %(message)s',  # Formato de la info
            level=logging.INFO,  # Level por defecto
            datefmt='%Y-%m-%d %H:%M:%S')  # Formato de fecha
        return True
    except Exception as e:
        print("Error configurando el logger: " + str(e))
        exit(1)


@dispatch(str)
def getLogger(name):
    """
    Devuelve el logger
    Parameters:
        - name: Nombre del logger
    Return:
        - logging.Logger: Objeto
    """

    try:
        # Si está en el config.ini se coje de ahí, sino se pone el nivel por defecto
        config = readConfig()
        level = int(config["DEFAULT"]["logger_level"])
    except:
        level = logging.ERROR

    # Preparamos el logger
    logger = logging.getLogger(str(name))
    setLogger()
    logger.setLevel(10)

    # Añadimos un Handler al logger para que muestre por consola los mensajes
    console = logging.StreamHandler()
    console.setLevel(level)

    # Preparamos el formato del Handler y lo añadimos
    formato = logging.Formatter('%(asctime)s %(levelname)s(%(name)s) '
                               '%(filename)s:line(%(lineno)s) '
                               '-> %(message)s')
    console.setFormatter(formato)

    # Añadimos el handler al logger y lo retornamos
    logger.addHandler(console)

    return logger

# -------------------------------------- coreInitConfig Fin ---------------------------------
