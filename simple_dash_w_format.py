# ========== (c) JP Hwang 2020-02-28  ==========

import logging

# ===== START LOGGER =====
logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

desired_width = 320
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', desired_width)

all_teams_df = pd.read_csv('shot_dist_compiled_data_2019_20.csv')


def clean_chart_format(fig):
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        annotations=[
            go.layout.Annotation(
                x=0.9,
                y=1.02,
                showarrow=False,
                text="Twitter: @_jphwang",
                xref="paper",
                yref="paper",
                textangle=0
            ),
        ],
        font=dict(
            family="Arial, Tahoma, Helvetica",
            size=10,
            color="#404040"
        ),
        margin=dict(
            t=20
        )
    )
    fig.update_traces(marker=dict(line=dict(width=1, color='Navy')),
                      selector=dict(mode='markers'))
    fig.update_coloraxes(
        colorbar=dict(
            thicknessmode="pixels", thickness=15,
            outlinewidth=1,
            outlinecolor='#909090',
            lenmode="pixels", len=300,
            yanchor="top",
            y=1,
        ))
    fig.update_yaxes(showgrid=True, gridwidth=1, tickson='boundaries', gridcolor='LightGray', fixedrange=True)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray', fixedrange=True)
    return True


def make_shot_dist_chart(input_df, color_continuous_scale=None, size_col='shots_count', col_col='pl_acc', range_color=None):
    max_bubble_size = 15
    if color_continuous_scale is None:
        color_continuous_scale = px.colors.diverging.RdYlBu_r
    if range_color is None:
        range_color = [min(input_df[col_col]), max(input_df[col_col])]

    fig = px.scatter(
        input_df, x='min_mid', y='player', size=size_col,
        color=col_col,
        color_continuous_scale=color_continuous_scale,
        range_color=range_color,
        range_x=[0, 49],
        range_y=[-1, len(input_df.player.unique())],
        hover_name='player', hover_data=['min_start', 'min_end', 'shots_count', 'shots_made', 'shots_freq', 'shots_acc', ],
        render_mode='svg'
    )
    fig.update_coloraxes(colorbar=dict(title='Points per<BR>100 shots'))
    fig.update_traces(marker=dict(sizeref=2. * 30 / (max_bubble_size ** 2)))
    fig.update_yaxes(title="Player")
    fig.update_xaxes(title='Minute', tickvals=list(range(0, 54, 6)))

    return fig


app = dash.Dash(__name__)

server = app.server

app.title = 'Dash Demo - NBA'
team_names = all_teams_df.group.unique()
team_names.sort()
app.layout = html.Div([
    html.Div([
        dcc.Markdown(
            """
            #### Shot Frequencies & Efficiencies (2019-20 NBA Season)

            This page compares players based on shot *frequency* and *efficiency*, 
            divided up into minutes of regulation time for each team.

            Use the pulldown to select a team, or select 'Leaders' to see leaders from each team.


            *Notes*:

            * **Frequency**: A team's shots a player is taking, indicated by **size**.

            * **Efficiency**: Points scored per 100 shots, indicated by **colour** (red == better, blue == worse).

            * Players with <1% of team shots are shown under 'Others'
            """
        ),
        html.P([html.Small("See more data / NBA analytics content, find me on "), html.A(html.Small("twitter"), href="https://twitter.com/_jphwang", title="twitter"), html.Small("!")]),
    ]),
    html.Div([
        dcc.Dropdown(
            id='group-select',
            options=[{'label': i, 'value': i} for i in team_names],
            value='TOR',
            style={'width': '140px'}
        )
    ]),
    dcc.Graph(
        'shot-dist-graph',
        config={'displayModeBar': False}
    )
])


@app.callback(
    Output('shot-dist-graph', 'figure'),
    [Input('group-select', 'value')]
)
def update_graph(grpname):
    fig = make_shot_dist_chart(
        all_teams_df[all_teams_df.group == grpname], col_col='pl_pps', range_color=[90, 120], size_col='shots_freq')
    clean_chart_format(fig)
    if len(grpname) > 3:
        fig.update_layout(height=850, width=1250)
    else:
        fig.update_layout(height=500, width=1250)

    return fig


# ===== END - PLOT GRAPH =====

if __name__ == '__main__':
    app.run_server(debug=False)
