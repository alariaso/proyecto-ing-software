import typer

from informes_cli.datos import Datos
from informes_cli.modelo import Entidad


def cmd_examinar(datos: Datos, entidad: Entidad, id: int | None):
    typer.echo(datos[entidad.value])
