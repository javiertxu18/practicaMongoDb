import configparser
import logging
import os

from multipledispatch import dispatch
from src.main.scripts.functions.core.myExceptions import NoAccessFromFile, CoreConfigError, \
    ProjectPathNotFound


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
        - True: Si todo_ ha ido bien
        - False: Si ha habido algún problema
    """
    try:
        # Controlamos el acceso a la función, para que solo se ejecute en los .py que queramos
        accessControl(initPath)

        # Preparamos el ConfigParser
        initConfigParser()

        # Iniciamos el logger para comprobar que todo_ ha ido bien
        loggerInit = getLogger("INIT")
        loggerInit.info("Inicio de  logger.")

        # Retorna true porque todo_ ha ido bien
        return True
    except Exception as e:
        # Si salta alguna excepción, mostrar error
        raise CoreConfigError(e)


@dispatch(str)
def accessControl(initPath):
    """
    Controlamos el acceso a la función, para que solo se ejecute en los .py que queramos
    Dentro de la lista, guardaremos otra lista con 2 elementos, el primero es la carpeta del
    fichero con permisos de ejecución, y el segundo, el nombre del fichero
    """

    pyList = [["bin", "main.py"]]
    if str(initPath).split(os.sep)[-2:] not in pyList:
        raise NoAccessFromFile(f"Solo puedes ejecutar esta función desde los ficheros con acceso.")


@dispatch()
def getRootPath():
    """
    Devuelve el root path de todo_ aquel programa que se haya ejecutado desde dentro de bin
    :return:
        - String: La ruta absoluta de la carpeta del proyecto
    """
    try:
        mainPath = str(os.getcwdb().decode('utf-8'))
        try:
            # Sacamos la posición de la carpeta bin de la lista
            binIndex = int(mainPath.split(os.sep).index("bin"))
        except Exception:
            # En caso de no encontrar la carpeta bin, buscamos la src
            binIndex = int(mainPath.split(os.sep).index("src"))

        # Sacamos la ruta root y la retornamos
        return str(os.sep).join(mainPath.split(os.sep)[:binIndex])

    except Exception as e:
        raise ProjectPathNotFound("No se ha encontrado la ruta del proyecto en " + str(os.getcwdb().decode('utf-8')) +
                                  ". Error: " + str(e))


def initConfigParser(rootPath=getRootPath(), logger_level=30):
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
        conf.read(getRootPath() + os.sep + "config.ini")
        # Retornamos el configParser
        return conf
    except Exception as e:
        print("Error preparando el ConfigParser. Error: " + str(e))
        exit(1)
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

        try:
            config = readConfig()
            logPath = config["DEFAULT"]["root_path"] + os.sep + ".log"
        except:
            # La primera ejecución pasará por aquí
            logPath = getRootPath() + os.sep + ".log"

        logging.basicConfig(
            filename=logPath,  # Fichero donde vamos a guardar la info
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
    logger.setLevel(10)  # Para que se guarde todo_ en el .log

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
