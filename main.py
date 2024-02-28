from flask import Flask ,render_template
import dash
import dash_core_components as dcc
import dash_html_components as html

server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

@app.server.route('/')
def index():
    return render_template('index.html')

@app.server.route('/dashboard')
def dashboard():
    return app.index()

app.layout = html.Div([
    html.H1('Dash Example'),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])




if __name__ == '__main__':
    server.run(debug=True)
