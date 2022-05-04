import pandas as pd
from multipledispatch import dispatch

"""
En este fichero van a ir las funciones relacionadas con la limpieza de datos.
"""


# ------------------ Transformaciones Inicio -------------------

@dispatch(pd.Series, str, str)
def replaceChar(col, oldVal, newVal):
    """
    Sustituye los carácteres de cada registro dentro de la serie pasada por parámetros.
    Parameters:
        - col: Serie de pandas que queremos cambiar
        - oldVal: String que queremos cambiar
        - newVal: String por el que queremos cambiar
    Return:
        - col: La columna transformada
    """

    return pd.Series(col).str.replace(str(oldVal), str(newVal), regex=True)


@dispatch(pd.Series, str, int)
def split(col, separador, parteRetorno):
    """
    Divide la columna por el carácter pasado por parámetros y devuelve la parte del split que queramos.
    Params:
        - col: Columna que queremos separar
        - separador: Carácter por el que se va a hacer el split
        - parteRetorno: Sección del split que se va a retornar
    Return:
        - pd.Series: Serie con la parte del split que nos interesa
    """
    return pd.Series(col).str.split(pat=separador, expand=True)[parteRetorno]


def changeDateFormat(col, oldFormat='%B %d, %Y', newFormat="%Y-%m-%d"):
    return pd.to_datetime(pd.Series(col), format=oldFormat).dt.strftime(newFormat)


# ------------------ Transformaciones Fin -------------------

# ------------------ Cambio de esquema Inicio -------------------

@dispatch(pd.DataFrame, list)
def updateSchema(df, lstTypes):
    """
    Esta función actualiza el esquema del dataframe pasado por parámetros
    Parameters:
        - df: El dataframe al que queremos cambiar el esquema
        - lstTypes: Lista que contiene los tipos de datos en orden.
    """

    # Comprobamos que el largo de la lista es igual al número de columnas del dataframe
    if len(lstTypes) != len(df.columns):
        raise Exception("Error al actualizar el esquema del dataframe. El largo de la lista de tipos no coincide"
                        "con el número de columnas del dataframe.")

    # Procedemos a cambiar los tipos de cada columna por los metidos en la lista
    for x in range(len(list(df.columns))):
        df[df.columns[x]] = df[df.columns[x]].astype(lstTypes[x])

    return df

# ------------------ Cambio de esquema Fin -------------------
