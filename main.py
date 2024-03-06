import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc


df = pd.read_csv('csv/pm25_new.csv')


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

pollutants = ['PM25','O3', 'WS','TEMP', 'RH', 'WD']
columns = [{'label': col, 'value': col} for col in df.columns if col in pollutants]
columns.append({'label': 'All Pollutants', 'value': 'all'})


app.layout = html.Div([
    html.Div([
        dcc.DatePickerSingle(
            id='start-date-picker',
            min_date_allowed=pd.to_datetime('2023-12-01'),
            max_date_allowed=pd.to_datetime('2024-02-27'),
            initial_visible_month=pd.to_datetime('2023-12-01'),
            date=pd.to_datetime('2024-01-01'),
            display_format='YYYY-MM-DD'
        ),
        dcc.DatePickerSingle(
            id='end-date-picker',
            min_date_allowed=pd.to_datetime('2023-12-01'),
            max_date_allowed=pd.to_datetime('2024-02-27'),
            initial_visible_month=pd.to_datetime('2024-02-27'),
            date=pd.to_datetime('2024-03-01'),
            display_format='YYYY-MM-DD'
        ),
        dcc.Dropdown(
            id='dropdown',
            options=columns,
            value='PM25'  
        ),
        dcc.Graph(id='air-quality-graph')
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='example-scatter-plot')
        ], className="six columns"),
        html.Div([
            dcc.Graph(id='pie-chart')
        ], className="six columns")
    ], className="row"),
    html.Div([
        dcc.Graph(id='bar-chart')
    ])
])

@app.callback(
    Output('air-quality-graph', 'figure'),
    [Input('dropdown', 'value'),
     Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date')]
)
def update_line_graph(selected_pollutant, start_date, end_date):
    filtered_df = df[(df['DATETIMEDATA'] >= start_date) & (df['DATETIMEDATA'] <= end_date)]
    if selected_pollutant == 'all':
        fig = go.Figure()
        for pollutant in pollutants:
            fig.add_trace(go.Scatter(
                x=filtered_df['DATETIMEDATA'],
                y=filtered_df[pollutant],
                mode='lines',
                name=pollutant
            ))
        layout = go.Layout(
            title='Air Quality',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Concentration'),
            hovermode='closest',
            template="simple_white"
        )
        fig.update_layout(layout)
    else:
        trace = go.Scatter(
            x=filtered_df['DATETIMEDATA'],
            y=filtered_df[selected_pollutant],
            mode='lines',
            name=selected_pollutant
        )
        fig = go.Figure(data=[trace])
        layout = go.Layout(
            title='Air Quality',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Concentration'),
            hovermode='closest',
            template="simple_white"
        )
        fig.update_layout(layout)

    return fig

@app.callback(
    Output('example-scatter-plot', 'figure'),
    [Input('dropdown', 'value'),
     Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date')]
)
def update_scatter_plot(selected_pollutant, start_date, end_date):
    filtered_df = df[(df['DATETIMEDATA'] >= start_date) & (df['DATETIMEDATA'] <= end_date)]
    if selected_pollutant == 'all':
        fig = go.Figure()
        for pollutant in pollutants:
            fig.add_trace(go.Scatter(
                x=filtered_df['DATETIMEDATA'],
                y=filtered_df[pollutant],
                mode='markers',
                name=pollutant
            ))
        layout = go.Layout(
            title='Air Quality Scatter Plot',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Concentration'),
            hovermode='closest',
            template="simple_white"
        )
        fig.update_layout(layout)
    else:
        fig = px.scatter(filtered_df, x='DATETIMEDATA', y=selected_pollutant,
                         template="simple_white", title=f'{selected_pollutant} over Time')
    return fig

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('dropdown', 'value'),
     Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date')]
)
def update_pie_chart(selected_pollutant, start_date, end_date):
    filtered_df = df[(df['DATETIMEDATA'] >= start_date) & (df['DATETIMEDATA'] <= end_date)]
    if selected_pollutant == 'all':
        fig = go.Figure(data=[go.Pie(labels=pollutants, values=[filtered_df[pollutant].sum() for pollutant in pollutants], hole=0.4)])
        layout = go.Layout(
            title='Total Concentration by Pollutant',
            template="simple_white"
        )
        fig.update_layout(layout)
    else:
        fig = go.Figure(data=[go.Pie(labels=[selected_pollutant], values=[filtered_df[selected_pollutant].sum()], hole=0.4)])
        layout = go.Layout(
            title=f'Total Concentration of {selected_pollutant}',
            template="simple_white"
        )
        fig.update_layout(layout)
    return fig

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('dropdown', 'value'),
     Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date')]
)
def update_bar_chart(selected_pollutant, start_date, end_date):
    filtered_df = df[(df['DATETIMEDATA'] >= start_date) & (df['DATETIMEDATA'] <= end_date)]
    if selected_pollutant == 'all':
        fig = go.Figure(data=[go.Bar(x=pollutants, y=[filtered_df[pollutant].sum() for pollutant in pollutants])])
        layout = go.Layout(
            title='Total Concentration by Pollutant (Bar Chart)',
            xaxis=dict(title='Pollutant'),
            yaxis=dict(title='Total Concentration'),
            template="simple_white"
        )
        fig.update_layout(layout)
    else:
        fig = go.Figure(data=[go.Bar(x=[selected_pollutant], y=[filtered_df[selected_pollutant].sum()])])
        layout = go.Layout(
            title=f'Total Concentration of {selected_pollutant} (Bar Chart)',
            xaxis=dict(title='Pollutant'),
            yaxis=dict(title='Total Concentration'),
            template="simple_white"
        )
        fig.update_layout(layout)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
