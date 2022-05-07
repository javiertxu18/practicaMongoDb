import os

from multipledispatch import dispatch
import src.main.scripts.functions.core.core as myCore
import src.main.scripts.functions.limpieza.limpieza as limp
import pandas as pd

# Recogemos el logger y el configParser
config = myCore.readConfig()
logger = myCore.getLogger("Cleaner")


class Cleaner:
    """
    Esta clase se va a dedicar a la limpieza de los ficheros
    """

    # ------------------ Target Inicio -------------------

    @dispatch(list)
    def setTargets(self, lst):
        """
        Sobreescribe los targets con la lista que se pase por parámetros
        """
        try:
            self.lstTargets = lst
            return True
        except Exception:
            return False

    @dispatch(str)
    def addTarget(self, newTarget):
        """
        Añade un target a la lista
        """
        try:
            self.lstTargets.append(newTarget)
            return True
        except Exception:
            return False

    @dispatch(str)
    def rmTarget(self, name):
        """
        Elimina un target cuyo valor sea igual que el string del parámetro
        """
        try:
            self.lstTargets.remove(str(name))
            return True
        except Exception:
            return False

    @dispatch(int)
    def rmTarget(self, indexPos):
        """
        Elimina un target en la posición indicada de la lista
        """
        try:
            self.lstTargets.pop(int(indexPos))
            return True
        except Exception:
            return False

    @dispatch()
    def getTargets(self):
        """
        Devuelve los targets
        """
        return self.lstTargets

    # ------------------ Target Fin -------------------

    # ------------------ toStrign Inicio -------------------

    def toString(self):
        return "Paths: " + str(self.lstTargets)

    # ------------------ toStrign Fin -------------------

    # ------------------ toPandas Inicio -------------------

    def toPandas(self, headerLine=0, separator=','):
        """
        Convierte los ficheros csv en las rutas ded self.lstTargets a dataframes de pandas.
        Return:
            - True: Si ha salido bien.
            - exit(1): Si ha habido algún error, o si no se han encontrado csv que pasar a dataframes
        """
        try:
            logger.debug("Guardando targets en la lista de dataframes como pd.DataFrame")

            # Si la lista de targets está vacía, retornamos False
            if len(self.lstTargets) <= 0:
                return False

            # Reseteamos la variable de los dataframes
            self.lstDf = []

            # Guardamos los dataframes leídos en una lista.
            for x in self.lstTargets:
                logger.debug("Guardando " + str(x) + " ....")
                self.lstDf.append(pd.read_csv(str(x), sep=separator, header=headerLine))

                # Guardamos los nombres de los ficheros en la lista
                self.lstDfNames.append(str(x).split(os.sep)[-1].split(".csv")[0])

                logger.debug("DataFrame guardado correctamente.")

            logger.debug("Los dataframes se han guardado correctamente.")
            # Una vez se han añadido los dataframes a la lista, devolvemos true
            return True
        except Exception as e:
            logger.critical("Error guardando los targets como dataframes. Error: " + str(e))
            exit(1)

    # ------------------ toPandas Fin -------------------

    # ------------------ Limpieza Inico -------------------

    def limpiarTodo(self):
        """
        Este método ejecuta los métodos necesarios para limpiar todos los CSV
        """
        logger.info("Limpiando dataframes ....")
        # Pasamos los csv de los targets a dataframes
        self.toPandas()

        logger.debug("Limpiando googleplaystore.csv")
        # Llamamos a las funciones que limpian los ficheros
        self.limpiarGooglePlayStore()  # Limpiarmos fichero de googleplaystore.csv
        logger.debug("googleplaystore.csv limpiado correctamente.")

        # Llamamos a las funciones que limpian los ficheros
        logger.debug("Limpiando googleplaystore_user_reviews.csv")
        self.limpiarGooglePlayStoreUserReviews()  # Limpiarmos fichero de googleplaystore_user_reviews.csv
        logger.debug("googleplaystore_user_reviews.csv limpiado correctamente.")

        logger.info("Limpieza realizada correctamente.")

    def limpiarGooglePlayStore(self):
        """
        Este método limpia el csv "google-play-store-apps/googleplaystore.csv"
        """

        # Borramos las rows con campos nulos
        self.lstDf[0] = self.lstDf[0].dropna(axis=0, how="any").copy()

        # Guardamos el df en una variable para trabajar más cómodo
        df = self.lstDf[0]

        # Empezamos a limpiar:

        # Borramos la última 'M' de la columna Size
        df["Size"] = limp.replaceChar(df["Size"], "M", "")
        df["Size"] = limp.replaceChar(df["Size"], "k", "")
        df["Size"] = limp.replaceChar(df["Size"], "Varies with device", "0")

        # Quitamos la ',' y el '+' de la columna Installs
        df["Installs"] = limp.replaceChar(df["Installs"], ",", "")
        df["Installs"] = limp.replaceChar(df["Installs"], "+", "")

        # Quitamos el '$' de la columna Price
        df["Price"] = limp.replaceChar(df["Price"], "$", "")

        # Eliminamos la parte de la columna a partir del carácter ';' en Genres
        df["Genres"] = limp.split(df["Genres"], ";", 0)

        # Cambiamos el formato de la fecha a otro más cómodo
        df["Last Updated"] = limp.changeDateFormat(df["Last Updated"])

        # Cambiamos el schema del df
        df = limp.updateSchema(df, ['str', 'category', 'float64', 'int64', 'float64', 'int64', 'category', 'float64',
                                    'category', 'category', 'str', 'str', 'str'])

        # Sobreescribimos el df en la lista
        self.lstDf[0] = df

    def limpiarGooglePlayStoreUserReviews(self):
        """
        Este método limpia el csv "google-play-store-apps/googleplaystore_user_reviews.csv"
        """

        # Borramos las rows con campos nulos
        self.lstDf[1] = self.lstDf[1].dropna(axis=0, how="any").copy()

        # Guardamos el df en una variable para trabajar más cómodo
        df = self.lstDf[1]

        # Empezamos a limpiar:

        # Borramos las columnas que tengan el valor 'nan'
        df.drop(df.index[df['Sentiment'] == 'nan'], inplace=True)

        # Cambiamos el scmema del DataFrame
        df = limp.updateSchema(df, ['category', 'str', 'category', 'float64', 'float64'])

        # Sobreescribimos el df en la lista
        self.lstDf[1] = df

    # ------------------ Limpieza Fin -------------------

    # ------------------ Guardar Inicio -------------------

    @dispatch(str)
    def saveOnCsv(self, targetDir):
        """
        Esta función guarda los dataframes de la lista self.lstDf en la ruta pasada por parámetros, en fichero .csv
        Parameters:
            - targetDir: Carpeta donde se van a guardar los ficheros
        Return:
            - True: Si ha funcionado correctamente
            - False: Si ha habido algún error
        """

        try:
            logger.info("Guardando dataframes a ficheros csv en " + str(targetDir))
            # Recorremos la lista y vamos guardando.
            for x in range(len(self.lstDf)):
                logger.debug("Guardando dataframe " + str(self.lstDfNames[x]) + " ....")
                self.lstDf[x].to_csv(targetDir + str(self.lstDfNames[x]) + ".csv", index=False, encoding='utf-8')
                logger.debug("Dataframe " + str(self.lstDfNames[x]) + " guardado correctamente.")

            logger.info("Dataframes guardados correctamente.")

            return True
        except Exception as e:
            print(str(e))
            return False

    # ------------------ Guardar Fin -------------------

    # ------------------ __init__ Inicio -------------------

    @dispatch()
    def __init__(self):
        # Variables
        self.lstTargets = []
        self.lstDf = []
        self.lstDfNames = []

    @dispatch(str)
    def __init__(self, strTarget):
        # Variables
        self.lstTargets = [str(strTarget)]
        self.lstDf = []
        self.lstDfNames = []

    @dispatch(list)
    def __init__(self, lstTarget):
        # Variables
        self.lstTargets = lstTarget
        self.lstDf = []
        self.lstDfNames = []

    # ------------------ __init__ Fin -------------------
