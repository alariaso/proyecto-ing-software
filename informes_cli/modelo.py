from enum import Enum


class Entidad(str, Enum):
    ventas = "ventas"
    producto = "producto"
    cliente = "cliente"


class Agregador(str, Enum):
    suma = "suma"
    promedio = "promedio"


class TipoGrafico(str, Enum):
    barras = "barras"
    circular = "circular"  # torta / piechart / segmentos
