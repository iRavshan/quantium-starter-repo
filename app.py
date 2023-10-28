from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

df = pd.read_csv("./output/output.csv")
df = df.sort_values(by="date")

app = Dash(__name__)

fig = px.line(df, x="date", y="sales", title="Pink Morsel Sales")

app.layout = html.Div(children=[
    html.H1(children='''
        Analysing the increase in the Pink Morsel price
    '''),

    dcc.Graph(
        id='visualization',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)