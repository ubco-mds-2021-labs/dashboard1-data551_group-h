from turtle import width
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import pandas as pd
import numpy as np
from vega_datasets import data

universities_tuition = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-10/tuition_cost.csv")
universities_salary = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-10/salary_potential.csv')

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

states = alt.topo_feature(data.us_10m.url, feature='states')

variable_list = ['Instate_tuition', 'Outstate_tuition', 'Early_career_pay', 'mid_career_pay']

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

def plot_map_us(option = 'Instate_tuition'):
    if option == 'Instate_tuition':
        map_us = alt.Chart(states).mark_geoshape().encode(
            color='Instate_tuition:Q',
            tooltip=[
                alt.Tooltip('state:N', title='State'),
                alt.Tooltip('Instate_tuition:Q', title='Instate Tuition Fees')
                ]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(universities_info, 'id', list(universities_info.columns))
                ).properties(
                    width=300,
                    height=300
                    ).project(
                        type='albersUsa'
                        ).configure(background='#E6E6FA')

    elif option == 'Outstate_tuition':
        map_us = alt.Chart(states).mark_geoshape().encode(
            color='Outstate_tuition:Q',
            tooltip=[
                alt.Tooltip('state:N', title='State'),
                alt.Tooltip('Outstate_tuition:Q', title='Outstate Tuition Fees')
                ]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(universities_info, 'id', list(universities_info.columns))
                ).properties(
                    width=300,
                    height=300
                    ).project(
                        type='albersUsa'
                        ).configure(background='#E6E6FA')
    elif option == 'Early_career_pay':
        map_us = alt.Chart(states).mark_geoshape().encode(
            color='Early_career_pay:Q',
            tooltip=[
                alt.Tooltip('state:N', title='State'),
                alt.Tooltip('Early_career_pay:Q', title='Early career pay')
                ]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(universities_info, 'id', list(universities_info.columns))
                ).properties(
                    width=300,
                    height=300
                    ).project(
                        type='albersUsa'
                        ).configure(background='#E6E6FA')

    elif option == 'mid_career_pay':
        map_us = alt.Chart(states).mark_geoshape().encode(
            color='mid_career_pay:Q',
            tooltip=[
                alt.Tooltip('state:N', title='State'),
                alt.Tooltip('mid_career_pay:Q', title='Mid Career Pay')
                ]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(universities_info, 'id', list(universities_info.columns))
                ).properties(
                    width=300,
                    height=300
                    ).project(
                        type='albersUsa'
                        ).configure(background='#E6E6FA')

    return map_us.to_html()

plot1 = html.Iframe(id='altair_chart_map_us',srcDoc=plot_map_us(option = 'Instate_tuition'),
style={'width': '100%', 'height': '400px'})
map_dropdown = html.Div(dcc.Dropdown(id='chart_dropdown',value='Instate_tuition', options = [{'label': i, 'value': i} for i in universities_info.columns if i not in ['Name'] and (i == 'Instate_tuition' or i == 'Outstate_tuition' or i == 'Early_career_pay' or i == 'mid_career_pay')], style={'border-width': '3', 'width': '40%'}))
app.layout = dbc.Container([
    html.Div(children='''
        US Heat Map Based on Tuition Fees and Salaries
    ''',style={'color': 'brown', 'font-weight': 'bold'}),
    html.P(),
    dbc.Row(dbc.Col(map_dropdown)),
    dbc.Row(dbc.Col(plot1))
   ],
   )

## Callback functions
@app.callback(
    Output('altair_chart_map_us','srcDoc'),
    Input('chart_dropdown', 'value')
    )
def update_plot(option):
    return plot_map_us(option)

if __name__ == '__main__':
    app.run_server(debug=True)