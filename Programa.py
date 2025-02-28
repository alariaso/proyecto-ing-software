#Aplicacion Dash: Reporte de Ventas

#recordar para visualizar la pagina es necesario instalar las librerias
#pip install (nombre de la libreria faltante)
#recordar que los archivos .csv deben encontrase en la misma carpeta que el programa para ser leidos sin problemas
#al ejecutar el codigo debe de salir algo como "Dash is running on "http://127.0.0.1:8050/"
#simple mente copien y peguen en el navegador la parte de "http://127.0.0.1:8050/" y debera mostrarse toda la pagina de forma correcta

# ===========================
# 0. IMPORTACION DE LIBRERIAS
# ===========================

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# =================================
# 1. CARGA Y PROCESAMIENTO DE DATOS
# =================================

#Se leen los 3 archivos csv proporcionados
df_pventa = pd.read_csv("productos_de_venta.csv") 
df_ventas = pd.read_csv("ventas.csv")
df_productos = pd.read_csv("productos.csv")


#Se calculan las ventas totales por cada registro (valor * cantidad) esto se usara mas adelante
df_pventa["ventas_totales"] = df_pventa["valor"] * df_pventa["cantidad"]

#Une la tabla de productos de ventas con la tabla de ventas para incorporar la fecha (es como un join xd)
df_merged = pd.merge(df_pventa, df_ventas, left_on="ID venta", right_on="ID", how="left", suffixes=("", "_venta"))

#Convierte la columna 'fecha' a datetime y extraer el año para usarse mas tarde
df_merged["fecha"] = pd.to_datetime(df_merged["fecha"])
df_merged["year"] = df_merged["fecha"].dt.year

#Une la tabla productos para obtener el nombre de cada producto de la tabla de ventas que se usara mas adelante en los graficos (es como un joun xd)
df_final = pd.merge(df_merged, df_productos, left_on="ID producto", right_on="ID", how="left", suffixes=("", "_prod"))

#Obtiene los años disponibles para el dropdown es decir el selector de mas adelante
years = sorted(df_merged["year"].unique())
year_options = [{"label": str(year), "value": str(year)} for year in years]


# =============================================================
# 2. CONFIGURACION DE LA APLICACION DASH Y ESTILOS DE LA PAGINA
# =============================================================

# === CREA LA APP ===
app = Dash(__name__)

# === COLORES DE LA PAGINA ===
COLOR_FONDO = "#222222"   # Fondo oscuro
COLOR_TEXTO = "#FFFFFF"   # Texto blanco

#lit toda la pagina ._. aqui se definen los colores de la pagina, además la distrubicion de los graficos e informacion extra de los graficos (Frontend)
app.layout = html.Div(
    style={
        "backgroundColor": COLOR_FONDO,
        "color": COLOR_TEXTO,
        "minHeight": "100vh",
        "padding": "20px",
        "fontFamily": "Arial, sans-serif"
    },
    children=[
        #Titulos principales
        html.H2("Compañía induboton SAS",
                style={"textAlign": "center", "marginBottom": "5px"}),
        html.H1("REPORTE DE VENTAS",
                style={"textAlign": "center", "marginTop": "0px", "marginBottom": "30px"}),

        #Dropdown para seleccionar el año
        html.Div(
            dcc.Dropdown(
                id="year-selector",
                options=year_options,
                value=str(years[0]),
                clearable=False,
                style={"width": "50%", "margin": "0 auto", "color": "#000000"}
            ),
            style={"textAlign": "center", "marginBottom": "30px"}
        ),

        #Subtitulos generales que muestran ventas totales y cantidad de ventas en el año seleccionado
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "marginBottom": "30px",
                "gap": "40px"
            },
            children=[
                #ventas totales
                html.Div([
                    html.H3("Ventas Totales:", style={"marginBottom": "10px"}),
                    html.Div(id="total-sales", style={"fontSize": "24px"})
                ], style={
                    "border": "1px solid #444",
                    "padding": "20px",
                    "borderRadius": "8px"
                }),
                #cantidad de ventas 
                html.Div([
                    html.H3("Cantidad de ventas:", style={"marginBottom": "10px"}),
                    html.Div(id="num-sales", style={"fontSize": "24px"})
                ], style={
                    "border": "1px solid #444",
                    "padding": "20px",
                    "borderRadius": "8px"
                }),
            ]
        ),

        #Linea separadora horizontal
        html.Hr(style={"border": "1px solid #444", "marginBottom": "30px"}),

        #Contenedor de graficos y sus respectivas secciones informativas
        html.Div([
            #Caja para el grafico de barras con información adicional sobre los productos
            html.Div([
                #Informacion del producto más vendido y menos vendido del grafico de barras
                html.Div(id="bar-info", style={"marginBottom": "20px", "fontSize": "18px"}),
                dcc.Graph(id="bar-chart", style={"height": "600px"})
            ], style={
                "width": "48%",
                "border": "1px solid #444",
                "borderRadius": "8px",
                "padding": "10px",
                "marginRight": "1%"
            }),
            #Caja para el grafico de pastel con informacion adicional sobre los productos
            html.Div([
                #Informacion del producto mas vendido y menos vendido del grafico de pastel
                html.Div(id="pie-info", style={"marginBottom": "20px", "fontSize": "18px"}),
                dcc.Graph(id="pie-chart", style={"height": "600px"})
            ], style={
                "width": "48%",
                "border": "1px solid #444",
                "borderRadius": "8px",
                "padding": "10px",
                "marginLeft": "1%"
            })
        ], style={"display": "flex", "justifyContent": "center", "marginBottom": "30px"}),

        #Linea final para separar secciones
        html.Hr(style={"border": "1px solid #444", "marginTop": "30px"})
    ]
)

# ==================================================
# 4. CALLBACK PARA ACTUALIZAR GRAFICOS E INFORMACION
# ==================================================

#Esto es lo q se encarga de relacionar el Front con el Back
#Función callback que actualiza los gráficos de barras y pastel e información adicional
#cuando se selecciona un año
@app.callback(
    Output("bar-chart", "figure"),
    Output("pie-chart", "figure"),
    Output("total-sales", "children"),
    Output("num-sales", "children"),
    Output("bar-info", "children"),
    Output("pie-info", "children"),
    Input("year-selector", "value")
)
def update_charts(selected_year):

    #Filtra los datos para el año seleccionado
    dff = df_final[df_final["year"] == int(selected_year)]

    #Agrupa por el nombre del producto y suma las ventas totales
    df_grouped = dff.groupby("nombre", as_index=False)["ventas_totales"].sum()

    #Calcula el total monetario y la cantidad total de productos vendidos en el año seleccionado
    total_monetario = dff["ventas_totales"].sum()
    total_unidades = dff["cantidad"].sum()
    total_sales_text = f"Ventas totales: ${total_monetario:,.2f}"
    num_sales_text = f"Cantidad de ventas: {total_unidades}"
    
    #Informacion adicional de los graficos:

    #Para el grafico de barras: ventas totales en $
    #Se saca el producto con mayor ventas y menor ventas (según ventas_totales)
    if not df_grouped.empty:
        max_row = df_grouped.loc[df_grouped["ventas_totales"].idxmax()]
        min_row = df_grouped.loc[df_grouped["ventas_totales"].idxmin()]
    else:
        max_row = {"nombre": "N/A", "ventas_totales": 0}
        min_row = {"nombre": "N/A", "ventas_totales": 0}
    
    #Se muestra el producto mas vendido y menos vendido
    bar_info = html.Div([
        html.Div([
            html.Strong("Producto más vendido: "),
            f"{max_row['nombre']} - US $ {max_row['ventas_totales']:,.2f}"
        ], style={"marginBottom": "10px"}),
        html.Div([
            html.Strong("Producto menos vendido: "),
            f"{min_row['nombre']} - US $ {min_row['ventas_totales']:,.2f}"
        ])
    ])

    #Para el grafico de pastel: ventas totales en %
    #se calcula el porcentaje de cada producto sobre el total de ventas agrupadas
    total_grouped = df_grouped["ventas_totales"].sum()
    if total_grouped > 0:
        max_pct = (max_row["ventas_totales"] / total_grouped) * 100
        min_pct = (min_row["ventas_totales"] / total_grouped) * 100
    else:
        max_pct = min_pct = 0

    #Se muestran el producto mas y menos vendido junto con el porcentaje correspondiente
    pie_info = html.Div([
        html.Div([
            html.Strong("Producto más vendido: "),
            f"{max_row['nombre']} - {max_pct:.1f}%"
        ], style={"marginBottom": "10px"}),
        html.Div([
            html.Strong("Producto menos vendido: "),
            f"{min_row['nombre']} - {min_pct:.1f}%"
        ])
    ])
    
    
    # === Grafico de Barras con Plotly Express ===
    bar_fig = px.bar(
        df_grouped,
        x="nombre",
        y="ventas_totales",
        title=f"Ventas Totales por Producto en {selected_year} (Barras)",
        labels={"ventas_totales": "Ventas Totales", "nombre": "Producto"},
        height=600
    )
    #Se usa el estilo oscuro en la grafica
    bar_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLOR_FONDO,
        plot_bgcolor="#333333",
        font_color=COLOR_TEXTO,
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16
    )

    # === Grafico de Pastel con Plotly Express ===
    pie_fig = px.pie(
        df_grouped,
        names="nombre",
        values="ventas_totales",
        title=f"Distribución de Ventas por Producto en {selected_year} (Pastel)",
        height=600
    )
    #Se usa el estilo oscuro en la grafica
    pie_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLOR_FONDO,
        plot_bgcolor="#333333",
        font_color=COLOR_TEXTO,
        title_font_size=20
    )
    
    return bar_fig, pie_fig, total_sales_text, num_sales_text, bar_info, pie_info

# =============================
# 5. EJECUCION DE LA APLICACION
# =============================

if __name__ == "__main__":
    app.run_server(debug=True)


#TwT lloros de desarrollador a las 12am

#Baby come back, any kind of fool could see♪
#There was something in everything about you♪
#Baby come back, yeah, you can blame it all on me♪
#'Cause I was wrong, and I just can't live without you♪ 

#-PLAYER