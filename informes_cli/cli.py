import json
import typer
from pathlib import Path

from informes_cli.comandos import cmd_examinar, cmd_examinar_agrupado, cmd_graficar
from informes_cli.datos import Datos, obtener_datos_importados
from informes_cli.modelo import Entidad, Agregador, TipoGrafico

APP_NAME = "informes_cli"

app = typer.Typer(no_args_is_help=True)


@app.command()
def importar_datos(carpeta: Path):
    cmd_importar_datos(carpeta)


@app.command()
def examinar(entidad: Entidad, id: int | None = None):
    datos = verificar_obtener_datos_importados()
    cmd_examinar(datos, entidad, id)


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


def cmd_importar_datos(carpeta: Path):
    if not carpeta.is_dir():
        typer.echo(f"No es una carpeta: {carpeta}")
        raise typer.Exit(1)

    archivos = ["ventas", "clientes", "productos", "productos_de_venta"]
    d = {x: (carpeta / f"{x}.csv").resolve() for x in archivos}
    d_str = {}

    for archivo, ubicacion in d.items():
        if not ubicacion.exists():
            typer.echo(f"Error: no existe el archivo: {ubicacion}")
            raise typer.Exit(1)

        if not ubicacion.is_file():
            typer.echo(f"Error: no es un archivo: {ubicacion}")
            raise typer.Exit(1)
        d_str[archivo] = str(ubicacion)

    datos_path = obtener_datos_path()
    datos_path.parent.mkdir(parents=True, exist_ok=True)
    with open(datos_path, "w") as datos_file:
        json.dump(d_str, datos_file)

    typer.echo("Datos importados!")
    for archivo, ubicacion in d.items():
        typer.echo(f"{archivo}: {ubicacion}")


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
