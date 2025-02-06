from enum import Enum


class Entidad(str, Enum):
    ventas = "ventas"
    productos = "productos"
    clientes = "clientes"
    productos_de_venta = "productos_de_venta"


class Agregador(str, Enum):
    suma = "suma"
    promedio = "promedio"


class TipoGrafico(str, Enum):
    barras = "barras"
    circular = "circular"  # torta / piechart / segmentos
