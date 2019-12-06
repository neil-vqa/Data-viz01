import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as do
import pandas as pd
import numpy as np

##external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__)

server = app.server

colors = {
    'background': '#F8F9FA',
    'text': '#F8F9FA'
}

df = pd.read_excel('commodity_data.xlsx')
dfx = df.iloc[0:17]

app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.P(
                children='Philippine Retail Price of Agricultural Commodities',
                style={
                'textAlign':'right',
                'color':'#ffffff',
                'fontSize':35,
                'marginRight': 30
            })
        ],
        style={
            'backgroundColor':'#00A568'
        }),

        html.P(
        children='20 Years Worth of Data (Data Source: PSA OpenSTAT)',
        style={
            'textAlign':'right',
            'color':'#000000',
            'fontSize':12,
            'fontStyle':'italic',
            'marginRight': 30
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
    ],style={'width': '23%', 'display': 'block', 'marginLeft': 60,
             'fontSize':15}
    ),

    html.Div([
        dcc.Graph(
        id='price-chart'
    )
    ]),

    html.Div([
        html.Div([
            dcc.Slider(
                id='year-slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].min(),
                marks={str(Year): str(Year) for Year in df['Year'].unique()},
                step=None
        )
        ],style={'marginTop': 5, 'width':'80%',
                'marginRight':'Auto', 'marginLeft':'Auto'}
        )
    ]),
    
    html.Div([
    	html.P(
            children=['Built using Dash (https://github.com/neil-vqa)'],
            style={
                'fontSize':12,
                'textAlign':'center',
                'fontStyle':'italic',
                'color':'#ffffff'
            }
        )
    ],
    style={
    	'marginTop':40,
    	'backgroundColor': '#00A568'
    })
    
],style={'backgroundColor': colors['background']})

@app.callback(
    Output('price-chart','figure'),
    [Input('commodity-select','value'),
     Input('year-slider','value')]
)
def update_chart(commodity_column, year_row):
    df_cur_price = df.loc[df['Year'] == year_row][commodity_column]
    df_cur_label = df.loc[df['Year'] == year_row]['Geolocation']
    ave = df_cur_price.mean()
    dfv_min = df_cur_price.min()
    dfv_max = df_cur_price.max()

    colored = np.array(['#00A568']*df_cur_price.shape[0])
    colored[df_cur_price == dfv_min] = '#C2C3C5'
    colored[df_cur_price == dfv_max] = '#B43757'
    

    fit = do.Figure()

    data = do.Bar(
        x= df_cur_label,
        y= df_cur_price,
        marker_color= colored,
        hoverinfo='y',
        width=.7
    )

    layout = do.Layout(
        xaxis= {
            'automargin': True
        },
        yaxis= {
            'automargin': True,
            'showgrid': True
        },
        transition={'duration':750},
        paper_bgcolor='#F8F9FA',
        plot_bgcolor='#ffffff'
    )

    name = {
        'RMR':'Regular Milled Rice',
        'AMP':'Ampalaya',
        'EGP':'Eggplant',
        'TMT':'Tomatoes',
        'CBB':'Cabbage',
        'KAKO':'Kangkong',
        'TOP':'Camote tops',
        'PEC':'Pechay',
        'CRR':'Carrots',
        'POT':'Potatoes',
        'SQU':'Squash',
        'UPO':'Upo',
        'COCO':'Coconut',
        'BNN':'Bananas',
        'MAN':'Mango carabao',
        'PNA':'Pineapples',
        'BEF':'Beef',
        'POR':'Pork',
        'CFD':'Whole Chicken',
        'CEG':'Chicken eggs',
        'BAN':'Bangus',
        'CRB':'Crabs',
        'SHR':'Shrimps (sugpo)',
        'SUA':'Shrimps (suaje)',
        'TILP':'Tilapia',
        'DIL':'Dilis',
        'Gal':'Galunggong',
        'TUL':'Tulingan'
    }

    is_name = name[commodity_column]

    annotate1 = {
        'text':'National Average Price of {} for the year {}:'.format(is_name,year_row),
        'showarrow':False,
        'xref':'paper',
        'yref':'paper',
        'x':.5,
        'y':1.37,
        'font':{'size':19}
    }

    annotate2 = {
        'text':'Php {:.1f}'.format(ave),
        'showarrow':False,
        'xref':'paper',
        'yref':'paper',
        'x':.5,
        'y':1.24,
        'font':{'size':19}
    }

    fit.add_trace(data)
    fit.update_layout(layout)
    fit.update_layout(overwrite=True, annotations=[annotate1,annotate2])

    return fit

if __name__ == '__main__':
    app.run_server(debug=True)
