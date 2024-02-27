from dash import Dash, html, dash_table
import pandas as pd


df = pd.read_csv('air4thai_44t_2024-02-19_2024-02-20.csv')


app = Dash(__name__)


app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])


if __name__ == '__main__':
    app.run(debug=True)
