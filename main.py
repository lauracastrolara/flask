import numpy as np
import pandas as pd
import warnings
import plotly.io as pio
import plotly.graph_objects as go
import colorlover as cl
from   IPython.display import HTML
import urllib.request, json
from   IPython.display import HTML
from   pyproj import Proj, transform
from   dash import Dash, html, dcc, Input, Output
import plotly.express as px
import dash
from   dash.dependencies import Input, Output
from flask import Flask

# --------------------------------------------------- 3D RENDERING ------------------------------------------------------------------


# -------------- GET [X Y ] ------------------
def getxy(latitudes,longitudes):

    # Define the projection
    proj_latlon = Proj(proj='latlong',datum='WGS84')
    proj_xy     = Proj(proj="utm", zone=33, datum='WGS84')

    # Initialize empty lists for x and y
    x_values = []
    y_values = []

    # Transform each pair of coordinates
    for latitude, longitude in zip(latitudes, longitudes):
        x, y = transform(proj_latlon, proj_xy, longitude, latitude)
        x_values.append(x/1000)
        y_values.append(y/1000)

    return x_values, y_values

# -------------- DATA FRAME OPTIONS ----------------------
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
warnings.filterwarnings("ignore")
# ----------------- DATA IMPORT ----------------------
# HTTP POST (get earth coordinates (x,y,z))
url = "https://raw.githubusercontent.com/Nov05/playground-fireball/master/data/earth.json"
response = urllib.request.urlopen(url)
json_data = json.loads(response.read())
#------------------- DATA ANALYSIS -------------------
#  PARALLEL PLANET MAP
x0 = json_data['data'][0]['x']
y0 = json_data['data'][0]['y']
z0 = json_data['data'][0]['z']

#  MERIDIANS PLANET MAP
x1 = json_data['data'][1]['x']
y1 = json_data['data'][1]['y']
z1 = json_data['data'][1]['z']

#  EQUATOR PLANET MAP
x2 = json_data['data'][2]['x']
y2 = json_data['data'][2]['y']
z2 = json_data['data'][2]['z']

# --------------- COLORS ------------------------------
# Colors palette
colors = ["rgb(0,0,255)","rgb(255, 255, 255)","rgb(12, 52, 61)","rgb(106, 168, 79)","rgb(229.5,229.5,25.5)","rgb(106, 168, 79)","rgba(31, 119, 180, 0.34)","rgb(31, 119, 180)" ]
HTML(cl.to_html(colors))
color_background = 'black'                          # Background
color_lines      = 'lightblue'                      # Parallels and Meridians
color_base       = 'darkblue'                       # Base surface

opacity_base = 0.1
opacity_land = 0.8
size_lines   = 1

# -------------------- DATA PLOT -----------------------
# PRALLELS
parallels = go.Scatter3d(x=x0, y=y0, z=z0,mode='lines',marker=dict(size=size_lines,color=color_lines, opacity=opacity_base,showscale=False,line=dict(width=size_lines,color=color_base)),showlegend=False,name='Parallel')

# MERIDIANS
meridians = go.Scatter3d(x=x1,y=y1,z=z1,mode='lines',marker=dict(size=size_lines,color=color_lines,opacity=opacity_base,showscale=False,line=dict(width=size_lines,color=color_base,)),showlegend=False,name='Meridian')

# BASE
base      = go.Scatter3d(x=x2,y=y2,z=z2,mode='markers',marker=dict(size=2,color=color_base,opacity=opacity_base,showscale=False,line=dict(width=1, color=color_base)),showlegend=False,name='Base',)

# PLANET DATA
data = [parallels, meridians, base]

# ------------------- LAYOUT ---------------------------
# Scene
scene = dict(
        xaxis = dict(title="x axis",color=color_background,backgroundcolor=color_background,showaxeslabels=False,showline=False,showgrid=False,zeroline=False),
        yaxis = dict(title="y axis",color=color_background,backgroundcolor=color_background,showaxeslabels=False,showline=False,showgrid=False,zeroline=False),
        zaxis = dict(title="z axis",color=color_background,backgroundcolor=color_background,showaxeslabels=False,showline=False,showgrid=False,zeroline=False),
        )

# Layout
layout = go.Layout(autosize=False,width=1150,height=500,margin=dict( l=0,r=0,b=0,t=0),title=dict(text='PLANET EXPLORATION',x=0.6, y=0.95,font=dict(size=20,color='white',family='Times New Roman')),scene = scene,paper_bgcolor=color_background,plot_bgcolor=color_background)


# --------------------- HTML --------------------------------
# Plot 3D
fig = go.Figure(data=data, layout=layout)
pio.write_html(fig, '3DRenderPlanet.html')
#

# ---------------------- APP DASH ----------------------------

# APP
server = Flask(__name__)
app3D = Dash(__name__, server = server, url_base_pathname='/3D/')
#dash_log = Dash(__name__, server = server, url_base_pathname='/log/')
df = px.data.iris()


# ---------------------- LAYOUT -------------------------------

app3D.layout = html.Div(style={'backgroundColor': 'black','width': '100%', 'height': '100%', 'margin': '0 auto'}, children=[
    html.Div([
        html.H1('Central Module',  style={'textAlign': 'center', 'margin': '0px', 'fontFamily': 'Times New Roman', 'color': 'black','fontSize': '25px','backgroundColor': 'lightgrey'})]),
    html.Div(style = {'display': 'flex', 'justify-content': 'center', 'flex-direction': 'row'}, children=[
        html.Button( 'SEQUENCER'   , id='btn-1', n_clicks=0, style={'margin': '5px', 'fontFamily': 'Times New Roman', 'backgroundColor': '#6495ED', 'color': 'white', 'border': 'none', 'padding': '15px 27px', 'textAlign': 'center', 'textDecoration': 'none', 'display': 'inline-block', 'fontSize': '22px', 'width':'200px', 'height': '80px'}),
        html.Button('CURRENT TASKS', id='btn-2', n_clicks=0, style={'margin': '5px', 'fontFamily': 'Times New Roman', 'backgroundColor': '#6495ED', 'color': 'white', 'border': 'none', 'padding': '15px 27px', 'textAlign': 'center', 'textDecoration': 'none', 'display': 'inline-block', 'fontSize': '22px', 'width':'200px', 'height': '80px'}),
        html.Button( 'EXPLORED'    , id='btn-3', n_clicks=0 ,style={'margin': '5px', 'fontFamily': 'Times New Roman', 'backgroundColor': '#6495ED', 'color': 'white', 'border': 'none', 'padding': '15px 27px', 'textAlign': 'center', 'textDecoration': 'none', 'display': 'inline-block', 'fontSize': '22px', 'width':'200px', 'height': '80px'}),
    ]),
    html.Div(style={'borderTop': '2px solid white'}),
    html.Div([
        dcc.Graph(id ='3DPlanet', figure=fig),
        dcc.Interval(id='interval-component',interval=5*1000, n_intervals=0)
    ])
])

# -------------- CALLBACK TO UPDATE PLOT ---------------------------
@app3D.callback(
    Output('3DPlanet', 'figure'),
    Input ('btn-1', 'n_clicks'),
    Input ('btn-2', 'n_clicks'),
    Input ('btn-3', 'n_clicks'),
    [Input('interval-component', 'n_intervals')])
def update(btn1,btn2,btn3,n_clicks):

    # ------------------ GET UPDATED DATA --------------------------

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]


    # ******************* TEST **************************
    random = go.Scatter3d(x=[np.random.randint(0,2000)], y=[np.random.randint(0,2000)],z=[np.random.randint(0,2000)],mode='markers',marker=dict(size=4,color='orange',opacity=1,showscale=False,line=dict(width=1, color='orange')),showlegend=False,name='Random',text = 'random')

    if 'btn-1' in changed_id:
        #return fig.add_trace(sequencer)
        fig.data = fig.data[0:3]
        fig.add_trace(random)
        # pio.write_html(fig, '3DRenderPlanet.html')

    elif 'btn-2' in changed_id:
        # return fig.add_trace(explored)
        fig.data = fig.data[0:3]
        fig.add_trace(random)
        # pio.write_html(fig, '3DRenderPlanet.html')

    elif 'btn-3' in changed_id:
        # return fig.add_trace(tasks)
        fig.data = fig.data[0:3]
        fig.add_trace(random)
        # pio.write_html(fig, '3DRenderPlanet.html')

    #elif sequencer is not None and explored is not None and tasks is not None:
        #return fig.add_trace(sequencer).add_trace(explored).add_trace(tasks)
    else:
        fig.add_trace(random)


    return fig

@server.route('/')
def hello():
    return 'Welcome!'


if __name__ == "__main__":


    server.run(debug=True)
