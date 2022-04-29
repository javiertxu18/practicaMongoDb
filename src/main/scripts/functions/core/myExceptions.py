"""
Aquí guardaré mis propias excepciones, y podré importarlas y utilizarlas en diferentes .py
"""


class NoAccessFromFile(Exception):
    """
    Causa de la Excepción:
    Cuando se ejecuta una función desde un fichero que no está en la lista
    """

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


class NoBinFolderFound(Exception):
    """
    Causa de la Excepción:
    Cuando no se encuentra la carpeta bin en la ruta
    """

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message
