# Aplicacion Dash: Reporte de Ventas

# recordar para visualizar la pagina es necesario instalar las librerias
# pip install (nombre de la libreria faltante)
# recordar que los archivos .csv deben encontrase en la misma carpeta que el programa para ser leidos sin problemas
# al ejecutar el codigo debe de salir algo como "Dash is running on "http://127.0.0.1:8050/"
# simple mente copien y peguen en el navegador la parte de "http://127.0.0.1:8050/" y debera mostrarse toda la pagina de forma correcta

# ===========================
# 0. IMPORTACION DE LIBRERIAS
# ===========================

import pandas as pd
import plotly.express as px
from dash import (
    Dash,
    html,
    dcc,
    Input,
    Output,
    State,
    no_update,
    dash_table,
    clientside_callback,
)
import base64
import io
import dash_bootstrap_components as dbc


# =================================
# 1. CARGA Y PROCESAMIENTO DE DATOS
# =================================

# Se leen los 3 archivos csv proporcionados


# =============================================================
# 2. CONFIGURACION DE LA APLICACION DASH Y ESTILOS DE LA PAGINA
# =============================================================

# === CREA LA APP ===
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Reportes"  # Cambiar el titulo de la pagina

# === COLORES DE LA PAGINA ===

COLOR_FONDO = "#222222"  # Fondo oscuro
COLOR_TEXTO = "#FFFFFF"  # Texto blanco


# lit toda la pagina ._. aqui se definen los colores de la pagina, además la distrubicion de los graficos e informacion extra de los graficos (Frontend)
app.layout = html.Div(
    style={
        "backgroundColor": COLOR_FONDO,
        "color": COLOR_TEXTO,
        "minHeight": "100vh",
        "padding": "20px",
        "fontFamily": "Arial, sans-serif",
    },
    children=[
        # Titulos principales
        html.H2(
            "Compañía induboton SAS",
            style={"textAlign": "center", "marginBottom": "5px"},
        ),
        html.H1(
            "REPORTE DE VENTAS",
            style={"textAlign": "center", "marginTop": "0px", "marginBottom": "30px"},
        ),
        # Ãlmacena datos procesados queluego se usaran en graficos
        dcc.Store(id="stored-data-ventas-producto", data={}),
        dcc.Store(id="stored-data-original"),
        dcc.Store(id="stored-for-excel-export-ventas", data={}),
        dcc.Store(id="stored-for-excel-export-productos_mas_vendidos", data={}),
        dcc.Store(id="stored-for-excel-export-productos_menos_vendidos", data={}),
        dcc.Store(id="stored-for-excel-export-ventas_por_cliente", data={}),
        dcc.Store(id="stored-for-excel-export-clientes_por_productos", data={}),
        dcc.Store(id="stored-for-excel-export-estadisticas_ventas_productos", data={}),
        dcc.Store(id="stored-for-excel-export-estadisticas_ventas_ingreso", data={}),
        dcc.Store(id="stored-for-excel-export-estadisticas_clientes_ingreso", data={}),
        dcc.Store(
            id="stored-for-excel-export-estadisticas_clientes_productos", data={}
        ),
        dcc.Download(id="download-excel"),
        # SUbir datos
        dcc.Upload(
            id="upload-data",
            children=dbc.Button("Subir Archivo CSV"),
            style={"textAlign": "center", "marginBottom": "20px"},
            multiple=True,
        ),
        html.Div(  # Pestaña para  visualizar los .csv importados
            [
                html.Div(
                    [
                        dbc.Button(
                            "Ver Archivos Importados",
                            id="open-modal-button",
                            color="secondary",
                            style={
                                "position": "absolute",
                                "top": "20px",
                                "left": "20px",
                            },
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Datos Importados")),
                                dbc.ModalBody(
                                    dbc.Tabs(
                                        id="csv-tabs", active_tab="tab-0"
                                    ),  # Pestañas dinamicas
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Cerrar",
                                        id="close-modal-button",
                                        color="secondary",
                                    )
                                ),
                            ],
                            id="csv-modal",
                            size="xl",
                            is_open=False,
                        ),
                    ]
                ),
                html.Div(
                    [
                        dbc.Button(
                            "Guardar pdf",
                            id="savePDF-button",
                            color="secondary",
                            class_name="m-2",
                        ),
                        # style={
                        #     "marginBottom": "20px",
                        # },
                        dbc.Button(
                            "Exportar a excel",
                            id="exportar-excel-button",
                            color="secondary",
                            class_name="m-2",
                        ),
                    ],
                    style={
                        "maxWidth": "fit-content",
                        "marginLeft": "auto",
                        "marginRight": "auto",
                        "marginBottom": "20px",
                    },
                ),
                # Dropdown para seleccionar el año
                html.Div(
                    dcc.Dropdown(
                        id="year-selector",
                        options=[],  # lista vacia y false que se definen luego de subir los archivos
                        value=False,
                        clearable=False,
                        style={"width": "50%", "margin": "0 auto", "color": "#000000"},
                    ),
                    style={"textAlign": "center", "marginBottom": "30px"},
                ),
                # Subtitulos generales que muestran ventas totales y cantidad de ventas en el año seleccionado
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "center",
                        "marginBottom": "30px",
                        "gap": "40px",
                    },
                    children=[
                        # ventas totales
                        html.Div(
                            [
                                html.H3(
                                    "Ventas Totales:", style={"marginBottom": "10px"}
                                ),
                                html.Div(id="total-sales", style={"fontSize": "24px"}),
                            ],
                            style={
                                "border": "1px solid #444",
                                "padding": "20px",
                                "borderRadius": "8px",
                            },
                        ),
                        # cantidad de ventas
                        html.Div(
                            [
                                html.H3(
                                    "Cantidad de ventas:",
                                    style={"marginBottom": "10px"},
                                ),
                                html.Div(id="num-sales", style={"fontSize": "24px"}),
                            ],
                            style={
                                "border": "1px solid #444",
                                "padding": "20px",
                                "borderRadius": "8px",
                            },
                        ),
                    ],
                ),
                # Linea separadora horizontal
                html.Hr(
                    style={
                        "border": "1px solid #444",
                        "marginBottom": "30px",
                        "breakAfter": "page",
                    }
                ),
                # Contenedor de graficos y sus respectivas secciones informativas
                dbc.Row(
                    [
                        # Caja para el grafico de barras con información adicional sobre los productos
                        dbc.Col(
                            [
                                # Informacion del producto más vendido y menos vendido del grafico de barras
                                html.Div(
                                    id="bar-info",
                                    style={"marginBottom": "20px", "fontSize": "18px"},
                                ),
                                dcc.Graph(id="bar-chart", style={"height": "600px"}),
                            ],
                            style={
                                "border": "1px solid #444",
                                "borderRadius": "8px",
                                "padding": "10px",
                                "breakAfter": "page",
                                "margin": "15px",
                            },
                        ),
                        # Caja para el grafico de pastel con informacion adicional sobre los productos
                        dbc.Col(
                            [
                                # Informacion del producto mas vendido y menos vendido del grafico de pastel
                                html.Div(
                                    id="pie-info",
                                    style={"marginBottom": "20px", "fontSize": "18px"},
                                ),
                                dcc.Graph(id="pie-chart", style={"height": "600px"}),
                            ],
                            style={
                                "border": "1px solid #444",
                                "borderRadius": "8px",
                                "padding": "10px",
                                "margin": "15px",
                            },
                        ),
                    ],
                    style={
                        "marginBottom": "30px",
                    },
                ),
                # Linea final para separar secciones
                html.Hr(
                    style={
                        "border": "1px solid #444",
                        "marginTop": "30px",
                        "breakAfter": "page",
                    }
                ),
                html.Div(
                    [
                        html.H3(
                            "Los",
                            style={"display": "inline-block", "marginRight": "5px"},
                        ),
                        dcc.Dropdown(
                            [5, 10, 15],
                            value=5,
                            id="tabla-productos-mas-vendidos-cantidad",
                            style={"display": "inline-block", "color": "#000000"},
                        ),
                        html.H3(
                            "productos más vendidos",
                            style={"display": "inline-block", "marginLeft": "5px"},
                        ),
                        dash_table.DataTable(
                            id="tabla-productos-mas-vendidos",
                            style_cell={
                                "color": COLOR_TEXTO,
                                "background-color": COLOR_FONDO,
                            },
                            style_header={"font-weight": "bold"},
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.H3(
                            "Los",
                            style={"display": "inline-block", "marginRight": "5px"},
                        ),
                        dcc.Dropdown(
                            [5, 10, 15],
                            value=5,
                            id="tabla-productos-menos-vendidos-cantidad",
                            style={"display": "inline-block", "color": "#000000"},
                        ),
                        html.H3(
                            "productos menos vendidos",
                            style={"display": "inline-block", "marginLeft": "5px"},
                        ),
                        dash_table.DataTable(
                            id="tabla-productos-menos-vendidos",
                            style_cell={
                                "color": COLOR_TEXTO,
                                "background-color": COLOR_FONDO,
                            },
                            style_header={"font-weight": "bold"},
                        ),
                    ]
                ),
                html.Hr(
                    style={
                        "border": "1px solid #444",
                        "marginTop": "30px",
                        "breakAfter": "page",
                    }
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H3("Cantidad de ventas por cliente"),
                                    dcc.Graph(
                                        id="cantidad-ventas-por-cliente", figure={}
                                    ),
                                ],
                                body=True,
                            ),
                            style={"breakAfter": "page"},
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H3("Clientes por producto"),
                                    dcc.Graph(id="clientes-por-productos", figure={}),
                                ],
                                body=True,
                            )
                        ),
                    ]
                ),
                html.Hr(
                    style={
                        "border": "1px solid #444",
                        "marginTop": "30px",
                        "breakAfter": "page",
                    }
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H3("Estadísticas de ventas"),
                                    html.H4("Productos por venta"),
                                    html.H5(
                                        "Promedio:",
                                        style={
                                            "display": "inline-block",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    html.Span(
                                        id="estadisticas-ventas-promedio-productos-por-venta"
                                    ),
                                    html.Br(),
                                    html.H5(
                                        "Desviación estándar:",
                                        style={
                                            "display": "inline-block",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    html.Span(
                                        id="estadisticas-ventas-desviacion-productos-por-venta"
                                    ),
                                    html.Br(),
                                    html.H4("Ingresos por venta"),
                                    html.H5(
                                        "Promedio:",
                                        style={
                                            "display": "inline-block",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    html.Span(
                                        id="estadisticas-ventas-promedio-ingreso-por-venta"
                                    ),
                                    html.Br(),
                                    html.H5(
                                        "Desviación estándar:",
                                        style={
                                            "display": "inline-block",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    html.Span(
                                        id="estadisticas-ventas-desviacion-ingreso-por-venta"
                                    ),
                                    html.Br(),
                                ],
                                body=True,
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H3("Estadísticas de clientes"),
                                    html.H4("Ingresos por cliente"),
                                    html.H5(
                                        "Promedio:",
                                        style={
                                            "display": "inline-block",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    html.Span(
                                        id="estadisticas-clientes-promedio-ingresos-por-cliente"
                                    ),
                                    html.Br(),
                                    html.H5(
                                        "Desviación estándar:",
                                        style={
                                            "display": "inline-block",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    html.Span(
                                        id="estadisticas-clientes-desviacion-ingresos-por-cliente"
                                    ),
                                    html.Br(),
                                    html.H4(
                                        "Cantidad de productos diferentes que compra cada cliente"
                                    ),
                                    html.H5(
                                        "Promedio:",
                                        style={
                                            "display": "inline-block",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    html.Span(
                                        id="estadisticas-clientes-promedio-cantidad-productos"
                                    ),
                                    html.Br(),
                                    html.H5(
                                        "Desviación estándar:",
                                        style={
                                            "display": "inline-block",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    html.Span(
                                        id="estadisticas-clientes-desviacion-cantidad-productos"
                                    ),
                                    html.Br(),
                                ],
                                body=True,
                            )
                        ),
                    ]
                ),
            ],
            id="app-container",
            style={"display": "none"},
        ),
    ],
)

# ==================================================
# 4. CALLBACK PARA ACTUALIZAR GRAFICOS E INFORMACION
# ==================================================


# Esto es lo q se encarga de relacionar el Front con el Back
# Función callback que actualiza los gráficos de barras y pastel e información adicional
# cuando se selecciona un año
@app.callback(
    Output("stored-data-ventas-producto", "data"),  # Guarda df_final en dcc.Store
    Output("year-selector", "options"),
    Output("year-selector", "value"),
    Output("stored-data-original", "data"),
    Output("app-container", "style"),
    Input("upload-data", "contents"),
    Input("upload-data", "filename"),
    prevent_initial_call=True,
)
def update_data(
    contents_list, filenames_list
):  # Si no se incluyen datos no hace  nada y no cambia la pagina
    if contents_list is None or filenames_list is None:
        return no_update

    # Verificar que contents_list y filenames_list sean listas
    if not isinstance(contents_list, list):
        contents_list = [contents_list]
    if not isinstance(filenames_list, list):
        filenames_list = [filenames_list]

    # Diccionario para guardar los DataFrames por nombre
    dfs = {}

    # Se procesan los archivos
    for contents, filename in zip(contents_list, filenames_list):
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

        # Guardar el DataFrame con su nombre de archivo
        dfs[filename] = df

    # Verificar que tengamos los 3 archivos
    if not all(
        name in dfs
        for name in [
            "productos_de_venta.csv",
            "ventas.csv",
            "productos.csv",
            "clientes.csv",
        ]
    ):
        return no_update  # No actualizar si falta alguno

    # Extraer los DataFrames correctamente
    df_pventa = dfs["productos_de_venta.csv"]
    df_ventas = dfs["ventas.csv"]
    df_productos = dfs["productos.csv"]
    # df_clientes = dfs["clientes.csv"]

    # Unir los datos
    df_pventa["ventas_totales"] = df_pventa["valor"] * df_pventa["cantidad"]
    df_merged = pd.merge(
        df_pventa, df_ventas, left_on="ID venta", right_on="ID", how="left"
    )
    df_merged["fecha"] = pd.to_datetime(df_merged["fecha"])
    df_merged["year"] = df_merged["fecha"].dt.year
    df_final = pd.merge(
        df_merged, df_productos, left_on="ID producto", right_on="ID", how="left"
    )

    # Obtener los años disponibles
    new_years = sorted(df_final["year"].unique())
    new_year_options = [{"label": str(year), "value": str(year)} for year in new_years]

    # Convertir df_final a formato json para almacenarlo en dcc.Store
    df_final_json = df_final.to_json(date_format="iso", orient="split")

    dfs["ventas.csv"]["fecha"] = pd.to_datetime(dfs["ventas.csv"]["fecha"])
    dfs["ventas.csv"]["year"] = dfs["ventas.csv"]["fecha"].dt.year
    dfs_original = dict(
        map(lambda item: (item[0], item[1].to_dict("records")), dfs.items())
    )

    return (
        df_final_json,
        new_year_options,
        str(new_years[0]),
        dfs_original,
        {"display": "block"},
    )


@app.callback(
    Output("bar-chart", "figure"),
    Output("pie-chart", "figure"),
    Output("total-sales", "children"),
    Output("num-sales", "children"),
    Output("bar-info", "children"),
    Output("pie-info", "children"),
    Output("stored-for-excel-export-ventas", "data"),
    Input("stored-data-ventas-producto", "data"),  # Obtiene los datos procesados
    Input("year-selector", "value"),
    prevent_initial_call=True,
)
def update_charts(stored_data, selected_year):
    if not stored_data:
        return no_update  # Si no hay datos, no hacer nada

    # Filtra los datos para el año seleccionado
    df_final = pd.read_json(stored_data, orient="split")

    dff = df_final[df_final["year"] == int(selected_year)]

    # Agrupa por el nombre del producto y suma las ventas totales
    df_grouped = dff.groupby("nombre", as_index=False)["ventas_totales"].sum()

    # Calcula el total monetario y la cantidad total de productos vendidos en el año seleccionado
    total_monetario = dff["ventas_totales"].sum()
    total_unidades = dff["cantidad"].sum()
    total_sales_text = f"Ventas totales: ${total_monetario:,.2f}"
    num_sales_text = f"Cantidad de ventas: {total_unidades}"

    # Informacion adicional de los graficos:

    # Para el grafico de barras: ventas totales en $
    # Se saca el producto con mayor ventas y menor ventas (según ventas_totales)
    if not df_grouped.empty:
        max_row = df_grouped.loc[df_grouped["ventas_totales"].idxmax()]
        min_row = df_grouped.loc[df_grouped["ventas_totales"].idxmin()]
    else:
        max_row = {"nombre": "N/A", "ventas_totales": 0}
        min_row = {"nombre": "N/A", "ventas_totales": 0}

    # Se muestra el producto mas vendido y menos vendido
    bar_info = html.Div(
        [
            html.Div(
                [
                    html.Strong("Producto más vendido: "),
                    f"{max_row['nombre']} - US $ {max_row['ventas_totales']:,.2f}",
                ],
                style={"marginBottom": "10px"},
            ),
            html.Div(
                [
                    html.Strong("Producto menos vendido: "),
                    f"{min_row['nombre']} - US $ {min_row['ventas_totales']:,.2f}",
                ]
            ),
        ]
    )

    # Para el grafico de pastel: ventas totales en %
    # se calcula el porcentaje de cada producto sobre el total de ventas agrupadas
    total_grouped = df_grouped["ventas_totales"].sum()
    if total_grouped > 0:
        max_pct = (max_row["ventas_totales"] / total_grouped) * 100
        min_pct = (min_row["ventas_totales"] / total_grouped) * 100
    else:
        max_pct = min_pct = 0

    # Se muestran el producto mas y menos vendido junto con el porcentaje correspondiente
    pie_info = html.Div(
        [
            html.Div(
                [
                    html.Strong("Producto más vendido: "),
                    f"{max_row['nombre']} - {max_pct:.1f}%",
                ],
                style={"marginBottom": "10px"},
            ),
            html.Div(
                [
                    html.Strong("Producto menos vendido: "),
                    f"{min_row['nombre']} - {min_pct:.1f}%",
                ]
            ),
        ]
    )

    # === Grafico de Barras con Plotly Express ===
    bar_fig = px.bar(
        df_grouped,
        x="nombre",
        y="ventas_totales",
        title=f"Ventas Totales por Producto en {selected_year} (Barras)",
        labels={"ventas_totales": "Ventas Totales", "nombre": "Producto"},
        height=600,
    )
    # Se usa el estilo oscuro en la grafica
    bar_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLOR_FONDO,
        plot_bgcolor="#333333",
        font_color=COLOR_TEXTO,
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
    )

    # === Grafico de Pastel con Plotly Express ===
    pie_fig = px.pie(
        df_grouped,
        names="nombre",
        values="ventas_totales",
        title=f"Distribución de Ventas por Producto en {selected_year} (Pastel)",
        height=600,
    )
    # Se usa el estilo oscuro en la grafica
    pie_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLOR_FONDO,
        plot_bgcolor="#333333",
        font_color=COLOR_TEXTO,
        title_font_size=20,
    )

    return (
        bar_fig,
        pie_fig,
        total_sales_text,
        num_sales_text,
        bar_info,
        pie_info,
        df_grouped.to_dict(),
    )


@app.callback(
    Output("tabla-productos-mas-vendidos", "data"),
    Output("stored-for-excel-export-productos_mas_vendidos", "data"),
    Input("stored-data-original", "data"),
    Input("year-selector", "value"),
    Input("tabla-productos-mas-vendidos-cantidad", "value"),
    prevent_initial_call=True,
)
def update_most_sold_products_table(dfs_originales, selected_year, size):
    if not dfs_originales:
        return no_update

    d = gen_tabla_productos_vendidos(dfs_originales, selected_year, size, mas=True)
    return d, d


@app.callback(
    Output("tabla-productos-menos-vendidos", "data"),
    Output("stored-for-excel-export-productos_menos_vendidos", "data"),
    Input("stored-data-original", "data"),
    Input("year-selector", "value"),
    Input("tabla-productos-menos-vendidos-cantidad", "value"),
    prevent_initial_call=True,
)
def update_least_sold_products_table(dfs_originales, selected_year, size):
    if not dfs_originales:
        return no_update

    d = gen_tabla_productos_vendidos(dfs_originales, selected_year, size, mas=False)
    return d, d


@app.callback(
    Output("cantidad-ventas-por-cliente", "figure"),
    Output("stored-for-excel-export-ventas_por_cliente", "data"),
    Input("stored-data-original", "data"),
    Input("year-selector", "value"),
    prevent_initial_call=True,
)
def update_qty_by_client_chart(dfs_originales, selected_year):
    if not dfs_originales:
        return no_update

    df_clientes = pd.DataFrame(dfs_originales["clientes.csv"])
    df_ventas = pd.DataFrame(dfs_originales["ventas.csv"])
    df_ventas = df_ventas[df_ventas["year"] == int(selected_year)]
    df_ventas_con_clientes = df_ventas.merge(
        df_clientes,
        how="right",
        left_on="Cliente",
        right_on="ID",
        suffixes=("_ventas", "_clientes"),
    )[["nombre", "ID_ventas"]].rename(columns={"nombre": "Cliente"})

    fig = px.histogram(df_ventas_con_clientes, x="Cliente")
    fig.update_layout(
        yaxis_title_text="Cantidad de ventas",
        template="plotly_dark",
        paper_bgcolor=COLOR_FONDO,
        plot_bgcolor="#333333",
        font_color=COLOR_TEXTO,
        title_font_size=20,
    )

    return fig, df_ventas_con_clientes.to_dict()


@app.callback(
    Output("clientes-por-productos", "figure"),
    Output("stored-for-excel-export-clientes_por_productos", "data"),
    Input("stored-data-original", "data"),
    Input("year-selector", "value"),
    prevent_initial_call=True,
)
def update_client_by_product_chart(dfs_originales, selected_year):
    if not dfs_originales:
        return no_update

    df_clientes = pd.DataFrame(dfs_originales["clientes.csv"])
    df_ventas = pd.DataFrame(dfs_originales["ventas.csv"])
    df_ventas = df_ventas[df_ventas["year"] == int(selected_year)]
    df_productos = pd.DataFrame(dfs_originales["productos.csv"])
    df_productos_de_venta = pd.DataFrame(dfs_originales["productos_de_venta.csv"])

    df_ventas_con_clientes = df_ventas.merge(
        df_clientes,
        how="right",
        left_on="Cliente",
        right_on="ID",
        suffixes=("_venta", "_cliente"),
    )[["ID_venta", "ID_cliente", "nombre"]].rename(columns={"nombre": "NOMBRE_cliente"})

    df_ventas_clientes_productos_de_venta = df_ventas_con_clientes.merge(
        df_productos_de_venta, how="left", left_on="ID_venta", right_on="ID venta"
    )[
        ["ID_venta", "ID_cliente", "NOMBRE_cliente", "ID", "ID producto", "cantidad"]
    ].rename(
        columns={
            "ID": "ID_producto_de_venta",
            "cantidad": "CANTIDAD_productos_de_venta",
        }
    )

    df_ventas_clientes_productos = df_ventas_clientes_productos_de_venta.merge(
        df_productos, how="left", left_on="ID producto", right_on="ID"
    )[["ID_venta", "NOMBRE_cliente", "nombre", "CANTIDAD_productos_de_venta"]].rename(
        columns={"nombre": "NOMBRE_producto"}
    )

    df = (
        df_ventas_clientes_productos.groupby(by=["NOMBRE_producto", "NOMBRE_cliente"])
        .sum()["CANTIDAD_productos_de_venta"]
        .reset_index()
        .rename(columns={"NOMBRE_cliente": "Cliente"})
    )

    fig = px.bar(
        df, x="NOMBRE_producto", color="Cliente", y="CANTIDAD_productos_de_venta"
    )
    fig.update_layout(
        yaxis_title_text="Cantidad de productos por cliente",
        xaxis_title_text="Producto",
        template="plotly_dark",
        paper_bgcolor=COLOR_FONDO,
        plot_bgcolor="#333333",
        font_color=COLOR_TEXTO,
        title_font_size=20,
    )

    return fig, df.to_dict()


@app.callback(
    Output("estadisticas-ventas-promedio-productos-por-venta", "children"),
    Output("estadisticas-ventas-desviacion-productos-por-venta", "children"),
    Output("stored-for-excel-export-estadisticas_ventas_productos", "data"),
    Input("stored-data-original", "data"),
    Input("year-selector", "value"),
    prevent_initial_call=True,
)
def update_stats_products_by_sale(dfs_originales, selected_year):
    if not dfs_originales:
        return no_update

    df_ventas = pd.DataFrame(dfs_originales["ventas.csv"])
    df_ventas = df_ventas[df_ventas["year"] == int(selected_year)]
    df_productos_de_venta = pd.DataFrame(dfs_originales["productos_de_venta.csv"])

    df = (
        df_ventas.merge(df_productos_de_venta, left_on="ID", right_on="ID venta")
        .groupby("ID venta")
        .count()["ID producto"]
    )

    mean = df.mean()
    std = df.std()

    return f"{mean:,.2f}", f"{std:,.2f}", df.to_dict()


@app.callback(
    Output("estadisticas-ventas-promedio-ingreso-por-venta", "children"),
    Output("estadisticas-ventas-desviacion-ingreso-por-venta", "children"),
    Output("stored-for-excel-export-estadisticas_ventas_ingreso", "data"),
    Input("stored-data-original", "data"),
    Input("year-selector", "value"),
    prevent_initial_call=True,
)
def update_stats_income_by_sale(dfs_originales, selected_year):
    if not dfs_originales:
        return no_update

    df_ventas = pd.DataFrame(dfs_originales["ventas.csv"])
    df_ventas = df_ventas[df_ventas["year"] == int(selected_year)]
    df_productos_de_venta = pd.DataFrame(dfs_originales["productos_de_venta.csv"])

    df = (
        df_ventas.merge(df_productos_de_venta, left_on="ID", right_on="ID venta")
        .groupby("ID venta")
        .sum()["valor"]
    )

    mean = df.mean()
    std = df.std()

    return f"${mean:,.2f}", f"{std:,.2f}", df.to_dict()


@app.callback(
    Output("estadisticas-clientes-promedio-ingresos-por-cliente", "children"),
    Output("estadisticas-clientes-desviacion-ingresos-por-cliente", "children"),
    Output("stored-for-excel-export-estadisticas_clientes_ingreso", "data"),
    Input("stored-data-original", "data"),
    Input("year-selector", "value"),
    prevent_initial_call=True,
)
def update_stats_clients_income(dfs_originales, selected_year):
    if not dfs_originales:
        return no_update

    df_clientes = pd.DataFrame(dfs_originales["clientes.csv"])
    df_ventas = pd.DataFrame(dfs_originales["ventas.csv"])
    df_ventas = df_ventas[df_ventas["year"] == int(selected_year)]
    df_productos_de_venta = pd.DataFrame(dfs_originales["productos_de_venta.csv"])

    df = (
        df_clientes.merge(
            df_ventas,
            how="left",
            left_on="ID",
            right_on="Cliente",
            suffixes=("_cliente", "_venta"),
        )
        .merge(
            df_productos_de_venta, how="left", left_on="ID_venta", right_on="ID venta"
        )[["nombre", "valor"]]
        .groupby("nombre")
        .sum()["valor"]
    )

    mean = df.mean()
    std = df.std()

    return f"${mean:,.2f}", f"{std:,.2f}", df.to_dict()


@app.callback(
    Output("estadisticas-clientes-promedio-cantidad-productos", "children"),
    Output("estadisticas-clientes-desviacion-cantidad-productos", "children"),
    Output("stored-for-excel-export-estadisticas_clientes_productos", "data"),
    Input("stored-data-original", "data"),
    Input("year-selector", "value"),
    prevent_initial_call=True,
)
def update_stats_clients_product_qty(dfs_originales, selected_year):
    if not dfs_originales:
        return no_update

    df_ventas = pd.DataFrame(dfs_originales["ventas.csv"])
    df_ventas = df_ventas[df_ventas["year"] == int(selected_year)]
    df_productos_de_venta = pd.DataFrame(dfs_originales["productos_de_venta.csv"])

    df = (
        df_productos_de_venta.merge(
            df_ventas,
            left_on="ID venta",
            right_on="ID",
            suffixes=("_producto_de_venta", "_venta"),
        )[["ID producto", "Cliente"]]
        .groupby("Cliente")
        .count()["ID producto"]
    )

    mean = df.mean()
    std = df.std()

    return f"{mean:,.2f}", f"{std:,.2f}", df.to_dict()


@app.callback(
    Output("download-excel", "data"),
    inputs=dict(n_clicks=Input("exportar-excel-button", "n_clicks")),
    state=dict(
        ventas=State("stored-for-excel-export-ventas", "data"),
        productos_mas_vendidos=State(
            "stored-for-excel-export-productos_mas_vendidos", "data"
        ),
        productos_menos_vendidos=State(
            "stored-for-excel-export-productos_menos_vendidos", "data"
        ),
        ventas_por_cliente=State("stored-for-excel-export-ventas_por_cliente", "data"),
        clientes_por_productos=State(
            "stored-for-excel-export-clientes_por_productos", "data"
        ),
        estadisticas_ventas_productos=State(
            "stored-for-excel-export-estadisticas_ventas_productos", "data"
        ),
        estadisticas_ventas_ingreso=State(
            "stored-for-excel-export-estadisticas_ventas_ingreso", "data"
        ),
        estadisticas_clientes_ingreso=State(
            "stored-for-excel-export-estadisticas_clientes_ingreso", "data"
        ),
        estadisticas_clientes_productos=State(
            "stored-for-excel-export-estadisticas_clientes_productos", "data"
        ),
    ),
    prevent_initial_call=True,
)
def save_to_excel_button(n_clicks, **kwargs):
    if not n_clicks or not n_clicks > 0:
        return no_update

    with pd.ExcelWriter(path="data.xlsx") as writer:
        for k, v in kwargs.items():
            if isinstance(v, dict) and should_be_series(v):
                df = pd.Series(v)
            else:
                df = pd.DataFrame(v)
            df.to_excel(writer, sheet_name=k)

    return dcc.send_file("./data.xlsx")


def gen_tabla_productos_vendidos(dfs_originales, selected_year, size, mas: bool):
    df_ventas = pd.DataFrame(dfs_originales["ventas.csv"])
    df_ventas = df_ventas[df_ventas["year"] == int(selected_year)]
    df_productos = pd.DataFrame(dfs_originales["productos.csv"])
    df_productos_de_venta = pd.DataFrame(dfs_originales["productos_de_venta.csv"])

    return (
        df_ventas.merge(
            df_productos_de_venta,
            left_on="ID",
            right_on="ID venta",
            suffixes=("_venta", "_producto_de_venta"),
        )[["ID_venta", "ID producto", "cantidad", "valor"]]
        .rename(
            columns={
                "cantidad": "CANTIDAD_producto_en_venta",
                "valor": "VALOR_producto_en_venta",
            }
        )
        .merge(df_productos, left_on="ID producto", right_on="ID")[
            ["CANTIDAD_producto_en_venta", "VALOR_producto_en_venta", "nombre"]
        ]
        .rename(columns={"nombre": "NOMBRE_producto"})
        .groupby("NOMBRE_producto")
        .sum()
        .sort_values(by="CANTIDAD_producto_en_venta", ascending=not mas)
        .head(size)
        .reset_index()
        .rename(
            columns={
                "NOMBRE_producto": "Producto",
                "CANTIDAD_producto_en_venta": "Unidades vendidas",
                "VALOR_producto_en_venta": "Valor total",
            }
        )
        .to_dict("records")
    )


def should_be_series(s: dict):
    for v in s.values():
        if isinstance(v, dict) or isinstance(v, list):
            return False
    return True


clientside_callback(
    """
    function(nClicks) {
        if (!(nClicks > 0)) return;
        savePDF();
    }
    """,
    Input("savePDF-button", "n_clicks"),
)


@app.callback(
    Output("csv-modal", "is_open"),
    [Input("open-modal-button", "n_clicks"), Input("close-modal-button", "n_clicks")],
    [State("csv-modal", "is_open")],
)
def toggle_modal(open_click, close_click, is_open):
    if open_click or close_click:
        return not is_open
    return is_open


@app.callback(
    Output("csv-tabs", "children"),
    Input("stored-data-original", "data"),
)
def update_tabs(dfs_originales):
    if not dfs_originales:
        return []

    tabs = []
    for idx, (file_name, data) in enumerate(dfs_originales.items()):
        df = pd.DataFrame(data)

        tab = dbc.Tab(
            label=file_name,  # Nombre del archivo en la pestaña
            tab_id=f"tab-{idx}",
            children=[
                dash_table.DataTable(
                    columns=[{"name": col, "id": col} for col in df.columns],
                    data=df.to_dict("records"),
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "textAlign": "left",
                        "color": "#FFFFFF",
                        "backgroundColor": "#222222",
                    },
                    style_header={"fontWeight": "bold"},
                )
            ],
        )
        tabs.append(tab)

    return tabs


# =============================
# 5. EJECUCION DE LA APLICACION
# =============================

if __name__ == "__main__":
    app.run_server(debug=True)


# TwT lloros de desarrollador a las 12am

# Baby come back, any kind of fool could see♪
# There was something in everything about you♪
# Baby come back, yeah, you can blame it all on me♪
#'Cause I was wrong, and I just can't live without you♪

# -PLAYER
