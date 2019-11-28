import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as do
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#ffffff',
    'text': '#228b22'
}

df = pd.read_excel('commodity_data.xlsx')
dfx = df.iloc[0:17]

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div([
        html.P(
            children='Philippine Retail Price of Agricultural Commodities',
        style={
            'textAlign':'center',
            'color':colors['text'],
            'fontSize':30
        }
    ),

        html.P(
        children='20 Years Worth of Data (Data Source: PSA OpenStat)',
        style={
            'textAlign':'center',
            'color':colors['text'],
            'fontSize':12,
            'fontStyle':'italic'
        }
    )
    ]),

    html.Div([
        dcc.Dropdown(
            id='commodity-select',
            options=[
                {'label': 'Regular Milled Rice', 'value': 'RMR'},
                {'label': 'Ampalaya', 'value': 'AMP'},
                {'label': 'Eggplant', 'value': 'EGP'},
                {'label': 'Tomato', 'value': 'TMT'},
                {'label': 'Cabbage', 'value': 'CBB'},
                {'label': 'Kangkong', 'value': 'KAKO'},
                {'label': 'Camote Tops', 'value': 'TOP'},
                {'label': 'Pechay', 'value': 'PEC'},
                {'label': 'Carrots', 'value': 'CRR'},
                {'label': 'Sweet Potato', 'value': 'POT'},
                {'label': 'Squash', 'value': 'SQU'},
                {'label': 'Upo', 'value': 'UPO'},
                {'label': 'Coconut (matured)', 'value': 'COCO'},
                {'label': 'Banana Latundan (10pcs/kg)', 'value': 'BNN'},
                {'label': 'Mango Carabao', 'value': 'MAN'},
                {'label': 'Pineapple Hawaiian (~2.4kg/pc)', 'value': 'PNA'},
                {'label': 'Beef Meat with bones', 'value': 'BEF'},
                {'label': 'Pork Meat with bones', 'value': 'POR'},
                {'label': 'Chicken Fully Dressed', 'value': 'CFD'},
                {'label': 'Chicken Egg (21pcs/kg)', 'value': 'CEG'},
                {'label': 'Bangus', 'value': 'BAN'},
                {'label': 'Crab (Alimasag)', 'value': 'CRB'},
                {'label': 'Shrimp (Sugpo)', 'value': 'SHR'},
                {'label': 'Shrimp (Suaje)', 'value': 'SUA'},
                {'label': 'Tilapia', 'value': 'TILP'},
                {'label': 'Dilis', 'value': 'DIL'},
                {'label': 'Galunggong', 'value': 'GAL'},
                {'label': 'Tulingan', 'value': 'TUL'}
                
        ],
        value='RMR'
        )
    ],style={'width': '25%', 'display': 'block', 'marginLeft': 30}
    ),

    html.Div([
        dcc.Graph(
        id='price-chart'
    )
    ]),

    html.Div([
        dcc.Slider(
            id='year-slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=df['Year'].min(),
            marks={str(Year): str(Year) for Year in df['Year'].unique()},
            step=None
    )
    ],style={'marginBottom': 50, 'marginTop': 5, 'width':'80%',
             'marginRight':'Auto', 'marginLeft':'Auto'}
    )
])

@app.callback(
    Output('price-chart','figure'),
    [Input('commodity-select','value'),
     Input('year-slider','value')]
)
def update_chart(commodity_column, year_row):
    df_cur_price = df.loc[df['Year'] == year_row][commodity_column]
    df_cur_label = df.loc[df['Year'] == year_row]['Geolocation']

    data = do.Bar(
        x= df_cur_label,
        y= df_cur_price,
        marker_color= '#71BC78'
    )

    layout = do.Layout(
        title= 'Select a product from the upper left box. Use the slider at the bottom to set the year.',
        xaxis= {
            'title': 'Region',
            'automargin': True
        },
        yaxis= {
            'title': 'Price (in PH Peso)',
            'automargin': True,
            'showgrid': True
        },
        transition={'duration':750}
    )

    return {
        'data':[data],
        'layout': layout
    }

if __name__ == '__main__':
    app.run_server(debug=True)