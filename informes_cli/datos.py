from pathlib import Path
from dataclasses import dataclass
import pandas as pd


@dataclass
class Datos:
    ventas: pd.DataFrame
    clientes: pd.DataFrame
    productos: pd.DataFrame
    productos_de_venta: pd.DataFrame

    def __getitem__(self, item):
        return getattr(self, item)


def leer_archivo(archivo: Path) -> pd.DataFrame:
    return pd.read_csv(archivo)


def obtener_datos_importados(datos_paths) -> Datos | None:
    ventas = leer_archivo(datos_paths["ventas"])
    clientes = leer_archivo(datos_paths["clientes"])
    productos = leer_archivo(datos_paths["productos"])
    productos_de_venta = leer_archivo(datos_paths["productos_de_venta"])
    return Datos(ventas, clientes, productos, productos_de_venta)
