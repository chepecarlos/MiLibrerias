"""Libreria de Funciones para Lectura y escritura de archivos."""

import json
import os
import yaml
import sys
import shutil

from pathlib import Path, PosixPath

from .FuncionesLogging import ConfigurarLogging

logger = ConfigurarLogging(__name__)

# TODO: https://www.youtube.com/watch?v=daefaLgNkw0
# TODO: usar get para obtener valor y recivir none si no esta
# TODO: update Actaulizar la info
# TODO: Borrar con def data['valor']
# TODO: pop para carcar un dato


def ObtenerFolderConfig():
    """Devuelte ruta donde esta el folder de configuracion."""
    Programa = os.path.basename(sys.argv[0]).lower()
    Programa = os.path.splitext(Programa)[0]

    Folder = UnirPath('.config', Programa)
    Folder = UnirPath(Path.home(), Folder)

    Path(Folder).mkdir(parents=True, exist_ok=True)

    return Folder


def BorrarFolderConfig():
    Contiguraciones = ObtenerFolderConfig()
    try:
        shutil.rmtree(Contiguraciones)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def ObtenerArchivo(Archivo, EnConfig=True):
    """Leer y devuelte la informacion de un archivo dentro del folde de configuraciones."""
    if type(Archivo) not in [str, PosixPath]:
        raise TypeError("El Archivo tiene que ser str o PosixPath")

    if EnConfig:
        ArchivoConfig = ObtenerFolderConfig()
        ArchivoActual = UnirPath(ArchivoConfig, Archivo)
    else: 
        ArchivoActual = Archivo
    if os.path.exists(ArchivoActual):
        try:
            with open(ArchivoActual) as f:
                if Archivo.endswith(".json"):
                    return json.load(f)
                elif Archivo.endswith(".md"):
                    return list(yaml.load_all(f, Loader=yaml.SafeLoader))[0]
        except Exception as e:
            logger.warning(f"Archivo[Error] {Archivo} {e}")
    return None


def ObtenerValor(Archivo, Atributo, Depurar=True):
    """Obtiene un Atributo de un Archivo."""
    if type(Archivo) not in [str, PosixPath]:
        raise TypeError("El Archivo tiene que ser str o PosixPath")

    data = ObtenerArchivo(Archivo)

    if data is None:
        return None

    Tipo = type(Atributo)
    if Tipo is list:
        if len(Atributo) >= 2:
            if Atributo[0] in data:
                if Atributo[1] in data[Atributo[0]]:
                    return data[Atributo[0]][Atributo[1]]
    else:
        if Atributo in data:
            return data[Atributo]

    return None


def EscribirArchivo(Archivo, Data):
    NombreArchivo = Path(Archivo).name
    RutaArchivo = Path(Archivo).parent
    SufijoArchivo = Path(Archivo).suffix
    RutaArchivo.mkdir(parents=True, exist_ok=True)
    with open(Archivo, 'w+') as f:
        if SufijoArchivo == ".json":
            json.dump(Data, f, indent=2)
        elif SufijoArchivo == ".txt":
            f.write(Data)
        elif SufijoArchivo == ".md":
            yaml.dump(Data, f, explicit_start=True, explicit_end=True)


def SalvarArchivo(Archivo, Data):
    """Sobre escribe data en archivo."""
    if type(Archivo) not in [str, PosixPath]:
        raise TypeError("Los Path tiene que ser str o PosixPath")

    ArchivoConfig = ObtenerFolderConfig()
    Archivo = UnirPath(ArchivoConfig, Archivo)
    EscribirArchivo(Archivo, Data)


def SalvarValor(Archivo, Atributo, Valor, local=True):
    """Salvar un Valor en Archivo."""
    if type(Archivo) not in [str, PosixPath]:
        raise TypeError("Los Path tiene que ser str o PosixPath")

    ArchivoConfig = ObtenerFolderConfig()
    if local:
        Archivo = UnirPath(ArchivoConfig, Archivo)

    data = ObtenerArchivo(Archivo)
    if data is None:
        data = dict()

    Tipo = type(Atributo)
    if Tipo is list:
        InData = data
        for AtributoActual in Atributo[:-1]:
            if not AtributoActual in InData:
                InData[AtributoActual] = dict()
            InData = InData[AtributoActual]
        InData[Atributo[-1]] = Valor
    else:
        data[Atributo] = Valor

    EscribirArchivo(Archivo, data)


def UnirPath(Path1, Path2):
    """Une dos direciones."""
    if type(Path1) not in [str, PosixPath] or type(Path2) not in [str, PosixPath]:
        raise TypeError("Los Path tiene que ser str o PosixPath")

    return os.path.join(Path1, Path2)


def RelativoAbsoluto(Path, FolderActual):
    """Convierte Direcion relativas en absolutas."""
    if type(Path) not in [str, PosixPath] or type(FolderActual) not in [str, PosixPath]:
        raise TypeError("Los Path tiene que ser str o PosixPath")

    if Path.startswith("./"):
        return UnirPath(FolderActual, QuitarPrefixInicio(Path, "./"))
    return Path


def QuitarPrefixInicio(text, prefix):
    """Quita un Prefijo o patron del inicio de una cadena."""
    return text[text.startswith(prefix) and len(prefix):]


def ObtenerListaFolder(Directorio):
    """Devuelve una lista de los folder dentro de Directorio."""
    ArchivoConfig = ObtenerFolderConfig()
    FolderActual = os.path.join(ArchivoConfig, Directorio)
    ListaFolder = []
    if os.path.exists(FolderActual):
        for folder in os.listdir(FolderActual):
            if os.path.isdir(os.path.join(FolderActual, folder)):
                # ListaFolder.append({"folder": folder})
                ListaFolder.append(folder)
        return ListaFolder
    return None


def ObtenerListaArhivos(Directorio):
    """Obtiene una lista de Archivo en un directorio."""
    if type(Directorio) not in [str, PosixPath]:
        raise TypeError("Los Path tiene que ser str o PosixPath")

    ArchivoConfig = ObtenerFolderConfig()
    FolderActual = os.path.join(ArchivoConfig, Directorio)
    ListaArchivos = []
    if os.path.exists(FolderActual):
        for archivo in os.listdir(FolderActual):
            if os.path.isfile(os.path.join(FolderActual, archivo)):
                ListaArchivos.append(archivo)
        return ListaArchivos
    return None
