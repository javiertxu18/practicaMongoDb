from multipledispatch import dispatch
import src.main.scripts.functions.core.core as myCore
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
        except Exception as e:
            return False

    @dispatch(str)
    def addTarget(self, newTarget):
        """
        Añade un target a la lista
        """
        try:
            self.lstTargets.append(newTarget)
            return True
        except Exception as e:
            return False

    @dispatch(str)
    def rmTarget(self, name):
        """
        Elimina un target cuyo valor sea igual que el string del parámetro
        """
        try:
            self.lstTargets.remove(str(name))
            return True
        except Exception as e:
            return False

    @dispatch(int)
    def rmTarget(self, indexPos):
        """
        Elimina un target en la posición indicada de la lista
        """
        try:
            self.lstTargets.pop(int(indexPos))
            return True
        except Exception as e:
            return False

    @dispatch()
    def getTargets(self):
        """
        Devuelve los targets
        """
        return self.lstTargets

    # ------------------ Target Fin -------------------

    def __init__(self):
        # Variables
        self.lstTargets = []
