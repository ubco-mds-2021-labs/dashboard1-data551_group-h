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
import altair as alt


df = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-10/tuition_cost.csv')

df['index1'] = df.index
filtered_df = df

df_filtered = df



#state_avg_instate = 
nation_avg_instate = sum(df_filtered['in_state_total'])/len(df_filtered['in_state_total'])
df_filtered = pd.DataFrame({
        "Type": ["National Average", "State Average"],
        "Tuition": [nation_avg_instate, sum(df_filtered.in_state_total)/len(df_filtered.in_state_total)]
    })



testdf = df.head(10)


app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True

testbutton = html.Div(
    [
        dbc.Button("test", size = "sm", id="test"),
    ],
    className="d-grid gap-2 d-md-flex justify-content-md-end",
)

## components

def generate_school_items(filtered_school_df):
    schoolitems = []
    for i in range(len(filtered_school_df)):
        cur_row = filtered_school_df.iloc[i]
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
                    ],style = {"marginTop":"8px"},align="end"
                ),
            ], style = {"width":"822px", "margin": "auto"}
        )
        schoolitems.append(schoolitem)

    return schoolitems


states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}
state_list = list(states.values())

# sample dataset (demo)
temp_tuition_dic = {"Type": ["National Average", "State Average", "This School"],
                    "Tuition": [60000, 55000, 65000]}
df_tuition = pd.DataFrame.from_dict(temp_tuition_dic)

# plot function for tuition
def plot_bar(xcol = 'Type', ycol='Tuition', data = df_filtered):
    chart = alt.Chart(data).mark_bar().encode(
        x=xcol,
        y=ycol,
        color = xcol).properties(
            height=400, 
            width=400
            )
    return chart.interactive().to_html()

# barchart for tuition and salary
plot1 = html.Iframe(id='bar_chart_tuition', srcDoc=plot_bar(xcol = 'Type', ycol='Tuition', data=df_filtered),
                    style={'width': '600px', 'height': '600px'})
plot2 = html.Iframe(id='bar_chart_salary', srcDoc=plot_bar(xcol = 'Type', ycol='Tuition', data=df_filtered),
                    style={'width': '600px', 'height': '600px'})                   

component_schoollist = dbc.Card([
        # html.Div("School List", style = {"margin": "auto", "width": "822px"}),
        html.H4("School List", style = {"margin": "auto", "width": "830px", "marginTop":"12px"}),
        html.Hr(style = {"margin": "10px 10px"}),
        html.Div( 
        [
            dbc.ListGroup(id="schoollist",children=[]), #generate_school_items()
        ], style = {"overflow": "auto", "height":"320px", "margin": "auto"})

    ],style = {"width":"870px", "height":"400px", "marginTop":"50px"})

component_control = dbc.Card([
       # Dropdown menu for School Type, Degree length, State
        html.Div([
            dcc.Markdown('''###### School Type '''),
            dcc.Dropdown(id='school-type', options = ['Private', 'Public', 'For-profit'], value = 'Private'),
            dcc.Markdown('''###### Degree Length '''),
            dcc.Dropdown(id='degree-length', options = ['4 Year', '2 Year'], value = '4 Year'),
            dcc.Markdown('''###### State '''),
            dcc.Dropdown(id='state', options = state_list, value = 'California')
        ],style = {"margin": "auto", "width": "440px", "marginTop":"20px"}),

        # In-state/Out-of-state & Room and board
        html.Div([
            dcc.RadioItems(options = [{"label": 'In-state', "value": 1}, {"label":'Out-of-state', "value": 0}], value = 1, id = "in-out-state", inline=True),
            dcc.RadioItems(options = [{"label": 'Room and board', "value": 1}, {"label":'No room and board', "value": 0}], id="room-board", value = 1, inline=True)
        ],style = {"margin": "auto", "width": "440px", "marginTop":"5px"}),
        
        # Tuition Range Slider
        html.Div([
            dcc.Markdown('''###### Tuition Rangae '''),
            dcc.RangeSlider(0, 80000, 10000, value=[30000, 60000], id='my-range-slider')
        ],style = {"margin": "auto", "width": "440px", "marginTop":"5px"}),

    ],style = {"width":"500px", "height":"400px", "marginTop":"50px"})

## Layout
app.layout = dbc.Container([

    dbc.Row(
        [
            dbc.Col(component_schoollist, width="auto"),
            dbc.Col(component_control, width="auto"),
        ],style = {"margin": "auto", "width": "1440px"}
    ),

    
    dbc.Card([
        # Tuition and Salary bar plot 
        html.Div(
            className='Chart Row',
            children=[plot1, plot2]
        ),

    ],style = {"width":"870px", "height":"400px", "marginTop":"50px"}),


], style = {"max-width": "2000px"})

## Callback functions
@app.callback(
    Output('bar_chart_tuition','srcDoc'), # Specifies where the output "goes"
    Input('school-type', 'value'),
    Input('degree-length', 'value'),
    Input('state', 'value'),
    # Input('in-out-state', 'value'),
    # Input('room-board', 'value')
    )
def update_plot(school_type = 'Private', degree = '4 Year', state = 'California', data=df): #, in_out_state = 1, room_board = 1
    newdata = data[(data.state == state) & (data.degree_length == degree) & (data.type == school_type)]
    new_df = pd.DataFrame({
        "Type": ["National Average", "State Average"],
        "Tuition": [nation_avg_instate, sum(newdata.in_state_total)/len(newdata.in_state_total)]
    })
    newplot = plot_bar(xcol = 'Type', ycol='Tuition', data = new_df)
    return newplot


@app.callback(
    Output('schoollist','children'), # Specifies where the output "goes"
    Input('school-type', 'value'),
    Input('degree-length', 'value'),
    Input('state', 'value'),
    # Input('in-out-state', 'value'),
    # Input('room-board', 'value')
    )
def update_schoollist(school_type = 'Private', degree = '4 Year', state = 'California', data=df):
    df_filtered = data[(data.state == state) & (data.degree_length == degree) & (data.type == school_type)]
    return generate_school_items(df_filtered)



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