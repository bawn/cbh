import plotly.express as px
from dash import Dash, dcc, html
from cbh import db

def create_dashboard():
    cursor = db.get_connection().cursor()

    metrics = db.fetch_metrics(cursor)
    
    figures = []

    for metric in metrics:
        data_list = db.fetch_metric_data(cursor, metric)
        years = [row[0] for row in data_list]
        values = [row[1] for row in data_list]

        fig = px.bar(x=years, y=values, title=metric)
        fig.update_layout(bargap=0.4)
        fig.update_xaxes(
            tickmode='array',
            tickvals=years
        )
        figures.append(fig)

    app = Dash(__name__)

    app.layout = html.Div([
        html.H1("Dashboard"),
        *[dcc.Graph(figure=fig) for fig in figures]
    ])
    app.run(debug=True)  
