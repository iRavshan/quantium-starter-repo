from dash import Dash, html, dcc, Input, Output, callback, clientside_callback
import plotly.express as px
import pandas as pd

df = pd.read_csv("./output/output.csv")
df = df.sort_values(by="date")


external_stylesheets = [
    "https://github.com/iRavshan/quantium-starter-repo/blob/main/assets/typography.css",
    "https://github.com/iRavshan/quantium-starter-repo/blob/main/assets/app.css"
]


app = Dash(
    __name__,
    external_stylesheets=external_stylesheets
)

title = html.H4(
    "Pink Morsel Visualizer",
    id="title",
    className="app-header-title"
)

subtitle = html.P(
    "Analysing the product sales before and after the product price increase on 15th of January 2021",
    id="subtitle",
    className="app-header-subtitle"
)

header = html.Div(
    className="app-header",
    id="header",
    children=[
        html.Div(
            className="app-header-desc",
            children = [
                title,
                subtitle
            ]),

        html.Div(
            className="app-header-logo",
            children=[
                html.Img(
                    src="/assets/me.jpg",
                    className="app-menu-img"
                )
            ])
    ]
)

def generate_figure(chart_data):
    line_chart = px.line(chart_data, x="date", y="sales")
    return line_chart

visualization = dcc.Graph(
    figure=generate_figure(df),
    id="visualization"
)

def generate_sum_figure(chart_data):
    bar_chart = {
        'data': [
            {'x': [1], 'y': [chart_data[(chart_data["date"]<="2021-01-14") & (chart_data["date"]>="2020-01-15")].sum()[2]], 'type': 'bar', 'name': 'before'},
            {'x': [2], 'y': [chart_data[chart_data["date"]>="2021-01-15"].sum()[2]], 'type': 'bar', 'name': 'after'} 
        ]
    }
    return bar_chart

sum_line_chart = dcc.Graph(
    figure=generate_sum_figure(df)
)

region_picker1 = dcc.RadioItems(
            ["north", "east", "south", "west", "all"],
            "all",
            id="region_picker",
            inline=True,
            className="radio-items")

region_picker2 = dcc.RadioItems(
            ["north", "east", "south", "west", "all"],
            "all",
            id="region_picker2",
            inline=True,
            className="radio-items-on-chart")

column1 = html.Div(
    className="two-thirds column sales-container",
    children=[
        html.Div(
            [
                html.H6(
                    className = "chart-title",
                    children="Pink Morsel Sales (USD)"
                )
            ]
        ),
        region_picker1,
        visualization
    ] 
)

column2 = html.Div(
    className="one-third column sum-chart",
    children=[
        html.Div(
            className="graph-container first",
            children =
            [
                html.Div(
                    html.H6(
                        className = "chart-title",
                        children="Total sales for 365 days"
                    )
                ),
                region_picker2,
                sum_line_chart
            ]
        )
    ]
)

content = html.Div(
    className="app-content",
    children=[
        column1,
        column2
    ]
)

app.layout = html.Div(
    className = "app-container",
    children = [
        header,
        content
    ]
)

@callback(
    Output(visualization, "figure"),
    Input(region_picker1, "value")
)
def update_graph(region):
    if region == "all":
        trimmed_data = df
    else:
        trimmed_data = df[df["region"] == region]
    figure = generate_figure(trimmed_data)
    return figure


@callback(
    Output(sum_line_chart, "figure"),
    Input(region_picker2, "value")
)
def update_bar_graph(region):
    if region == "all":
        trimmed_data = df
    else:
        trimmed_data = df[df["region"] == region]
    figure = generate_sum_figure(trimmed_data)
    return figure


if __name__ == '__main__':
    app.run(debug=True)