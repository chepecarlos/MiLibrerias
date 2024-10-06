"""Libreria de Funciones para Lectura y escritura de archivos."""

import json
import os
import shutil
import sys
from pathlib import Path, PosixPath

import yaml

from .FuncionesLogging import ConfigurarLogging

logger = ConfigurarLogging(__name__)

# TODO: https://www.youtube.com/watch?v=daefaLgNkw0
# TODO: usar get para obtener valor y recibir none si no esta
# TODO: update Actualizar la info
# TODO: Borrar con def data['valor']
# TODO: pop para carcar un dato


def ObtenerFolderConfig() -> Path:
    """Devuelve ruta donde esta el folder de configuración."""
    Programa = __name__.split(".")[0].lower()

    Folder = UnirPath(".config", Programa)
    Folder = UnirPath(Path.home(), Folder)

    Path(Folder).mkdir(parents=True, exist_ok=True)

    return Folder


def leerData(archivo, depruacion: bool = False):
    """Lee los archivos primero .md y después .json y lo devuelve"""
    tipoArchivos = [".md", ".json"]

    if ".md" in archivo or ".json" in archivo:
        return ObtenerArchivo(archivo)

    for tipo in tipoArchivos:
        dataTmp = ObtenerArchivo(f"{archivo}{tipo}")
        if dataTmp is not None:
            if depruacion:
                logger.info(f"Abriendo {archivo}{tipo}")
            return dataTmp
    return None


def BorrarFolderConfig() -> None:
    """¨Borra todas las configuraciones del paquete"""
    Configuraciones = ObtenerFolderConfig()
    try:
        shutil.rmtree(Configuraciones)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def ObtenerArchivo(Archivo: str | PosixPath, EnConfig: bool = True, depuracion: bool = False):
    """Leer y devuelta la información de un archivo dentro del folded de configuraciones."""
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
                elif Archivo.endswith(".txt"):
                    return f.read()
        except Exception as e:
            if depuracion:
                logger.warning(f"Archivo[Error] {Archivo} {e}")
    else:
        if depuracion:
            logger.warning(f"Archivo[Error] No existe {ArchivoActual}")

    return None


def ObtenerValor(Archivo: str | PosixPath, Atributo: list | str, depuracion: bool = False):
    """Obtiene un Atributo de un Archivo."""

    if Path(Archivo).suffix == "":
        Archivo = f"{Archivo}.md"

    data = ObtenerArchivo(Archivo, depuracion=depuracion)

    if data is None:
        return None

    Tipo = type(Atributo)
    if Tipo is list:
        # TODO modificar para cual dimension
        if len(Atributo) >= 2:
            if Atributo[0] in data:
                if Atributo[1] in data[Atributo[0]]:
                    return data[Atributo[0]][Atributo[1]]
    else:
        return data.get(Atributo)
    return None


def EscribirArchivo(Archivo: str, Data) -> None:
    """Escribe en un Archivo de Texto (md, txt, json)"""
    NombreArchivo = Path(Archivo).name
    RutaArchivo = Path(Archivo).parent
    SufijoArchivo = Path(Archivo).suffix
    RutaArchivo.mkdir(parents=True, exist_ok=True)

    if SufijoArchivo == "":
        SufijoArchivo = ".md"
        Archivo = f"{Archivo}.md"

    with open(Archivo, "w+") as f:
        if SufijoArchivo == ".json":
            json.dump(Data, f, indent=2)
        elif SufijoArchivo == ".txt":
            f.write(Data)
        elif SufijoArchivo == ".md":
            yaml.dump(Data, f, explicit_start=True, explicit_end=True, allow_unicode=True, sort_keys=False)
        else:
            print(f"Error: {Archivo} Atributo {SufijoArchivo}")


def SalvarArchivo(Archivo: str | PosixPath, Data) -> None:
    """Sobre escribe data en archivo."""
    if not Path(Archivo).is_absolute():
        ArchivoConfig = ObtenerFolderConfig()
        Archivo = UnirPath(ArchivoConfig, Archivo)
    EscribirArchivo(Archivo, Data)


def SalvarValor(Archivo: str | PosixPath, Atributo: str | list, Valor, local: bool = True, depuracion: bool = False) -> None:
    """Salvar un Valor en Archivo."""
    ArchivoConfig = ObtenerFolderConfig()
    if local:
        Archivo = UnirPath(ArchivoConfig, Archivo)

    if Path(Archivo).suffix == "":
        Archivo = f"{Archivo}.md"

    data = ObtenerArchivo(Archivo, local, depuracion=depuracion)
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


def UnirPath(Path1: str | PosixPath, Path2: str | PosixPath) -> str | PosixPath:
    """Une dos direcciones."""
    return os.path.join(Path1, Path2)


def RelativoAbsoluto(Path: str | PosixPath, FolderActual: str | PosixPath) -> str | PosixPath:
    """Convierte dirección relativas en absolutas."""
    if Path.startswith("./"):
        return UnirPath(FolderActual, QuitarPrefixInicio(Path, "./"))
    return Path


def QuitarPrefixInicio(text: str, prefix: str) -> str:
    """Quita un Prefijo o patron del inicio de una cadena."""
    return text[text.startswith(prefix) and len(prefix):]


def ObtenerListaFolder(Directorio: str) -> list:
    """Devuelve una lista de los folder dentro de Directorio."""
    ArchivoConfig = ObtenerFolderConfig()
    FolderActual = os.path.join(ArchivoConfig, Directorio)
    ListaFolder = list()
    if os.path.exists(FolderActual):
        for folder in os.listdir(FolderActual):
            if os.path.isdir(os.path.join(FolderActual, folder)):
                # ListaFolder.append({"folder": folder})
                ListaFolder.append(folder)
        return ListaFolder
    return None


def ObtenerListaArhivos(Directorio: str | PosixPath) -> list:
    """Obtiene una lista de Archivo en un directorio
    
    Args:
        Directorio (str | PosixPath): folder a buscar Archivos


    Returns:
        list: lista de folder encontrados
    """
    
    ArchivoConfig = ObtenerFolderConfig()
    FolderActual = os.path.join(ArchivoConfig, Directorio)
    ListaArchivos = list()
    if os.path.exists(FolderActual):
        for archivo in os.listdir(FolderActual):
            if os.path.isfile(os.path.join(FolderActual, archivo)):
                ListaArchivos.append(archivo)
        return ListaArchivos
    return None

def obtenerArchivoPaquete(paquete: str, ruta: str):
    """devuelve archivos interno del paquete

    Args:
        paquete (str): Nombre del programa
        ruta (str): Donde esta la direccion a habir

    Returns:
        _type_: Información del Archivo
    """
    # http://peak.telecommunity.com/DevCenter/setuptools#non-package-data-files
    from pkg_resources import Requirement, resource_filename
    archivoPaquete = resource_filename(Requirement.parse(paquete),ruta)
    return ObtenerArchivo(archivoPaquete)

def rutaAbsoluta(ruta: str):
    """Obtiene ruta absoluta si es relataba
    """    

    return os.path.abspath(ruta)