import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import json
from dash import Input, Output, State, MATCH, ALL

#data
import pandas as pd
import numpy as np
import altair as alt


df = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-10/tuition_cost.csv')
universities_salary = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-10/salary_potential.csv')
universities_tuition = df

df['index1'] = df.index
filtered_df = df

df_filtered = df # tuition dataframe
salary_filtered = universities_salary # salary dataframe

merged_df = pd.merge(df, universities_salary, how='inner', on='name')

# national average instate_total for tuition
nation_avg_instate = sum(df_filtered['in_state_total'])/len(df_filtered['in_state_total'])
nation_avg_outstate = sum(df_filtered['out_of_state_total'])/len(df_filtered['out_of_state_total'])

# national average early_career_pay for salary
nation_avg_early = sum(salary_filtered['early_career_pay'])/len(salary_filtered['early_career_pay'])

# national average mid_career_pay for salary
nation_avg_mid = sum(salary_filtered['mid_career_pay'])/len(salary_filtered['mid_career_pay'])

df_filtered = pd.DataFrame({
        "Type": ["National Average", "State Average", "This School"],
        "Tuition": [nation_avg_instate, sum(df_filtered.in_state_total)/len(df_filtered.in_state_total),0]
    })

new_df_test = pd.DataFrame({
    "Type": ["National Average", "State Average", "This School"],
    "Early Career": [4, 5, 0],
    "Mid Career": [7, 8, 0]
})
new_df_test_long = pd.melt(new_df_test, id_vars=['Type'], var_name='Career Stage', value_name='salary')

testdf = df.head(10)


app = dash.Dash(__name__, title='US School Finder Dashboard', external_stylesheets = [dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server
app.config.suppress_callback_exceptions = True

testbutton = html.Div(
    [
        dbc.Button("test", size = "sm", id="test"),
    ],
    className="d-grid gap-2 d-md-flex justify-content-md-end",
)

## components

## heatmap

universities_tuition = universities_tuition.rename(columns={
    "name": "Name", 
    "state": "State", 
    "state_code": "State_code",
    "type": "Type",
    "degree_length": "Degree_length",
    "room_and_board": "Room_and_Board",
    "in_state_tuition": "Instate_tuition",
    "in_state_total": "Instate_total",
    "out_of_state_tuition": "Outstate_tuition",
    "out_of_state_total": "Outstate_total"
})

universities_salary = universities_salary.rename(columns={
    "rank": "Rank", 
    "name": "Name", 
    "state_name": "State_name",
    "early_career_pay": "Early_career_pay",
    "mid_career_pay": "mid_career_pay",
    "make_world_better_percent": "make_world_better_percent",
    "stem_percent": "stem_percent"
})

universities_tuition.dropna(inplace = True)
state_tuition = universities_tuition.groupby(['State'])[['Instate_tuition','Outstate_tuition']].mean()
state_tuition = state_tuition.reset_index(level=['State'])

state_tuition.loc[7.5] = "District of Columbia", 6152, 26045
state_tuition = state_tuition.sort_index().reset_index(drop=True)

state_tuition.loc[50.5] = "Puerto Rico", 4109, 6733
state_tuition = state_tuition.sort_index().reset_index(drop=True)

universities_salary.dropna(inplace = True)
state_salary = universities_salary.groupby(['State_name'])[['Early_career_pay','mid_career_pay']].mean()
state_salary = state_salary.reset_index(level=['State_name'])

state_salary.loc[7.5] = "District of Columbia", 80439, 106800
state_salary = state_salary.sort_index().reset_index(drop=True)

state_salary.loc[50.5] = "Puerto Rico", 25332, 56108
state_salary = state_salary.sort_index().reset_index(drop=True)

universities_info = data.population_engineers_hurricanes()

universities_info['Outstate_tuition'] = state_tuition['Outstate_tuition']
universities_info['Instate_tuition'] = state_tuition['Instate_tuition']
universities_info['Early_career_pay'] = state_salary['Early_career_pay']
universities_info['mid_career_pay'] = state_salary['mid_career_pay']

universities_info.drop(columns=['population', 'engineers', 'hurricanes'], inplace=True)

states_url = alt.topo_feature(data.us_10m.url, feature='states')

variable_list = ['Instate_tuition', 'Outstate_tuition', 'Early_career_pay', 'mid_career_pay']


def plot_map_us(option = 'Instate_tuition'):
    if option == 'Instate_tuition':
        map_us = alt.Chart(states_url).mark_geoshape().encode(
            color = alt.Color('Instate_tuition:Q', legend=alt.Legend(
        orient='none',
        legendX=100, legendY=-50,
        direction='horizontal',
        titleAnchor='middle',
        gradientLength = 250,
        title = "Avg Instate Tution Fees (USD)")),
            tooltip=[
                alt.Tooltip('state:N', title='State'),
                alt.Tooltip('Instate_tuition:Q', title='Instate Tuition Fees')
                ]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(universities_info, 'id', list(universities_info.columns))
                ).properties(
                    width=470,
                    height=250
                    ).project(
                        type='albersUsa'
                        )#.configure(background='#E6E6FA')
        
        map_us.configure_legend(
            gradientLength=400
)

    elif option == 'Outstate_tuition':
        map_us = alt.Chart(states_url).mark_geoshape().encode(
            color=alt.Color('Outstate_tuition:Q', legend=alt.Legend(
        orient='none',
        legendX=100, legendY=-50,
        direction='horizontal',
        titleAnchor='middle',
        gradientLength = 300,
        title = "Avg Outstate Tution Fees (USD)")),
            tooltip=[
                alt.Tooltip('state:N', title='State'),
                alt.Tooltip('Outstate_tuition:Q', title='Outstate Tuition Fees')
                ]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(universities_info, 'id', list(universities_info.columns))
                ).properties(
                    width=470,
                    height=250
                    ).project(
                        type='albersUsa'
                        )#.configure(background='#E6E6FA')
    elif option == 'Early_career_pay':
        map_us = alt.Chart(states_url).mark_geoshape().encode(
            color=alt.Color('Early_career_pay:Q', legend=alt.Legend(
        orient='none',
        legendX=100, legendY=-50,
        direction='horizontal',
        titleAnchor='middle',
        gradientLength = 250,
        title = "Avg Early Career Pay (USD)")),
            tooltip=[
                alt.Tooltip('state:N', title='State'),
                alt.Tooltip('Early_career_pay:Q', title='Early career pay')
                ]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(universities_info, 'id', list(universities_info.columns))
                ).properties(
                    width=470,
                    height=250
                    ).project(
                        type='albersUsa'
                        )#.configure(background='#E6E6FA')

    elif option == 'mid_career_pay':
        map_us = alt.Chart(states_url).mark_geoshape().encode(
            color=alt.Color('mid_career_pay:Q', legend=alt.Legend(
        orient='none',
        legendX=100, legendY=-50,
        direction='horizontal',
        titleAnchor='middle',
        gradientLength = 250,
        title = "Avg Mid Career Pay (USD)")),
            tooltip=[
                alt.Tooltip('state:N', title='State'),
                alt.Tooltip('mid_career_pay:Q', title='Mid Career Pay')
                ]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(universities_info, 'id', list(universities_info.columns))
                ).properties(
                    width=470,
                    height=250
                    ).project(
                        type='albersUsa'
                        )#.configure(background='#E6E6FA')

    return map_us.to_html()

plot_map = html.Iframe(id='altair_chart_map_us',srcDoc=plot_map_us(option = 'Instate_tuition'),
style={'width': '100%', 'height': '400px'})
map_dropdown = html.Div(dcc.Dropdown(id='chart_dropdown',value='Instate_tuition', options = [{'label': i, 'value': i} for i in universities_info.columns if i not in ['Name'] and (i == 'Instate_tuition' or i == 'Outstate_tuition' or i == 'Early_career_pay' or i == 'mid_career_pay')], style={'border-width': '3', 'width': '250px'}))



## school list
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
    bars = alt.Chart(data).mark_bar().encode(
        alt.X('Tuition:Q',
            scale=alt.Scale(domain=(0, 60000))
        ),
        y=xcol,
        color = xcol
        ).properties(
            height=200, 
            width=185
            )

    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='Tuition:Q'
    )
    chart = (bars + text)
    return chart.interactive().to_html()

# plot function for salary
def plot_bar_salary(x = 'Career Stage', y='salary', color='Career Stage', row='Type', data=new_df_test_long):
    bars = alt.Chart(data).mark_bar().encode(
        x=y,
        y=x,
        color=alt.Color('Career Stage', legend=alt.Legend(title="Career Stage")),
        row=row
        ).properties(
            height=60, 
            width=180
            )
    '''
    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='salary:Q'
    )
    chart = (bars + text)
    '''

    return bars.interactive().to_html()  

# barchart for tuition and salary
plot1 = html.Iframe(id='bar_chart_tuition', srcDoc=plot_bar(xcol = 'Type', ycol='Tuition', data=df_filtered),
                    style={'width': '420px', 'height': '350px'})
plot2 = html.Iframe(id='bar_chart_salary', srcDoc=plot_bar_salary(x = 'Career Stage', y='salary', color='Career Stage', row='Type', data = new_df_test_long),
                    style={'width': '420px', 'height': '350px'})                   
## Instate/Outstate switch botton
button_group = html.Div(
    [
        dbc.RadioItems(
            id="in-out-state",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": 'In-state', "value": 1}, 
                {"label":'Out-of-state', "value": 0}
            ],
            value=1,
            style = {"width": "100%"}
        ),
    ],
    className="radio-group",
    style = {"margin": "auto", "width": "440px", "marginTop":"20px"}
)


component_schoollist = dbc.Card([
        # html.Div("School List", style = {"margin": "auto", "width": "822px"}),
        html.H4("School List", style = {"margin": "auto", "width": "830px", "marginTop":"12px"}),
        html.Hr(style = {"margin": "10px 10px"}),
        html.Div( 
        [
            dbc.ListGroup(id="schoollist",children=[]), #generate_school_items()
        ], style = {"overflow": "auto", "height":"320px", "margin": "auto"})

    ],style = {"width":"870px", "height":"400px", "marginTop":"20px"})

component_control = dbc.Card([
       # Dropdown menu for School Type, Degree length, State
        html.Div([
            dcc.Markdown('''###### School Type '''),
            dcc.Dropdown(id='school-type', options = ['Private', 'Public', 'For Profit'], value = 'Private', style = {"marginBottom":"20px"}),
            dcc.Markdown('''###### Degree Length '''),
            dcc.Dropdown(id='degree-length', options = ['4 Year', '2 Year'], value = '4 Year', style = {"marginBottom":"20px"}),
            dcc.Markdown('''###### State '''),
            dcc.Dropdown(id='state', options = state_list, value = 'California', style = {"marginBottom":"20px"}),
            button_group
        ],style = {"margin": "auto", "width": "440px", "marginTop":"20px"}),

        # # In-state/Out-of-state & Room and board
        # html.Div([
        #     dcc.RadioItems(options = [{"label": 'In-state', "value": 1}, {"label":'Out-of-state', "value": 0}], value = 1, id = "in-out-state", inline=True),
        #     dcc.RadioItems(options = [{"label": 'Room and board', "value": 1}, {"label":'No room and board', "value": 0}], id="room-board", value = 1, inline=True)
        # ],style = {"margin": "auto", "width": "440px", "marginTop":"5px"}),
        
        # # Tuition Range Slider
        html.Div([
            dcc.Markdown('''###### Tuition Range '''),
            dcc.RangeSlider(0, 80000, 10000, value=[0, 80000], id='my-range-slider')
        ],style = {"margin": "auto", "width": "440px", "marginTop":"5px"}),
        

    ],style = {"width":"500px", "height":"400px", "marginTop":"20px"})

component_heatmap = dbc.Card([

        dbc.Row([
            dbc.Col(html.H4("US Heat Map"), width="auto"),
            dbc.Col(map_dropdown, width="auto")
        ], justify="between", style = {"margin": "auto", "width": "480px", "marginTop":"12px"}),
        dbc.Row([
            html.Hr(style = {"margin": "10px 10px", "width": "460px"}),
        ], style = {"margin": "auto", "width": "480px"}),
        # html.Div(children='''
        #         US Heat Map
        #     ''',style={'color': 'brown', 'font-weight': 'bold'}),
            # html.P(),
            # dbc.Row(dbc.Col(map_dropdown)),
        dbc.Row(dbc.Col(plot_map))

    ],style = {"width":"500px", "height":"400px", "marginTop":"20px"})


component_barchart = dbc.Card([
        # Tuition and Salary bar plot 
        html.Div(
            className='Chart Row',
            children=[plot1, plot2],
            style = {"marginTop":"48px"}
        ),

    ],style = {"width":"870px", "height":"400px", "marginTop":"20px"}),



## Layout
app.layout = dbc.Container([

    dbc.Row(
        [
            dbc.Col(component_heatmap, width="auto"),
            dbc.Col(component_schoollist, width="auto"),
            
        ],style = {"margin": "auto", "width": "1440px"}
    ),

    dbc.Row(
        [
            dbc.Col(component_control, width="auto"),
            dbc.Col(component_barchart, width="auto"),
        ],style = {"margin": "auto", "width": "1440px"}
    ),
    


], style = {"max-width": "2000px"})

# Callback functions for tuition chart
@app.callback(
    Output('bar_chart_tuition','srcDoc'), # Specifies where the output "goes"
    Input('school-type', 'value'),
    Input('degree-length', 'value'),
    Input('state', 'value'),
    Input('in-out-state', 'value'),
    Input('my-range-slider', 'value'),
    Input({'type': 'selectbtn', 'index': ALL}, 'n_clicks'), prevent_initial_call=True
    # Input('room-board', 'value')
    )
def update_plot(school_type, degree, state, instate, tuition_range, args, data=df, schoolindex = 0): #, in_out_state = 1, room_board = 1
    schoolid = -1
    if len(dash.callback_context.triggered) == 1:
        jsonstr = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
        if "index" in jsonstr:
            jsonobj = json.loads(jsonstr)
            schoolid = jsonobj["index"]
    
    tuition_lower = tuition_range[0]
    tuition_upper = tuition_range[1]

    if instate == 1:
        nation_data =data[(data.degree_length == degree) & (data.type == school_type)]
        if len(nation_data.in_state_total) == 0:
            nation_avg_instate = 0
        else:
            nation_avg_instate = sum(nation_data.in_state_total)/len(nation_data.in_state_total)

        newdata = data[(data.state == state) & (data.degree_length == degree) & (data.type == school_type)]
        if schoolid == -1:
            cur_school_tuition = 0
        else:
            schoolindex = schoolid
            
            cur_school_tuition = newdata[newdata["index1"] == schoolindex].in_state_total
            if len(cur_school_tuition) == 0:
                cur_school_tuition = 0
            else:
                cur_school_tuition = cur_school_tuition.iloc[0]
        
        # cur_school_tuition = newdata[newdata["index1"] == schoolindex].in_state_total
        # if len(cur_school_tuition) == 0:
        #     cur_school_tuition = 0
        # else:
        #     cur_school_tuition = cur_school_tuition[0]

        if len(newdata.in_state_total) == 0:
            in_state_total_avg = 0
        else:
            in_state_total_avg = sum(newdata.in_state_total)/len(newdata.in_state_total)

        new_df = pd.DataFrame({
            "Type": ["National Average", "State Average", "This School"],
            "Tuition": [round(nation_avg_instate), round(in_state_total_avg), round(cur_school_tuition)]
        })
    else:
        nation_data =data[(data.degree_length == degree) & (data.type == school_type)]
        if len(nation_data.out_of_state_total) == 0:
            nation_avg_outstate = 0
        else:
            nation_avg_outstate = sum(nation_data.out_of_state_total)/len(nation_data.out_of_state_total)


        newdata = data[(data.state == state) & (data.degree_length == degree) & (data.type == school_type)]
        if schoolid == -1:
            cur_school_tuition = 0
        else:
            schoolindex = schoolid
            
            cur_school_tuition = newdata[newdata["index1"] == schoolindex].out_of_state_total
            if len(cur_school_tuition) == 0:
                cur_school_tuition = 0
            else:
                cur_school_tuition = cur_school_tuition.iloc[0]
        

        if len(newdata.out_of_state_total) == 0:
            out_state_total_avg = 0
        else:
            out_state_total_avg = sum(newdata.out_of_state_total)/len(newdata.out_of_state_total)

        new_df = pd.DataFrame({
            "Type": ["National Average", "State Average", "This School"],
            "Tuition": [round(nation_avg_outstate), round(out_state_total_avg), round(cur_school_tuition)]
        })

    
   
    newplot = plot_bar(xcol = 'Type', ycol='Tuition', data = new_df)
    return newplot

# Callback functions for salary chart
@app.callback(
    Output('bar_chart_salary','srcDoc'), # Specifies where the output "goes"
    Input('school-type', 'value'),
    Input('degree-length', 'value'),
    Input('state', 'value'),
    Input('in-out-state', 'value'),
    Input('my-range-slider', 'value'),
    Input({'type': 'selectbtn', 'index': ALL}, 'n_clicks'), prevent_initial_call=True
    # Input('in-out-state', 'value'),
    # Input('room-board', 'value')
    )
def update_plot(school_type, degree, state, instate, tuition_range, args, merged_df = merged_df, schoolindex = 0): #, in_out_state = 1, room_board = 1
    schoolid = -1
    if len(dash.callback_context.triggered) == 1:
        jsonstr = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
        if "index" in jsonstr:
            jsonobj = json.loads(jsonstr)
            schoolid = jsonobj["index"]
    
    tuition_lower = tuition_range[0]
    tuition_upper = tuition_range[1]


    newdata = merged_df[(merged_df.state_name == state) & (merged_df.degree_length == degree) & (merged_df.type == school_type)]
        
    
    if schoolid == -1:
        cur_school_early_salary = 0
        cur_school_mid_salary = 0
    else:
        schoolindex = schoolid
        
        cur_school_early_salary = merged_df[merged_df["index1"] == schoolindex].early_career_pay
        if len(cur_school_early_salary) == 0:
            cur_school_early_salary = 0
        else:
            cur_school_early_salary = cur_school_early_salary.iloc[0]

        cur_school_mid_salary = merged_df[merged_df["index1"] == schoolindex].mid_career_pay
        if len(cur_school_mid_salary) == 0:
            cur_school_mid_salary = 0
        else:
            cur_school_mid_salary = cur_school_mid_salary.iloc[0]
    
    # cur_school_tuition = newdata[newdata["index1"] == schoolindex].in_state_total
    # if len(cur_school_tuition) == 0:
    #     cur_school_tuition = 0
    # else:
    #     cur_school_tuition = cur_school_tuition[0]

    if len(newdata.early_career_pay) == 0:
        early_career_pay = 0
    else:
        early_career_pay = sum(newdata.early_career_pay)/len(newdata.early_career_pay)

    if len(newdata.mid_career_pay) == 0:
        mid_career_pay = 0
    else:
        mid_career_pay = sum(newdata.mid_career_pay)/len(newdata.mid_career_pay)

    new_df = pd.DataFrame({
        "Type": ["National Average", "State Average", "This School"],
        "Early Career": [nation_avg_early, early_career_pay, cur_school_early_salary],
        "Mid Career": [nation_avg_mid, mid_career_pay, cur_school_mid_salary]
    })
    new_df_long = pd.melt(new_df, id_vars=['Type'], var_name='Career Stage', value_name='salary')
    newplot = plot_bar_salary(x = 'Career Stage', y='salary', color='Career Stage', row='Type', data = new_df_long)
    return newplot


@app.callback(
    Output('schoollist','children'), # Specifies where the output "goes"
    Input('school-type', 'value'),
    Input('degree-length', 'value'),
    Input('state', 'value'),
    Input('in-out-state', 'value'),
    Input('my-range-slider', 'value'),
    # Input('room-board', 'value')
    )
def update_schoollist(school_type, degree, state, instate,tuition_range, data=df):
    tuition_lower = tuition_range[0]
    tuition_upper = tuition_range[1]
    if instate == 1:
        filtered_df = data[(data.state == state) & (data.degree_length == degree) & (data.type == school_type) & (data.in_state_total >= tuition_lower) & (data.in_state_total <= tuition_upper)]
    else:
        filtered_df = data[(data.state == state) & (data.degree_length == degree) & (data.type == school_type) & (data.out_of_state_total >= tuition_lower) & (data.out_of_state_total <= tuition_upper)]
    
    # filtered_df = data[(data.state == state) & (data.degree_length == degree) & (data.type == school_type)]
    return generate_school_items(filtered_df)



## Callback functions
@app.callback(
    Output('altair_chart_map_us','srcDoc'),
    Input('chart_dropdown', 'value')
    )
def update_plot_map(option):
    return plot_map_us(option)


if __name__ == "__main__":
    app.run_server(host="127.0.0.4")
