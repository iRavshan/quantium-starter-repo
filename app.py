from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

df = pd.read_csv("./output/output.csv")
df = df.sort_values(by="date")


external_stylesheets = [
    "https://github.com/iRavshan/quantium-starter-repo/blob/main/assets/typography.css"
]


app = Dash(
    __name__,
    external_stylesheets=external_stylesheets
)

fig = px.line(df, x="date", y="sales", title="Pink Morsel Sales")
visualization = dcc.Graph(
    figure=fig,
    id="visualization"
)

header = html.H4(
    "Pink Morsel Visualizer",
    id="header"
)

subtitle = html.H6(
    "This app continually queries a SQL database and displays live charts of wind speed and wind direction.",
    id="subtitle"
)

region_picker = dcc.RadioItems(
    ["north", "east", "south", "west", "all"],
    "north",
    id="region_picker",
    inline=True
)

region_picker_wrapper = html.Div(
    [
        region_picker
    ]
)


app.layout = html.Div(
    [
        header,
        subtitle,
        region_picker_wrapper,
        visualization
    ]
)

if __name__ == '__main__':
    app.run(debug=True)