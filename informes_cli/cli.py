import json
import typer
from pathlib import Path

from informes_cli.comandos import cmd_examinar, cmd_examinar_agrupado, cmd_graficar
from informes_cli.datos import Datos, obtener_datos_importados
from informes_cli.modelo import Entidad, Agregador, TipoGrafico

APP_NAME = "informes_cli"

app = typer.Typer(no_args_is_help=True)


@app.command()
def importar_datos(
    ventas: Path, clientes: Path, productos: Path, productos_de_venta: Path
):
    cmd_importar_datos(ventas, clientes, productos, productos_de_venta)


@app.command()
def examinar(entidad: Entidad):
    datos = verificar_obtener_datos_importados()
    cmd_examinar(datos, entidad)


@app.command()
def examinar_agrupado(
    entidad: Entidad, agrupar_por: Entidad, agregar_que: str, agregar_como: Agregador
):
    datos = verificar_obtener_datos_importados()
    cmd_examinar_agrupado(datos, entidad, agrupar_por, agregar_que, agregar_como)


@app.command()
def graficar(tipo_grafico: TipoGrafico, entidad: Entidad, agrupar_por: Entidad):
    datos = verificar_obtener_datos_importados()
    cmd_graficar(datos, tipo_grafico, entidad, agrupar_por)


def cmd_importar_datos(
    ventas: Path, clientes: Path, productos: Path, productos_de_venta: Path
):
    def verificar_existe(archivo: Path):
        if not archivo.exists():
            typer.echo(f"Error: no existe el archivo: {archivo}")
            raise typer.Exit(1)
    
    for archivo in [ventas, clientes, productos, productos_de_venta]:
        verificar_existe(archivo)

    datos_path = obtener_datos_path()
    d = {
        "ventas": str(ventas.resolve()),
        "clientes": str(clientes.resolve()),
        "productos": str(productos.resolve()),
        "productos_de_venta": str(productos_de_venta.resolve()),
    }
    datos_path.parent.mkdir(parents=True, exist_ok=True)
    with open(datos_path, "w") as datos_file:
        json.dump(d, datos_file)
    print("Datos importados!")


def verificar_obtener_datos_importados() -> Datos:
    datos_path = obtener_datos_path()

    if not datos_path.exists():
        typer.echo("Error: debe importar los datos primero (comando importar-datos)")
        raise typer.Exit(1)

    with open(datos_path) as datos_file:
        datos_paths = json.load(datos_file)
    datos = obtener_datos_importados(datos_paths)

    if datos is None:
        typer.echo("Error: debe importar los datos primero (comando importar-datos)")
        raise typer.Exit(1)

    return datos


def obtener_datos_path() -> Path:
    app_dir = typer.get_app_dir(APP_NAME)
    datos_path: Path = Path(app_dir) / "datos.json"
    return datos_path
