from flask import Flask, render_template
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')


df = pd.read_csv('csv\pm25.csv')


data_table = dash_table.DataTable(
    id='datatable-interactivity',
    columns=[
        {"name": i, "id": i} for i in df.columns
    ],
    data=df.to_dict('records'),
    editable=True,
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    column_selectable="single",
    row_selectable="multi",
    row_deletable=True,
    selected_columns=[],
    selected_rows=[],
    page_action="native",
    page_current=0,
    page_size=13,
)


app.layout = html.Div([
    html.H1('Dashboard'),
    data_table
])

@server.route('/')
def index():
    return render_template('index.html')

@server.route('/dashboard')
def dashboard():
    return app.index()

if __name__ == '__main__':
    server.run(debug=True)
