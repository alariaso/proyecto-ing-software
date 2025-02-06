- leer los cuatro archivos csv
- poner los datos en dataframes de pandas
- interfaz para los comandos


- comandos:
	- un comando para ver cada tabla, o una entrada especifica de una tabla
	- un comando para ver datos agregados (total, promedio, etc)
		- ventas (total del valor) agregado por cualquier columna
	- generar graficas
		- piechart de ventas agrupado por clientes
		- barras de ventas agrupado por productos


ARCHIVOS:
1. ventas
2. clientes
3. productos
4. productos de venta

VENTAS Columnas:
- ID de la venta
- Cliente
- fecha

PRODUCTOS DE VENTA Columnas:
- ID
- ID venta
- ID producto
- valor
- cantidad

Producto:
- ID
- nombre

Cliente:
- ID
- nombre

## Setup inicial

[Instalar uv](https://docs.astral.sh/uv/getting-started/installation/)

## Uso

```
uv run informes_cli
```
