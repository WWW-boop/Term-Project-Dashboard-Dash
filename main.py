import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY, 'static/style.css'])

# Load data
df = pd.read_csv('csv/pm25_new2.csv')
pdi = pd.read_csv('csv/predicted_pm25--5.csv')
pdw = pd.read_csv('csv/predicted_WD.csv')

# Define pollutants and columns
pollutants = ['PM25', 'O3', 'WS', 'TEMP', 'RH', 'WD']
columns = [{'label': col, 'value': col} for col in df.columns if col in pollutants]
columns.append({'label': 'All Pollutants', 'value': 'all'})

# Layout of the app
app.layout = html.Div([
    # Date pickers
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
    ], style={'display': 'flex', 'justify-content': 'center'}),

    # Dropdown for selecting pollutant and chart type
    html.Div([
        dcc.Loading(
            dcc.Dropdown(
                id='dropdown',
                options=columns,
                value='PM25',
                style={'backgroundColor': '#E7DDFF', 'borderRadius': '10px', 'text-align': 'center'}
            ),
            type="cube"
        ),
        html.Label('Select Your Favorite Chart Under', style={'text-align': 'center'}),
        dcc.Dropdown(
            id='chart-type-dropdown',
            options=[
                {'label': 'None', 'value': 'none'},
                {'label': 'Scatter Plot', 'value': 'scatterx'},
                {'label': 'Bar Chart', 'value': 'barx'},
                {'label': 'Pie Chart', 'value': 'piex'},
                {'label': 'data','value': 'tablex'}
            ],
            style={'backgroundColor': '#E7DDFF', 'borderRadius': '10px', 'text-align': 'center'}
        ),
        html.Div(id='selected-chart')
    ]),

    # Graphs
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
    #predict zone
    html.Div([
        dcc.Loading(
            dcc.DatePickerSingle(
                id='start-date-picker-v2',
                min_date_allowed=pd.to_datetime('2024-02-28'),
                max_date_allowed=pd.to_datetime('2024-03-28'),
                initial_visible_month=pd.to_datetime('2024-02-28'),
                date=pd.to_datetime('2024-02-28'),
                display_format='YYYY-MM-DD',
                className="btn btn-danger btn-outline-success"
            ),
            type="cube"
        ),
        dcc.Loading(
            dcc.DatePickerSingle(
                id='end-date-picker-v2',
                min_date_allowed=pd.to_datetime('2024-02-29'),
                max_date_allowed=pd.to_datetime('2024-04-28'),
                initial_visible_month=pd.to_datetime('2024-04-28'),
                date=pd.to_datetime('2024-04-28'),
                display_format='YYYY-MM-DD',
                className="btn btn-danger btn-outline-success"
            ),
            type="cube"
        ),

    ], style={'display': 'flex', 'justify-content': 'center'}),
    dcc.Graph(id='predict-PM25-graph'),
    html.Div(children='Predict PM25 with Data', style={'color': 'green', 'font-weight': 'bold', 'margin-bottom': '10px'}),  # Add a title or description
    dash_table.DataTable(
        id='datatable',
        data=pdi.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in pdi.columns],  # Assuming pdi is your DataFrame
        page_size=10,
        style_table={'overflowX': 'auto'},  # Enable horizontal scroll
        style_header={
            'backgroundColor': 'lightgreen',  # Background color for headers
            'fontWeight': 'bold'  # Bold text for headers
        },
        style_data={
            'whiteSpace': 'normal',  # Allow text wrapping
            'height': 'auto',  # Set row height to auto
            'backgroundColor': 'lightyellow'  # Background color for data cells
        },
        style_cell={
            'textAlign': 'center',  # Center-align text in cells
            'minWidth': '100px',  # Set minimum width of cells
            'width': '150px',  # Set default width of cells
            'maxWidth': '300px',  # Set maximum width of cells
            'overflow': 'hidden',  # Hide overflow content in cells
            'textOverflow': 'ellipsis',  # Ellipsis for overflow text
            'border': '1px solid green'  # Border around cells
        }
    ),
    #wd zone
    html.Div([
        dcc.Loading(
            dcc.DatePickerSingle(
                id='start-date-picker-v3',
                min_date_allowed=pd.to_datetime('2024-02-28'),
                max_date_allowed=pd.to_datetime('2024-03-28'),
                initial_visible_month=pd.to_datetime('2024-02-28'),
                date=pd.to_datetime('2024-02-28'),
                display_format='YYYY-MM-DD',
                className="btn btn-danger btn-outline-success"
            ),
            type="cube"
        ),
        dcc.Loading(
            dcc.DatePickerSingle(
                id='end-date-picker-v3',
                min_date_allowed=pd.to_datetime('2024-02-29'),
                max_date_allowed=pd.to_datetime('2024-04-28'),
                initial_visible_month=pd.to_datetime('2024-04-28'),
                date=pd.to_datetime('2024-04-28'),
                display_format='YYYY-MM-DD',
                className="btn btn-danger btn-outline-success"
            ),
            type="cube"
        ),
    ], style={'display': 'flex', 'justify-content': 'center'}),
    dcc.Graph(id='predict-WD-graph'),
    html.Div(children='Predict WD with Data', style={'color': 'green', 'font-weight': 'bold', 'margin-bottom': '10px'}),  # Add a title or description
    dash_table.DataTable(
        id='datatable',
        data=pdw.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in pdw.columns],  # Assuming pdi is your DataFrame
        page_size=10,
        style_table={'overflowX': 'auto'},  # Enable horizontal scroll
        style_header={
            'backgroundColor': 'lightgreen',  # Background color for headers
            'fontWeight': 'bold'  # Bold text for headers
        },
        style_data={
            'whiteSpace': 'normal',  # Allow text wrapping
            'height': 'auto',  # Set row height to auto
            'backgroundColor': 'lightyellow'  # Background color for data cells
        },
        style_cell={
            'textAlign': 'center',  # Center-align text in cells
            'minWidth': '100px',  # Set minimum width of cells
            'width': '150px',  # Set default width of cells
            'maxWidth': '300px',  # Set maximum width of cells
            'overflow': 'hidden',  # Hide overflow content in cells
            'textOverflow': 'ellipsis',  # Ellipsis for overflow text
            'border': '1px solid green'  # Border around cells
        }
    )

])




# Callbacks
@app.callback(
    Output('selected-chart', 'children'),
    [Input('chart-type-dropdown', 'value')]
)
def update_selected_chart(chart_type):
    if chart_type == 'none':
        return html.Div()
    elif chart_type in ['scatterx', 'barx', 'piex']:
        if chart_type == 'piex':
            graph_or_table = dcc.Graph(
                id='pie-chart'
            )
        else:
            graph_or_table = dcc.Graph(
                id='example-scatter-plot' if chart_type == 'scatterx' else
                    'bar-chart' if chart_type == 'barx' else 'pie-chart'
            )

        return dcc.Loading(
            html.Div(graph_or_table),
            type="cube"
        )
    elif chart_type == 'tablex':
        return dcc.Loading(
            dash_table.DataTable(
                id='datatable',
                data=df.to_dict('records'),
                columns=[{'name': col, 'id': col} for col in df.columns],  # Assuming pdi is your DataFrame
                page_size=10,
                style_table={'overflowX': 'auto'},  # Enable horizontal scroll
                style_header={
                    'backgroundColor': 'lightgreen',  # Background color for headers
                    'fontWeight': 'bold'  # Bold text for headers
                },
                style_data={
                    'whiteSpace': 'normal',  # Allow text wrapping
                    'height': 'auto',  # Set row height to auto
                    'backgroundColor': 'lightyellow'  # Background color for data cells
                },
                style_cell={
                    'textAlign': 'center',  # Center-align text in cells
                    'minWidth': '100px',  # Set minimum width of cells
                    'width': '150px',  # Set default width of cells
                    'maxWidth': '300px',  # Set maximum width of cells
                    'overflow': 'hidden',  # Hide overflow content in cells
                    'textOverflow': 'ellipsis',  # Ellipsis for overflow text
                    'border': '1px solid green'  # Border around cells
                }
            ),
            type="cube"
        )
    else:
        return html.Div(children='all')



def update_figure(filtered_df, plot_type, selected_pollutant):
    if selected_pollutant == 'all':
        if plot_type == 'scatter':
            fig = go.Figure()
            for pollutant in pollutants:
                fig.add_trace(go.Scatter(
                    x=filtered_df['DATETIMEDATA'],
                    y=filtered_df[pollutant],
                    mode='markers',
                    name=pollutant
                ))
        elif plot_type == 'bar':
            fig = go.Figure(data=[go.Bar(x=pollutants,
                                        y=[filtered_df[pollutant].sum() for pollutant in pollutants])])
        else:  # Pie chart
            fig = go.Figure(data=[go.Pie(labels=pollutants,
                                        values=[filtered_df[pollutant].sum() for pollutant in pollutants],
                                        hole=0.4)])
    else:
        if plot_type == 'scatter':
            fig = px.scatter(filtered_df, x='DATETIMEDATA', y=selected_pollutant,
                            template="simple_white", title=f'{selected_pollutant} over Time')
        elif plot_type == 'bar':
            fig = go.Figure(data=[go.Bar(x=[selected_pollutant], y=[filtered_df[selected_pollutant].sum()])])
        else:  # Pie chart
            fig = go.Figure(data=[go.Pie(labels=[selected_pollutant],
                                        values=[filtered_df[selected_pollutant].sum()], hole=0.4)])
    fig.update_layout(plot_bgcolor='#E4F9F5', paper_bgcolor='#E4F9F5')  # Background color
    return fig


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
    return update_figure(filtered_df, 'scatter', selected_pollutant)


@app.callback(
    Output('bar-chart', 'figure'),
    [Input('dropdown', 'value'),
    Input('start-date-picker', 'date'),
    Input('end-date-picker', 'date')]
)
def update_bar_chart(selected_pollutant, start_date, end_date):
    filtered_df = df[(df['DATETIMEDATA'] >= start_date) & (df['DATETIMEDATA'] <= end_date)]
    return update_figure(filtered_df, 'bar', selected_pollutant)


@app.callback(
    Output('pie-chart', 'figure'),
    [Input('dropdown', 'value'),
    Input('start-date-picker', 'date'),
    Input('end-date-picker', 'date')]
)
def update_pie_chart(selected_pollutant, start_date, end_date):
    filtered_df = df[(df['DATETIMEDATA'] >= start_date) & (df['DATETIMEDATA'] <= end_date)]

    return update_figure(filtered_df, 'pie', selected_pollutant)

#predict zone
@app.callback(
    Output('predict-PM25-graph', 'figure'),
    [Input('start-date-picker-v2', 'date'),
    Input('end-date-picker-v2', 'date')]
)
def update_predict_PM25(start_date, end_date):
    filtered_pdi = pdi[(pdi['DATETIMEDATA'] >= start_date) & (pdi['DATETIMEDATA'] <= end_date)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_pdi['DATETIMEDATA'], y=filtered_pdi['prediction_label'], mode='lines+markers'))
    fig.update_layout(
        title='Prediction PM25',
        xaxis_title='Date',
        yaxis_title='Prediction',
        template="plotly_white",
        plot_bgcolor='#E4F9F5',  # สีพื้นหลังกราฟ
        paper_bgcolor='#E4F9F5',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=2, label="2d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=14, label="2w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=2, label="2m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        ),

        xaxis_range=[start_date, end_date]
    )
    return fig
    #wd zone
@app.callback(
    Output('predict-WD-graph', 'figure'),
    [Input('start-date-picker-v3', 'date'),
    Input('end-date-picker-v3', 'date')]
)
def update_predict_wd(start_date, end_date):
    filtered_pdw = pdw[(pdw['DATETIMEDATA'] >= start_date) & (pdw['DATETIMEDATA'] <= end_date)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_pdw['DATETIMEDATA'], y=filtered_pdw['prediction_label'], mode='lines+markers'))
    fig.update_layout(
        title='Prediction WD',
        xaxis_title='Date',
        yaxis_title='Prediction',
        template="plotly_white",
        plot_bgcolor='#E4F9F5',  # สีพื้นหลังกราฟ
        paper_bgcolor='#E4F9F5',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=2, label="2d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=14, label="2w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=2, label="2m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        ),

        xaxis_range=[start_date, end_date]
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
