import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-10/tuition_cost.csv')
df_filtered = df
#state_avg_instate = 
nation_avg_instate = sum(df_filtered['in_state_total'])/len(df_filtered['in_state_total'])
df_filtered = pd.DataFrame({
        "Type": ["National Average", "State Average"],
        "Tuition": [nation_avg_instate, sum(df_filtered.in_state_total)/len(df_filtered.in_state_total)]
    })

# list of US states
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


# Dashboard
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([

    # Dropdown menu for School Type, Degree length, State
    html.Div([
        dcc.Markdown('''###### School Type '''),
        dcc.Dropdown(id='school-type', options = ['Private', 'Public', 'For-profit'], value = 'Private'),
        dcc.Markdown('''###### Degree Length '''),
        dcc.Dropdown(id='degree-length', options = ['4 Year', '2 Year'], value = '4 Year'),
        dcc.Markdown('''###### State '''),
        dcc.Dropdown(id='state', options = state_list, value = 'California')
    ]),

    # In-state/Out-of-state & Room and board
    html.Div([
        dcc.RadioItems(['In-state', 'Out-of-state'], 'In-state', inline=True),
        dcc.RadioItems(['Room and board', 'No room and board'], 'Room and board', inline=True)
    ]),
    
    # Tuition Range Slider
    html.Div([
        dcc.Markdown('''###### Tuition Rangae '''),
        dcc.RangeSlider(0, 80000, 10000, value=[30000, 60000], id='my-range-slider')
    ]),

    # Tuition and Salary bar plot 
    html.Div(
        className='Chart Row',
        children=[plot1, plot2]
    ),

    #plot1,
    #plot2,

    html.Div(id='output-container-range-slider'),
    html.Div(id='dd-output-container-school-type')

])


## Callback functions
@app.callback(
    Output('bar_chart_tuition','srcDoc'), # Specifies where the output "goes"
    Input('school-type', 'value'),
    Input('degree-length', 'value'),
    Input('state', 'value'))
def update_plot(type = 'Private', degree = '4 Year', state = 'California', data=df):
    newdata = data[(data.state == state) & (data.degree_length == degree) & (data.type == type)]
    new_df = pd.DataFrame({
        "Type": ["National Average", "State Average"],
        "Tuition": [nation_avg_instate, sum(newdata.in_state_total)/len(newdata.in_state_total)]
    })
    newplot = plot_bar(xcol = 'Type', ycol='Tuition', data = new_df)
    return newplot

"""
@app.callback(
    #Output('bar_chart_tuition','srcDoc'), # Specifies where the output "goes"
    Input('school-type', 'value'),
    Input('degree-length', 'value'),
    Input('state', 'value'))
def update_data(type = 'Private', degree = '4 Year', state = 'California', data=df):
    newdf = data[(data.State == state) & (data.Degree_length == degree) & (data.Type == type)]
    return newdf
"""
if __name__ == "__main__":
    app.run_server(host="127.0.0.3", debug=True)