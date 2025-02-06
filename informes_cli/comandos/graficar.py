import typer
import pandas as pd
import numpy as np
from matplotlib import rcParams

from informes_cli.datos import Datos
from informes_cli.modelo import Entidad, TipoGrafico


def cmd_graficar(
    datos: Datos, tipo_grafico: TipoGrafico, entidad: Entidad, agrupar_por: Entidad
):
    rcParams.update({'figure.autolayout': True})

    df = datos[entidad.value]

    match (entidad, agrupar_por):
        case (Entidad.ventas, entidad.clientes):
            df_clientes = datos.clientes

            merged = pd.merge(df, df_clientes, how="outer", left_on="Cliente", right_index=True, suffixes=("_venta", "_cliente"))
            pivot = pd.pivot_table(merged, index="nombre", aggfunc="count")["ID_venta"]
            pivot = pivot.rename("Cantidad")
            f = None
            match tipo_grafico:
                case TipoGrafico.barras:
                    f = pivot.plot.bar
                case TipoGrafico.circular:
                    f = pivot.plot.pie
            fig = f().get_figure()
            fig.savefig("plot.png")
        case _:
            typer.echo(f"Error: no soportado actualmente: {entidad.value} agrupando por {agrupar_por.value}")
            raise typer.Exit(1)

