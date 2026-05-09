import pandas as pd #Importamos esta librería para manipulación y análisis de datos (filtrar, agrupar, limpiar datasets).
from dash import Dash, dcc, html #Dash es para la creación del dashboard web interactivo.Dash: inicializa la app.# dcc: componentes interactivos (gráficos, sliders, dropdowns)
#html: estructura visual (divs, títulos, textos)
from dash.dependencies import Input, Output #Permite la interactividad en Dash (callbacks): conecta acciones del usuario con actualizaciones en los gráficos.
import plotly.express as px #Sirve para creación rápida de gráficos interactivos
import plotly.io as pio #sirve para configuración global de gráficos (templates, estilos, exportación).

# ------------------- CONFIG -------------------

pio.templates.default = "plotly_white" #Le dice a todos los gráficos de Plotly que usen por defecto el estilo blanco.
app = Dash(__name__) #Inicializamos la aplicación Dash.
server = app.server
df_global = pd.read_csv("df_energia_global.csv") #Cargamos el archivo CSV en un DataFrame de pandas.

df_arg = pd.read_csv("dataset_arg.csv") #Cargamos el archivo CSV con datos de Argentina en un DataFrame de pandas.
# ------------------- GRUPOS DE PAÍSES -------------------

nombres_grupos = { #Definimos listas de países agrupados
    "Grupo 1": [
        "Noruega", "Emiratos Árabes Unidos", "Bélgica", "España",
        "Corea, República de", "México", "Turquía", "Sudáfrica",
        "Colombia", "Egipto, República Árabe de", "Nigeria"
    ],
    "Grupo 2": [
        "Estados Unidos", "Alemania", "Reino Unido", "Nueva Zelandia",
        "Portugal", "Polonia", "Federación de Rusia", "Kazajstán",
        "Irán, República Islámica del", "Indonesia", "Uzbekistán"
    ],
    "Grupo 3": [
        "Suecia", "Australia", "Canadá", "Italia",
        "Arabia Saudita", "Argentina", "Venezuela", "Rumania",
        "Tailandia", "Ucrania", "India"
    ],
    "Grupo 4": [
        "Países Bajos", "Japón", "Francia", "Kuwait",
        "República Checa", "Chile", "Brasil", "Malasia",
        "China", "Argelia"
    ]
}

# ------------------- ESTILOS -------------------
#Guardamos colores y estilos en variables.
BG_COLOR = "#f5f7fb"
CARD_BG = "white"
TEXT = "#1f2a44"
MUTED = "#6b7280"
PRIMARY = "#3559E0"
BORDER = "1px solid #e5e7eb"

#Definimos cómo se van a ver: el título principal, los subtítulos, las cards y KPI

TITLE_STYLE = {
    "textAlign": "left",
    "fontSize": "34px",
    "fontWeight": "700",
    "margin": "0 0 8px 0",
    "color": TEXT
}

SUBTEXT_STYLE = {
    "fontSize": "15px",
    "color": MUTED,
    "margin": "0 0 24px 0"
}

CARD_STYLE = {
    "backgroundColor": CARD_BG,
    "borderRadius": "16px",
    "boxShadow": "0 4px 14px rgba(0,0,0,0.06)",
    "padding": "18px",
    "border": BORDER
}

KPI_CARD_STYLE = {
    "backgroundColor": CARD_BG,
    "borderRadius": "16px",
    "boxShadow": "0 4px 14px rgba(0,0,0,0.06)",
    "padding": "18px",
    "border": BORDER,
    "flex": "1",
    "minWidth": "220px"
}

SECTION_TITLE_STYLE = {
    "fontSize": "20px",
    "fontWeight": "700",
    "color": TEXT,
    "margin": "8px 0 14px 0"
}


#Con esta función de pandas chequeamos si n es un valor faltante, si lo es coloca N/D y sino continúa con la función
def formato_grande(n):
    if pd.isna(n): 
        return "N/D"
    if n >= 1_000_000_000:
       return f"{n/1e9:.1f}B" #.1f significa mostrar el número con 1 decimal en formato flotante
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}k" 

    return f"{n:.1f}"

def calcular_kpis(df, year): #Función para calcular los KPI
    df_year = df[df["Year"] == year].copy() #Filtra solo las filas del año seleccionado.
    

    co2_total = df_year["CO2_ton"].sum() #Suma todo el CO₂ de ese año.
    consumo_total = df_year["Energy consumption"].sum() #Suma todo el consumo energético de ese año.
    renovables_prom = df_year["Renewables"].mean() #Como es porcentaje en este caso calculamos el promedio de renovables.

    return co2_total, consumo_total, renovables_prom


# ------------------- DATOS BASE -------------------
#Para el slider de año hace estas dos líneas de código:
#obtiene todos los años del dataset, los ordena y elige el último como valor inicial
years_disponibles = sorted(df_global["Year"].dropna().astype(int).unique()) 
year_default = max(years_disponibles)

# ------------------- FIGURA 1: EVOLUCIÓN TEMPORAL -------------------
#Agrupa por año los datos del dataset y suma el CO2 total de cada año.
df_co2_year = df_global.groupby("Year", as_index=False)["CO2_ton"].sum()

fig_co2 = px.line( #Crea un gráfico de línea con x= year e y= CO2_ton
    df_co2_year,
    x="Year",
    y="CO2_ton",
    title="Evolución global de las emisiones de CO₂",
    labels={
        "Year": "Año",
        "CO2_ton": "Emisiones de CO₂ (ton)"
    }
)

fig_co2.update_traces(line=dict(color=PRIMARY, width=3)) #Después se cambia: color de la línea, tamaño
fig_co2.update_layout( #Aca modificamos el layout, o sea, todo lo visual que rodea al gráfico
    title_x=0.03, #mueve el título hacia la izquierda (0 = izquierda, 0.5 = centro)
    title_font=dict(size=20, color=TEXT), #definimos cómo se ve el título
    paper_bgcolor="white", #fondo total (incluye márgenes)
    plot_bgcolor="white", #fondo solo del área donde están los datos
    font=dict(color=TEXT), #Define el color del texto de todo el gráfico (ejes, labels, etc.)
    height=360, #Tamaño del gráfico, altura en pixeles
    margin=dict(l=30, r=20, t=60, b=40) #Espacio alrededor del gráfico
)
fig_co2.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)") #Definimos que muestre líneas de la grilla y el color, esto es para el eje x y abajo el eje y
fig_co2.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")

# ------------------- FIGURA 2: CONSUMO VS EMISIONES -------------------

fig_consumo_renovables = px.scatter( #Creamos un scatter donde: X = consumo energético total, Y = emisiones totales, color = porcentaje de renovables para 
    #estudiar como se relaciona consumo, emisiones y energía renovable
    df_global,
    x="Energy consumption",
    y="CO2_ton",
    color="Renewables",
    title="Consumo total vs emisiones totales",
    labels={
        "Energy consumption": "Consumo de energía (TWh)",
        "CO2_ton": "Emisiones de CO₂ (ton)",
        "Renewables": "% Energías renovables"
    },
    hover_data=["Country Name", "Year"], #Con esto definimos la info que aparece cuando pasás el mouse sobre un punto
    color_continuous_scale="YlGnBu", #Definimos la paleta de colores cuando los datos son continuos (numéricos)
    opacity=0.72 #Controla la transparencia de los puntos 
)

fig_consumo_renovables.update_xaxes( #Definimos el eje X
    type="log", #Escala logarítmica
    showgrid=True, #Muestra las líneas de fondo de la grilla
    gridcolor="rgba(0,0,0,0.10)", #color de la grilla
    exponentformat="power", # formato de números en los ejes, los muestra como potencias
    minor=dict(showgrid=False), #Oculta los “minor ticks” que son líneas intermedias entre potencias
    tickfont=dict(size=10) #Tamaño del texto en el eje
)
#Lo mismo que para el eje X
fig_consumo_renovables.update_yaxes(
    type="log",
    showgrid=True,
    gridcolor="rgba(0,0,0,0.10)",
    exponentformat="power",
    minor=dict(showgrid=False),
    tickfont=dict(size=10)
)

fig_consumo_renovables.update_layout(
    title_x=0.03, #título alineado a la izq
    title_font=dict(size=20, color=TEXT), #Tamaño del título y color
    paper_bgcolor="white", #fondo total (incluye márgenes)
    plot_bgcolor="white",#fondo solo del área donde están los datos
    font=dict(color=TEXT), #Color de todo el texto
    height=430, #Altura del gráfico
    margin=dict(l=30, r=20, t=60, b=40), #Espaciado alrededor del gráfico
    coloraxis_colorbar=dict( #Esto controla la barra que indica el significado del color para renovables
        title="% Renovables", #Nombre de la variable representada por el color
        thickness=16, #Ancho de la barra
        len=0.72 #Largo de la barra
    ))
# ------------------- FIGURA 3: HEATMAP -------------------
    # calculamos la correlación entre las variables para estudiar qué tan relacionadas están entre sí
df_corr = df_global[[
    "CO2_ton",
    "CO2_per_capita_ton",
    "Energy consumption",
    "Electricity",
    "Renewables",
    "Poblacion",
    "PBI per capita"
]]
df_corr.columns = [ #Cambiamos el nombre de las variables para que sea más entendible el heatmap
    "Emisiones de CO₂ (toneladas)",
    "Emisiones de CO₂ per cápita",
    "Consumo energético",
    "Producción eléctrica",
    "Energías renovables (%)",
    "Población",
    "PBI per cápita"
]
corr = df_corr.corr() #Calculamos la matriz de correlación entre las variables seleccionadas

# Creamos heatmap
fig_heatmap = px.imshow( #Convierte esa matriz que le pasamos con corr en un gráfico de colores (heatmap)
    corr,
    color_continuous_scale="Blues", #Usa una escala de color azul.
    title="Matriz de correlación entre variables"
)

# Estética
fig_heatmap.update_layout( #Modifica el diseño general del heatmap.
    title_x=0.03, #Mueve el título hacia la izquierda.
    title_font=dict(size=20, color=TEXT), #Define tamaño y color del título.
    paper_bgcolor="white",#Fondo total de la figura.
    plot_bgcolor="white", #Fondo del área donde está el gráfico.
    font=dict(color=TEXT), #Color general del texto: ejes, labels, etc.
    height=520, #Altura del gráfico.
    margin=dict(l=120, r=40, t=80, b=120), #Márgenes internos del gráfico
     xaxis=dict(
        tickangle=-90), #Rota los nombres del eje X. -90 hace que queden verticales y se lean de abajo hacia arriba.
        coloraxis_colorbar=dict( #Controla la barra de color.
        x=0.85,   # mover más cerca del gráfico la barra
        thickness=18,
        len=0.7
    )
    )
# ------------------- FIGURAS ARGENTINA -------------------

fig_arg_renov = px.line( #Creamos un gráfico de líneas con Plotly
    df_arg,
    x="Year",
    y="Generación renovable (GWh)",
    markers=True, #Agrega puntos en cada dato
    title="Renovables",
    labels={
        "Year": "Año",
        "Generación renovable (GWh)": "Generación de Energía renovable (GWh)"
    }
)

fig_arg_demanda = px.line(
    df_arg,
    x="Year",
    y="Demanda energética",
    markers=True,
    title="Demanda",
    labels={
        "Year": "Año",
        "Demanda energética": "Demanda eléctrica"
    }
)

fig_arg_emision = px.line(
    df_arg,
    x="Year",
    y="tCO2_MWh_real",
    markers=True,
    title="Emisión",
    labels={
        "Year": "Año",
        "tCO2_MWh_real": "Factor de emisión (tCO₂/MWh)"
    }
)


for fig in [fig_arg_renov, fig_arg_demanda, fig_arg_emision]: #este for nos permite usar el mismo estilo a los 3 gráficos
    fig.update_traces(line=dict(width=3), marker=dict(size=7)) #Se indica con esto cómo se ven los datos (la línea mas gruesa y agranda los puntos)
    fig.update_layout(#con esto vamos a modificar el diseño general del gráfico
        title_x=0.5, #centra el título
        title_font=dict(size=18, color=TEXT), #tamaño y color del título
        paper_bgcolor="white", #fondo total blanco
        plot_bgcolor="white", #fondo del gráfico blanco
        font=dict(color=TEXT), #Se define el color de todos los textos
        height=340, #altura del gráfico
        margin=dict(l=40, r=20, t=60, b=40) #espacio alrededor del gráfico
    )
    #Configuración los ejes del gráfico
    fig.update_xaxes(showgrid=True,   #muestra las líneas de fondo (la grilla)
                    gridcolor="rgba(0,0,0,0.08)", #color de la grilla
                    linecolor="black",#color del eje (la línea del borde)
                    linewidth=1.2, #rosor del eje
                    mirror=True ) #dibuja el eje en ambos lados
    fig.update_yaxes(showgrid=True,
                     gridcolor="rgba(0,0,0,0.08)",
                     linecolor="black",
                    linewidth=1.2,
                    mirror=True)


# ------------------- LAYOUT ------------------- (Layout general de la app)
#Es toda la estructura visible del dashboard, el esqueleto de la página
app.layout = html.Div( #HTML div es un contenedor que agrupa elementos
    style={
        "backgroundColor": BG_COLOR,# color de fondo de toda la app
        "padding": "28px", #espacio interno (separa el contenido de los bordes)
        "fontFamily": "Arial, sans-serif" #tipo de letra
    },
    children=[ #el contenido dentro del contenedor
        #Es una lista de componentes. Cada elemento es algo que se va a mostrar en pantalla. todo lo q uno quiere mostrar va dentro de children

        html.H1("Emisiones de CO₂ y transición energética", style=TITLE_STYLE), #Título principal 
        html.Div("Análisis global", style=SECTION_TITLE_STYLE),

        html.P(
            "Análisis de factores asociados a las emisiones, su relación con el consumo energético y la transición hacia energías renovables.", #Subtítulo
            style=SUBTEXT_STYLE
        ),

        # Selector de año
        html.Div( #contenedor del selector agrupa todo el bloque del selector
            style={**CARD_STYLE, "marginBottom": "24px"}, #**CARD_STYLE: copia todo el diccionario dentro del otro q es style, con margin Agrega espacio debajo
              #del componente, separa de lo q viene después
            children=[
                html.Div("Seleccioná un año", style=SECTION_TITLE_STYLE), #html.Div: contenedor simple de texto, Seleccioná un año": texto visible,
                # style=SECTION_TITLE_STYLE: estilo. 
                dcc.Slider( #Definimos la creación del slider: componente interactivo para elegir valores
                    id="year-slider", #identificador
                    min=min(years_disponibles), #Definimos el rango del slider, valor min y max
                    max=max(years_disponibles),
                    value=year_default, #Año que aparece seleccionado al cargar la app
                    marks={int(y): str(int(y)) for y in years_disponibles}, #es un diccionario para que cada año seleccionado en el 
                    #slider lo pase a texto 
                    step=None #Hace que el slider solo pueda tomar valores reales, no valores intermedios como 2007.3
                )
            ]
        ),

        # KPIs
        html.Div( 
            style={#Definimos el estilo de las tarjetas
                "display": "flex", #pone los elementos uno al lado del otro (horizontal)
                "gap": "18px", #espacio entre tarjetas
                "flexWrap": "wrap", #permite que bajen de línea si no entran
                "marginBottom": "24px" #espacio debajo del bloque
            },
            children=[ #Acá están las 4 tarjetas KPI
                html.Div([
                    html.Div("Año analizado", style={"fontSize": "13px", "color": MUTED}), #Etiqueta de texto, lo que vemos y el estilo
                    html.H3(id="kpi-year", style={"margin": "8px 0 0 0", "fontSize": "28px", "color": TEXT}) 
                ], style=KPI_CARD_STYLE),#id="kpi-year" identificador y todo el estilo para mostrar el KPI del año

                html.Div([
                    html.Div("CO₂ total global", style={"fontSize": "13px", "color": MUTED}),
                    html.H3(id="kpi-co2", style={"margin": "8px 0 4px 0", "fontSize": "28px", "color": TEXT})
                ], style=KPI_CARD_STYLE), #id="kpi-co2" identificador y todo el estilo para mostrar el KPI de las emisiones totales

                html.Div([
                    html.Div("Consumo total", style={"fontSize": "13px", "color": MUTED}),
                    html.H3(id="kpi-consumo", style={"margin": "8px 0 4px 0", "fontSize": "28px", "color": TEXT})
                ], style=KPI_CARD_STYLE), #id="kpi-consumo" identificador y todo el estilo para mostrar el KPI del consumo total

                html.Div([
                    html.Div("Renovables promedio", style={"fontSize": "13px", "color": MUTED}),
                    html.H3(id="kpi-renov", style={"margin": "8px 0 4px 0", "fontSize": "28px", "color": TEXT})
                ], style=KPI_CARD_STYLE), #id="kpi-renov" identificador y todo el estilo para mostrar el KPI del promedio de la utilización de las energías renovables
            ]
        ),

        # Evolución temporal
        html.Div( #contenedor que agrupa todo lo relacionado con la evolución temporal
            style={**CARD_STYLE, "marginBottom": "24px"}, #aplica el estilo base y margin espacio debajo
            children=[ #Lo que vemos de ese contenedor
                html.Div("Evolución temporal", style=SECTION_TITLE_STYLE), #Título y estilo, es el encabezado de esta sección del dashboard
                dcc.Graph(figure=fig_co2, config={"displayModeBar": False}), #dcc. graph: Componente de Dash para mostrar gráficos de Plotly, le pasamos el 
                #gráfico que creamos antes (fig_co2)
                #config={"displayModeBar": False: Oculta la barra flotante de Plotly (zoom, descargar, etc.)
                html.Div( #creamos un contenedor debajo del grafico con un texto explicativo 
                    "Las emisiones globales muestran una trayectoria creciente a lo largo del tiempo, acompañando la expansión de la actividad energética.",
                    style={"fontSize": "14px", "color": MUTED, "marginTop": "6px"}
                )
            ]
        ),

        # Dos gráficos
        html.Div( #contenedor de los dos gráficos
            style={
                "display": "flex", #pone los elementos en fila
                "gap": "24px", #espacio entre los dos gráficos
                "flexWrap": "wrap" #si no entran, pasan a la siguiente línea
            },
            children=[ #Son dos html.Div, cada uno es una card con su gráfico. Una card en este caso es un contenedor visual que agrupa información relacionada.

                html.Div( #contenedor para el primer gráfico
                    style={**CARD_STYLE, "flex": "1", "minWidth": "500px"}, #Estilo de la card1
                    children=[ #contenido
                        html.Div("Relación consumo-emisiones", style=SECTION_TITLE_STYLE), #Título y estilo del mismo
                        dcc.Graph(figure=fig_consumo_renovables, config={"displayModeBar": False}), #Gráfico ya creado anteriormente
                        html.Div( #texto interpretativo
                            "Los países con mayor consumo total tienden a presentar mayores emisiones. El color muestra la participación de energías renovables.",
                            style={"fontSize": "14px", "color": MUTED, "marginTop": "6px"}
                        )
                    ]
                ),

                html.Div( #Igual estructura visual del gráfico 2 que el anterior
                    style={**CARD_STYLE, "flex": "1", "minWidth": "500px"},
                    children=[
                        html.Div("PBI y emisiones per cápita", style=SECTION_TITLE_STYLE),
                        dcc.Graph(id="grafico-pbi-dinamico", config={"displayModeBar": False}), #No tiene un gráfico definido antes, sino que 
                        #el gráfico se va a generar con un callback
                        html.Div( #Bloque interactivo debajo del gráfico
                            [
                                html.P(
                                    "Seleccioná un grupo de países:", #Texto guía 
                                    style={
                                        "textAlign": "center", #estilo del texto guía
                                        "margin": "8px 0 8px 0",
                                        "fontWeight": "600",
                                        "color": TEXT
                                    }
                                ),
                                dcc.Dropdown( #Creamos el dropdown para la seleccion de los países
                                    id="dropdown-grupos",#Identificador para conectar con el callback
                                    options=[
                                        {"label": "Grupo 1", "value": "Grupo 1"},
                                        {"label": "Grupo 2", "value": "Grupo 2"},
                                        {"label": "Grupo 3", "value": "Grupo 3"},
                                        {"label": "Grupo 4", "value": "Grupo 4"}
                                    ],
                                    value="Grupo 2", #Opción seleccionada al inicio
                                    clearable=False, #No se puede borrar la selección
                                    style={ #estilo 
                                        "width": "65%", #ancho del dropdown
                                        "margin": "0 auto" #centrado horizontal
                                    }
                                ),
                                html.Div( #creamos un contenedor debajo del grafico con un texto explicativo 
                                "Existe una tendencia positiva entre ingreso y emisiones, aunque con gran variabilidad entre países, indicando que el nivel de ingreso no es el único determinante.",
                                style={"fontSize": "14px", "color": MUTED, "marginTop": "6px"}
                                )
                            ],
                            
                            style={"marginTop": "6px"}
                        )
                    ]
                 )
             ]
        ),
                        # Heatmap de correlaciones
                                html.Div( #contenedor externo que permite controlar la alineación y el espaciado
                                style={"display": "flex", #activa Flexbox que permite alinear fácilmente lo que está adentro
                                "justifyContent": "center",  #centra horizontalmente el contenido
                                "marginTop": "24px" #agrega espacio arriba
                                },
                                 children=[ #Lo que esta dentro del contenedor que es la card. Este primer children dice "el contenedor externo tiene UNA cosa: la card",
                                     #sin este children no podriamos centrar la card. 

                                html.Div( #el contenedor interno (card) agrupa los elementos visuales como el título, el gráfico y la descripción.
                                style={**CARD_STYLE,
                                "width": "100%" #ocupa todo el ancho disponible
                                },
                                children=[#contenido de la card, lo que se ve dentro, este segundo dice el contenido que tiene esa card
                                html.Div("Relaciones entre variables", style=SECTION_TITLE_STYLE),

                                dcc.Graph( #Gráfico
                                figure=fig_heatmap,#el heatmap que creamos con Plotly
                                config={"displayModeBar": False},#oculta la barra de herramientas (zoom, guardar, etc.)
                                style={"height": "520px"} #define altura del gráfico
                                ),

                                html.Div( #contenedor con texto explicativo del heatmap
                                "Las emisiones de CO₂ están fuertemente asociadas al consumo energético " \
                                "y la producción eléctrica. En cambio, las emisiones per cápita muestran " \
                                "una relación más clara con el nivel de ingreso.",
                                style={"fontSize": "14px", "color": MUTED, "marginTop": "6px"}
                        )
                    ]
                )
            ]
       ),

# Argentina
html.Div(
    style={**CARD_STYLE, "marginTop": "24px"},
    children=[
        html.Div("Análisis de Argentina", style=SECTION_TITLE_STYLE),

        html.P(
            "Se analiza la evolución de la generación de energías renovables, la demanda eléctrica y el factor de emisión para evaluar cambios recientes en la matriz energética argentina.",
            style={"fontSize": "14px", "color": MUTED, "marginTop": "0"}
        ),

        # 3 gráficos
        html.Div(
            style={
                "display": "flex",
                "gap": "24px",
                "flexWrap": "wrap",
                "marginTop": "16px"
            },
            children=[
                html.Div(
                    style={"flex": "1", "minWidth": "320px"},
                    children=[dcc.Graph(figure=fig_arg_renov, config={"displayModeBar": False})]
                ),
                html.Div(
                    style={"flex": "1", "minWidth": "320px"},
                    children=[dcc.Graph(figure=fig_arg_demanda, config={"displayModeBar": False})]
                ),
                html.Div(
                    style={"flex": "1", "minWidth": "320px"},
                    children=[dcc.Graph(figure=fig_arg_emision, config={"displayModeBar": False})]
                ),
            ]
        ),

        
        html.Div(
            "En Argentina, la generación renovable muestra una tendencia creciente, mientras que la demanda eléctrica se estabiliza en los últimos años y el factor de emisión disminuye. Esto sugiere una mejora relativa en la intensidad de emisiones del sistema eléctrico.",
            style={"fontSize": "14px", "color": MUTED, "marginTop": "12px"}
        )
    ]
),

# CONCLUSIONES 
html.Div(
    style={**CARD_STYLE, "marginTop": "24px"},
    children=[
        html.Div("Conclusiones", style=SECTION_TITLE_STYLE),

        html.Div(
            [
                html.P(
                    "En síntesis, el análisis evidencia que las emisiones de CO₂ están estrechamente vinculadas al consumo energético y a la producción eléctrica a nivel global.",
                    style={"marginBottom": "8px"}
                ),
                html.P(
                    "Asimismo, las métricas per cápita permiten observar una relación más clara con el nivel de ingreso, aunque con variabilidad entre países.",
                    style={"marginBottom": "8px"}
                ),
                html.P(
                    "En el caso de Argentina, el aumento en la generación de energías renovables se asocia con una disminución del factor de emisión, lo que sugiere avances en la transición energética.",
                    style={"marginBottom": "8px"}
                ),
                html.P(
                    "Estos resultados indican que políticas orientadas a reducir el consumo energético y promover el uso de energías renovables podrían contribuir a mitigar las emisiones de CO₂ y su impacto ambiental."
                )
            ],
                    style={
                        "fontSize": "14px",
                        "color": MUTED,
                        "marginTop": "12px",
                        "lineHeight": "1.6"
                    }
                )
             ]
        )
    ]
)
# ------------------- CALLBACK KPIS -------------------

@app.callback( #Función de Dash que se ejecuta automáticamente cuando cambian los Inputs
    Output("kpi-year", "children"), #Cada Output dice que componente actualizar (id) y que propiedad cambiar (children)
    Output("kpi-co2", "children"),
    Output("kpi-consumo", "children"),
    Output("kpi-renov", "children"),
    Input("year-slider", "value") #Esto significa que cuando cambie el año del slider..
)
#Como se conectan los input y output con la función: el Input (slider) manda el valor: year, la función usa ese year y devuelve resultados que van a los Output
def actualizar_kpis(year):
    co2_total, consumo_total, renovables_prom = calcular_kpis(df_global, year) #Ejecutá la función calcular_kpis(df_global, 
    #year) y guarda los 3 resultados que devuelve en estas 3 variables

    return ( #Esta función devuelve valores para llenar los Output
        str(year), #Convierte el año a texto. Va al KPI del año.
        f"{formato_grande(co2_total)} ton", #El valor calculado de co2_total es utilizado en la función formato_grande, que fue definida más arriba,
        #para que quede en un lindo formato para mostrar
        f"{formato_grande(consumo_total)} TWh",
        f"{renovables_prom:.1f}%"
    )
#Conclusión de esta parte: la función recibe año seleccionado calcula KPIs para ese año, formatea los valores como texto, devuelve textos y estilos, Dash 
# los muestra en las tarjetas

# ------------------- CALLBACK GRÁFICO PBI -------------------

@app.callback( #Este callback actualiza el gráfico de PBI cada vez que elegís un grupo en el dropdown.
    Output("grafico-pbi-dinamico", "figure"),
    Input("dropdown-grupos", "value") #Cuando cambie el valor de dropdown-grupos, que se actualice la figure del grafico con id:"grafico-pbi-dinamico"
)
def actualizar_grafico(grupo_seleccionado): #Se define la función que se ejecuta cuando cambia el dropdown.

    paises_seleccionados = nombres_grupos[grupo_seleccionado] #Busca qué países pertenecen a ese grupo.
    

    df_filtrado = df_global[df_global["Country Name"].isin(paises_seleccionados)] #Filtra el dataframe para quedarse solo con los países seleccionados.
    df_filtrado = df_filtrado.dropna(subset=["PBI per capita", "CO2_per_capita_ton", "Year"])#Elimina filas que tengan datos faltantes en esas columnas porque 
    #sin esos datos no podés graficar bien.
    df_filtrado = df_filtrado[df_filtrado["PBI per capita"] > 0] #Se queda solo con filas donde el PBI per cápita sea mayor a 0, porque después usa escala 
    #logarítmica, y en log no pueden entrar valores 0 o negativos.

    #Conclusión: Dropdown cambia entonces se identifica el grupo elegido, se buscan los países de ese grupo, se filtra df_global,se limpian datos faltantes
    #se eliminan PBI menores o iguales a 0, si no queda nada, muestra gráfico vacío

    if df_filtrado.empty: #Pregunta si después de filtrar no quedó ningún dato.
        return px.scatter(title="No hay datos válidos para el grupo seleccionado") #Si no hay datos válidos, devuelve un gráfico vacío con ese título.

    fig = px.scatter( #Esta parte construye el gráfico dinámico que después devuelve el callback.
        df_filtrado, #Se hace un grafico de dispersión con datos el dataframe ya filtrado, o sea, solo los países del grupo seleccionado.
        x="PBI per capita",
        y="CO2_per_capita_ton",
        color="Country Name", #Cada país aparece con un color distinto
        title=f"PBI per cápita vs emisiones de CO₂ per cápita<br>{grupo_seleccionado}", #f"..." permite insertar variables dentro del texto
        labels={
            "PBI per capita": "PBI per cápita",
            "CO2_per_capita_ton": "Emisiones de CO₂ per cápita (ton)",
            "Country Name": "País"
        },
        hover_data=["Year"], #Cuando pasás el mouse sobre un punto, también muestra el año.
        opacity=0.82, #Hace los puntos un poco transparentes.
        color_discrete_sequence=px.colors.qualitative.Set2 #Define la paleta de colores para los países.Como Country Name es una variable categórica, 
        #se usa una escala discreta.
    )

    fig.update_xaxes( #Modifica el eje X.
        type="log", #El eje X usa escala logarítmica
        tickmode="array", #Significa que vamos a definir manualmente dónde van los ticks y lo hacemos con los tickvals y ticktext
        tickvals=[500, 1000, 2000, 5000, 10000, 20000, 50000],
        ticktext=["500", "1k", "2k", "5k", "10k", "20k", "50k"],
        showgrid=True, #Muestra una grilla suave en el eje X.
        gridcolor="rgba(0,0,0,0.10)"
    )

    fig.update_yaxes(
        type="linear", #El eje Y queda lineal, no logarítmico.
        showgrid=True,
        gridcolor="rgba(0,0,0,0.10)"
    )

    fig.update_layout( #Ajusta el diseño general.
        title_x=0.03, #Mueve el título hacia la izquierda.
        title_font=dict(size=20, color=TEXT), #Define tamaño y color del título.
        paper_bgcolor="white", #Fondo blanco para toda la figura 
        plot_bgcolor="white",# y para el área del gráfico.
        font=dict(color=TEXT), #Color general del texto.
        legend_title_text="País", #Título de la leyenda.
        height=430, #Altura del gráfico.
        margin=dict(l=30, r=20, t=70, b=40), #Márgenes: izquierda, derecha, arriba, abajo.
        legend=dict(font=dict(size=11)) #Tamaño de letra de la leyenda.
    )

    return fig #Devuelve el gráfico terminado. Esa fig va al Output. O sea Dash toma esta figura y la muestra dentro de: dcc.Graph(id="grafico-pbi-dinamico")

# ------------------- RUN -------------------

if __name__ == "__main__":
    app.run(debug=True)
    
    