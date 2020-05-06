import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from get_data import filterIntoList

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background' : 'rgb(0,0,26)',
    'tested' : '#ffa31a',
    'positive' : '#ffff00',
    'death' : '#ff4d4d'
}
""" NavBar """

LOGO = "/assets/icon.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="State Abbreviation i.e 'IL'", id="state", value="IL")),
        dbc.Col(
            dbc.Button("Search", color="light", className="ml-2", id="submit-button", outline=True, n_clicks = 0),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("Coronavirus Statistics in the US", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="#1e2130",
    dark=True,
)

""" Cards """
test_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Number of People Tested", className="card-title"),
                html.Div(id='test-graph')
            ]
        ),
    ],
    style={"width": "100%",
           "height": "100%",
           "margin" : "auto",
           "background" : "#1e2130",
           "border-radius": "8px"},
)

positive_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Number of Confirmed Cases", className="card-title"),
                html.Div(id='pos-graph')
            ]
        ),
    ],
    style={"width": "100%",
           "height": "100%",
           "margin" : "auto",
           "background" : "#1e2130",
           "border-radius": "8px"},
)

death_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Number of Deaths", className="card-title"),
                html.Div(id='dea-graph')
            ]
        ),
    ],
    style={"width": "100%",
           "margin" : "auto",
           "background" : "#1e2130",
           "border" : 0,
           "border-radius": "8px"},
)


""" Layout Render """

app.layout = html.Div(children=[
    html.Div(navbar),
    html.A([
        dbc.Row([
            dbc.Col(html.Div(test_card),
            style={
                'margin-left': '15px'
            }, className='padding-0'),
            dbc.Col(html.Div(positive_card),
            style={
                'margin-right': '15px'
            },
            className='padding-0')
        ]),
        dbc.Col(html.Div(death_card), className='padding-0')
    ])
    # html.Div([html.Div(id='test-graph'),
    #     html.Div(id='pos-graph'),
    #     html.Div(id='dea-graph')
    #     ])

])

@app.callback(
    Output(component_id='test-graph', component_property='children'),
    [Input('submit-button', 'n_clicks')],
    [State(component_id='state', component_property='value')]
    )
def tested_graph(n_clicks, curr_state):
    dates, tested, _, _ = filterIntoList(curr_state)

    return dcc.Graph(
        id='tested-graph',
        animate=True,
        figure={
            'data': [
                {'x': dates, 'y': tested,
                'type': 'line',
                'mode' : 'lines+markers',
                'name': curr_state.upper(),
                'line' : {'color' : colors['tested']}
                }
            ],
            'layout': {
                'plot_bgcolor' : colors['background'],
                'paper_bgcolor' : '#1e2130',
                'yaxis' : {
                    'range' : [min(tested), max(tested)+200000]
                },
                'font' : {
                    'color' : '#FFFFFF'
                },
                'margin' : {
                    't': 0
                },
                'width' : 850
            }
        }
    )


@app.callback(
    Output(component_id='pos-graph', component_property='children'),
    [Input('submit-button', 'n_clicks')],
    [State(component_id='state', component_property='value')]
    )
def positive_graph(n_clicks, state):
    dates, _, positive, _ = filterIntoList(state)

    return dcc.Graph(
        id='positive-graph',
        animate=True,
        figure={
            'data': [
                {'x': dates,
                'y': positive,
                'type': 'line',
                'mode' : 'lines+markers',
                'name': state.upper(),
                'line' : {'color' : colors['positive']}
                }
            ],
            'layout': {
                'plot_bgcolor' : colors['background'],
                'paper_bgcolor' : '#1e2130',
                'yaxis' : {
                    'range' : [min(positive), max(positive)+50000]
                },
                'font' : {
                    'color' : '#FFFFFF'
                },
                'margin' : {
                    't': 0
                }
            }
        }
    )


@app.callback(
    Output(component_id='dea-graph', component_property='children'),
    [Input('submit-button', 'n_clicks')],
    [State(component_id='state', component_property='value')]
    )
def death_graph(n_clicks, state):
    dates, _, _, deaths = filterIntoList(state)

    return dcc.Graph(
        id='positive-graph',
        animate=True,
        figure={
            'data': [
                {'x': dates,
                'y': deaths,
                'type': 'line',
                'mode' : 'lines+markers',
                'name': state.upper(),
                'line' : {'color' : colors['death']}
                }
            ],
            'layout': {
                'plot_bgcolor' : colors['background'],
                'paper_bgcolor' : '#1e2130',
                'yaxis' : {
                    'range' : [0, max(deaths) + 1000]
                },
                'font' : {
                    'color' : '#FFFFFF'
                },
                'margin' : {
                    't': 0
                }
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)
