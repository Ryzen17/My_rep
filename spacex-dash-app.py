import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
    
url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"    
data=pd.read_csv(url)
print(data.info())

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "SpaceX Launch Records Dashboard"
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

     html.Div([
        html.Label("Select a site:"),
        dcc.Dropdown(id='site-dropdown',
                options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                ],
                value='ALL',
                placeholder="Select a Launch Site here",
                searchable=True
                )
     ]),
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display':'flex'}),
        dcc.Graph(id='success-pie-chart'),
    html.Div([
        html.Label('Payload Range (kg):',style={'margin-top':'20px'}),
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            marks={0: '0', 2500:'2500',5000:'5000',7500:'7500',10000: '10000'},
            value=[0, 10000]
        )
        
    ]),
        dcc.Graph(id='success-payload-scatter-chart')    
       
    ])
])
         

# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
        
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(data, values='class',names='Launch Site',title='Total Successful launches by site') 
        return fig
    else:
        s=data[data['Launch Site']==entered_site]
        fig = px.pie(s,names='class',title=f"Total successful launches for {entered_site}") 
        return fig
        
      

#callback

@app.callback(
        Output(component_id='success-payload-scatter-chart', component_property='figure'),
         [Input(component_id='site-dropdown', component_property='value'), 
          Input(component_id='payload-slider', component_property='value')]
     )
              
def get_scatter_chart(entered_site,payload_range):
    low,high=payload_range
    filtered_df=data[(data['Payload Mass (kg)']>=low)& (data['Payload Mass (kg)']<=high)]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)',y='class', color='Booster Version Category',title='Correlation between Payload and success for all sites') 
        fig.update_layout(
            xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1000
        ))
        return fig
    else:
        filtered_df=filtered_df[filtered_df['Launch Site']==entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)',y='class', color='Booster Version Category',title=f'Correlation between Payload and success for the {entered_site}site') 
        fig.update_layout(
            xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1000
        ))
        return fig


if __name__ == '__main__':
    app.run(debug=True)