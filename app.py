import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


tips=px.data.tips()

px.defaults.template = "plotly_dark"


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph', config={
        'scrollZoom': True
    }),

    html.H3("What should determine graph color?"),
    dcc.Dropdown(id='plot_against',
        options=[{'label': x, 'value': x} for x in tips.columns]),

    html.H3("Choose a marginal graph"),
    dcc.Dropdown(id='dropdown', options=[
        {'label': 'boxplot', 'value': 'box'},
        {'label': 'violin chart', 'value' : 'violin'}]),

    html.H3("Do you want a violin plot on the right?"),  
    dcc.Checklist(id='want_violin', options=[
        {'label': 'violin', 'value': 'box'}]),
])


@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value'),
    Input('want_violin', 'value'),
    Input('plot_against', 'value')])
def update_figure(dropdown_selection, the_violin, plot_against):
    the_violin = 'violin' if the_violin else None
    fig = px.scatter(tips, x='total_bill', y='tip',
                 marginal_x=dropdown_selection,
                 marginal_y=the_violin,
                 color=plot_against,
                 size='tip',
                 trendline='ols')
    

    fig.update_layout(dragmode='pan')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)