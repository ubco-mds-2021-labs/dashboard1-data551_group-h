import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import json
from dash import Input, Output, State, MATCH, ALL

# cars = data.cars()

#data
import pandas as pd
import numpy as np

df = pd.read_csv("tuition_cost.csv")
df['index1'] = df.index
testdf = df.head(10)


app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True

testbutton = html.Div(
    [
        dbc.Button("test", size = "sm", id="test"),
    ],
    className="d-grid gap-2 d-md-flex justify-content-md-end",
)


def generate_school_items(n=9):
    schoolitems = []
    for i in range(n):
        cur_row = testdf.iloc[i]
        cur_btn = html.Div(
            [
                dbc.Button("Select", size = "sm", id={
                    'type': 'selectbtn',
                    'index': int(cur_row["index1"])
                }, value=i),
            ],
            className="d-grid gap-2 d-md-flex justify-content-md-end",
        )
        if cur_row["type"] == "Public":
            schooltype_color = "text-success"
        elif cur_row["type"] == "Private":
            schooltype_color = "text-warning"
        else:
            schooltype_color = "text-info"
        schoolitem = dbc.ListGroupItem(
            [
                html.Div(
                    [
                        html.H5(cur_row["name"], className="mb-1"),
                        html.Small(cur_row["type"], className=schooltype_color),
                    ],
                    className="d-flex w-100 justify-content-between",
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div([
                            html.Small([
                                html.Span("Room and Board: ", className="text-muted"),
                                str(cur_row["room_and_board"])
                            ], className="mb-1")
                        ])),
                        dbc.Col(html.Div([
                            html.Small([
                                html.Span("Instate Tuition: ", className="text-muted")
                            ], className="mb-1"),
                            html.Small([
                                str(cur_row["in_state_tuition"])
                            ], className="mb-1")
                        ])),
                        dbc.Col(html.Div([
                            html.Small([
                                html.Span("Outstate Tuition: ", className="text-muted")
                            ], className="mb-1"),
                            html.Small([
                                str(cur_row["out_of_state_tuition"])
                            ], className="mb-1")
                        ])),
                        dbc.Col(html.Div([
                            html.Small([
                                html.Span("Instate Total: ", className="text-muted"),
                                str(cur_row["in_state_total"])
                            ], className="mb-1")
                        ])),
                        dbc.Col(html.Div([
                            html.Small([
                                html.Span("Outstate Total: ", className="text-muted"),
                                str(cur_row["out_of_state_total"])
                            ], className="mb-1")
                        ])),
                        dbc.Col(html.Div([
                            cur_btn
                        ])),
                    ],style = {"margin-top":"8px"},align="end"
                ),
            ], style = {"width":"822px", "margin": "auto"}
        )
        schoolitems.append(schoolitem)

    return schoolitems


## Layout
app.layout = dbc.Container([
    html.Div( 
    [
        dbc.ListGroup(id="schoollist",children=generate_school_items()),
        testbutton,
        html.Div(children="Test", id="print")

    ], style = {"overflow": "auto", "width":"870px", "height":"400px", "margin": "auto", "margin-top":"50px"})
])



@app.callback(
    Output('schoollist','children'),
    Input('test', 'n_clicks'), prevent_initial_call=True)
def update_schoollist(xcol=1):
    return generate_school_items(xcol)



@app.callback(
    Output('print', 'children'),
    Input({'type': 'selectbtn', 'index': ALL}, 'n_clicks'), prevent_initial_call=True
)
def update_print(args):
    schoolid = -1
    if len(dash.callback_context.triggered) == 1:
        jsonstr = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
        jsonobj = json.loads(jsonstr)
        schoolid = jsonobj["index"]
    return schoolid


if __name__ == "__main__":
    app.run_server(host="127.0.0.1", debug=True)