import typer
import pandas as pd
from informes_cli.datos import Datos
from informes_cli.modelo import Entidad

def cmd_examinar(datos: Datos, entidad: Entidad, id: int | None):
    df = datos[entidad.value]

    if id is None:
        typer.echo(df)
    else:
        id_col = "ID"

        if id_col in df.columns:
            resultado = df[df[id_col] == id]
            if resultado.empty:
                typer.echo(f"No se encontró {entidad.value} con ID {id}.")
            else:
                typer.echo(resultado)
        else:
            typer.echo(f"La entidad {entidad.value} no tiene una columna ID reconocida.")
