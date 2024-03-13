import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)

pdi = pd.read_csv('csv/predicted_pm25--5.csv')

app.layout = html.Div([
    html.Div([
        dcc.Loading(
            dcc.DatePickerSingle(
                id='start-date-picker',
                min_date_allowed=pd.to_datetime('2024-02-28'),
                max_date_allowed=pd.to_datetime('2024-03-28'),
                initial_visible_month=pd.to_datetime('2024-02-28'),
                date=pd.to_datetime('2024-02-28'),
                display_format='YYYY-MM-DD',
                className="btn btn-success btn-outline-danger"
            ),
            type="cube"
        ),
        dcc.Loading(
            dcc.DatePickerSingle(
                id='end-date-picker',
                min_date_allowed=pd.to_datetime('2024-02-29'),
                max_date_allowed=pd.to_datetime('2024-03-28'),
                initial_visible_month=pd.to_datetime('2024-03-28'),
                date=pd.to_datetime('2024-03-28'),
                display_format='YYYY-MM-DD',
                className="btn btn-success btn-outline-danger"
            ),
            type="cube"
        ),
    ]),
    dcc.Graph(id='example-graph')
])

@app.callback(
    Output('example-graph', 'figure'),
    [Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date')]
)
def update_graph(start_date, end_date):
    filtered_pdi = pdi[(pdi['DATETIMEDATA'] >= start_date) & (pdi['DATETIMEDATA'] <= end_date)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_pdi['DATETIMEDATA'], y=filtered_pdi['prediction_label'], mode='lines+markers'))
    fig.update_layout(
        title='Prediction over Time',
        xaxis_title='Date',
        yaxis_title='Prediction',
        template="plotly_white",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
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
