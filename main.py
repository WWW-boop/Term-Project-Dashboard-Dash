import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

df = pd.read_csv('csv/pm25_new.csv')
pd_pm25 = pd.read_csv('csv/predicted_pm25--5.csv')

pollutants = ['PM25','O3', 'WS','TEMP', 'RH', 'WD']
columns = [{'label': col, 'value': col} for col in df.columns if col in pollutants]
columns.append({'label': 'All Pollutants', 'value': 'all'})

app.layout = html.Div([
    html.Div([
        dcc.Loading(
            dcc.DatePickerSingle(
                id='start-date-picker',
                min_date_allowed=pd.to_datetime('2023-12-01'),
                max_date_allowed=pd.to_datetime('2024-02-27'),
                initial_visible_month=pd.to_datetime('2023-12-01'),
                date=pd.to_datetime('2024-01-01'),
                display_format='YYYY-MM-DD',
                className="btn btn-success btn-outline-danger"
            ),
            type="cube"
        ),
        dcc.Loading(
            dcc.DatePickerSingle(
                id='end-date-picker',
                min_date_allowed=pd.to_datetime('2023-12-01'),
                max_date_allowed=pd.to_datetime('2024-02-27'),
                initial_visible_month=pd.to_datetime('2024-02-27'),
                date=pd.to_datetime('2024-03-01'),
                display_format='YYYY-MM-DD',
                className="btn btn-success btn-outline-danger"
            ),
            type="cube"
        ),
    ], style={'display': 'flex'}),
    html.Div([
        dcc.Loading(
            dcc.Dropdown(
                id='dropdown',
                options=columns,
                value='PM25',
                style={'backgroundColor': '#E7DDFF'}
            ),
            type="cube"
        ),
    ]),

    # เพิ่มโค้ดที่ต้องการรวมตรงนี้
    html.Div([
        html.Label('Select Your Favorite Chart Under:'),
        dcc.Dropdown(
            id='chart-type-dropdown',
            options=[
                {'label': 'None', 'value': 'none'},
                {'label': 'Scatter Plot', 'value': 'scatter'},
                {'label': 'Bar Chart', 'value': 'bar'},
                {'label': 'Pie Chart', 'value': 'pie'}
            ],
            style={'backgroundColor': '#E7DDFF', 'margin-top': '10px', 'margin-bottom': '10px'}
        ),
        html.Div(id='selected-chart')
    ]),

    html.Div([
        html.Div([
            dcc.Loading(
            dcc.Graph(id='air-quality-graph'),
            type="cube"
        )
        ], className="six columns"),
        html.Div([
            dcc.Loading(
            dcc.Graph(id='example-scatter-plot'),
            type="cube"
        )
        ], className="six columns"),
        html.Div([
            dcc.Loading(
                dcc.Graph(id='pie-chart'),
                type="cube"
            )
        ], className="six columns")
    ], className="row"),
    html.Div([
        dcc.Loading(
            dcc.Graph(id='bar-chart'),
            type="cube"
        )
    ]),

])


@app.callback(
    Output('selected-chart', 'children'),
    [Input('chart-type-dropdown', 'value')]
)
def update_selected_chart(chart_type):
    if chart_type == 'none':
        pass
    elif chart_type == 'scatter':
        return dcc.Loading(
                    dcc.Graph(id='example-scatter-plot'),
                    type="cube"
                )
    elif chart_type == 'bar':
        return dcc.Loading(
            dcc.Graph(id='bar-chart'),
            type="cube"
        )
    elif chart_type == 'pie':
        return dcc.Loading(
                dcc.Graph(id='pie-chart'),
                type="cube"
            )

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
                name=pollutant,

            ))
        layout = go.Layout(
            title='Air Quality',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Concentration'),
            hovermode='closest',
            template="simple_white",
            plot_bgcolor='#E4F9F5',  # สีพื้นหลังกราฟ
            paper_bgcolor='#E4F9F5',
        )
        fig.update_layout(layout)
    else:
        trace = go.Scatter(
            x=filtered_df['DATETIMEDATA'],
            y=filtered_df[selected_pollutant],
            mode='lines',
            name=selected_pollutant,
            line=dict(color='#30E3CA')
        )
        fig = go.Figure(data=[trace])
        layout = go.Layout(
            title='Air Quality',
            xaxis=dict(title='Date', showgrid=False),
            yaxis=dict(title='Concentration', showgrid=False),
            hovermode='closest',
            plot_bgcolor='#E4F9F5',  # สีพื้นหลังกราฟ
            paper_bgcolor='#E4F9F5',
        )
        fig.update_layout(layout)

    return fig

@app.callback(
    Output('example-scatter-plot', 'figure'),
    [Input('dropdown', 'value'),
    Input('start-date-picker', 'date'),
    Input('end-date-picker', 'date')]
)
def update_example_scatter_plot(selected_pollutant, start_date, end_date):
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
            template="simple_white",
            plot_bgcolor='#E4F9F5',  # สีพื้นหลังกราฟ
            paper_bgcolor='#E4F9F5',  # สีพื้นกระดาน
        )
        fig.update_layout(layout)
    else:
        fig = px.scatter(filtered_df, x='DATETIMEDATA', y=selected_pollutant,
                        template="simple_white", title=f'{selected_pollutant} over Time')
        fig.update_layout(plot_bgcolor='#E4F9F5', paper_bgcolor='#E4F9F5')  # สีพื้นหลังกราฟและพื้นกระดาน
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
            template="simple_white",
            plot_bgcolor='#E4F9F5',  # สีพื้นหลังกราฟ
            paper_bgcolor='#E4F9F5',
        )
        fig.update_layout(layout)
    else:
        fig = go.Figure(data=[go.Pie(labels=[selected_pollutant], values=[filtered_df[selected_pollutant].sum()], hole=0.4)])
        layout = go.Layout(
            title=f'Total Concentration of {selected_pollutant}',
            template="simple_white",
            plot_bgcolor='#E4F9F5',  # สีพื้นหลังกราฟ
            paper_bgcolor='#E4F9F5',
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
            template="simple_white",
            plot_bgcolor='#E4F9F5',  # สีพื้นหลังกราฟ
            paper_bgcolor='#E4F9F5',
        )
        fig.update_layout(layout)
    else:
        fig = go.Figure(data=[go.Bar(x=[selected_pollutant], y=[filtered_df[selected_pollutant].sum()])])
        layout = go.Layout(
            title=f'Total Concentration of {selected_pollutant} (Bar Chart)',
            xaxis=dict(title='Pollutant'),
            yaxis=dict(title='Total Concentration'),
            template="simple_white",
            plot_bgcolor='#E4F9F5',  # สีพื้นหลังกราฟ
            paper_bgcolor='#E4F9F5',
        )
        fig.update_layout(layout)
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)