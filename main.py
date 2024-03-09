from dash import Dash, dcc, html, Input, Output, State, ALL, no_update, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

todo_list = [
    {
        "title": " Take the dog for a walk",
        "state": "To do"
    }
]

state_list = [
    {
        "name": "To do",
        "color": "#00bcff"
    },
    {
        "name": "In process",
        "color": "#00ffd2"
    },
    {
        "name": "Done",
        "color": "#00ff83"
    }
]

app = Dash(__name__)


def generate_cards() -> list:
    return [
        dbc.Container(
            [
                html.Div([*[
                    html.Button(
                        state_data["name"],
                        disabled=to_do_item["state"] == state_data["name"],
                        style={"border": "0.5px solid " + state_data["color"], "borderRadius": 3,
                               "color": "#555",
                               "cursor": "auto" if to_do_item["state"] == state_data["name"] else "pointer",
                               "background": "#DDD" if to_do_item["state"] == state_data["name"] else "white"},
                        id={"type": state_data["name"], "index": idx}
                    ) for state_data in state_list
                ],
                          html.Button(
                              "✕",
                              style={"border": "none", "color": "red", "fontSize": "1.2rem", "fontWeight": "bold",
                                     "cursor": "pointer", "background": "white"},
                              id={"type": "delete", "index": idx}
                          )
                          ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}),
                html.Span(to_do_item["title"], style={"overflowY": "auto", "height": 80, "display": "block"})
            ], style={"height": 120, "border": "1px #BBB solid", "minWidth": "200px", "width": "calc(16% - 22px)",
                      "marginBottom": "10px", "borderRadius": 5, "boxShadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                      "padding": "5px 10px"}
        ) for idx, to_do_item in enumerate(todo_list)
    ]


app.layout = dbc.Container([
    html.Div([
        html.Span("My to do list", style={"fontSize": "2rem"}),
        html.Div([
            dcc.Input(id="new_to_do", placeholder="Water the plants"),
            html.Button("+", id="add_btn", style={"background": "black", "color": "white", "cursor": "pointer",
                                                  "borderRadius": "100%", "marginLeft": 5, "width": 30, "height": 30})
        ])
    ], style={"display": "flex", "justify-content": "space-between"}),
    html.Br(),
    dcc.Graph(id="graph"),
    html.Br(),
    html.Div(generate_cards(), id="cards_grid",
             style={"display": "flex", "alignItems": "center",
                    "gap": "5%", "flexFlow": "row wrap"})
], style={"margin": "auto", "width": "70%"})


@app.callback(
    Output("graph", "figure"),
    Input("cards_grid", "children")
)
def update_fig(_):
    data = pd.DataFrame(todo_list)
    fig = px.histogram(data, x="state", color="state",
                       color_discrete_map={state["name"]: state["color"] for state in state_list})
    return fig


@app.callback(
    Output("cards_grid", "children"),
    Output("new_to_do", "value"),
    Input("add_btn", "n_clicks"),
    State("new_to_do", "value"),
)
def create_new_to_do_item(_, value):
    if value:
        todo_list.append({
            "title": value,
            "state": "To do"
        })

    return generate_cards(), ""


@app.callback(
    Output("cards_grid", "children", allow_duplicate=True),
    Input({"type": "delete", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def delete_item(values: list):
    try:
        deleted_idx = values.index(1)
        del todo_list[deleted_idx]
        return generate_cards()
    except ValueError:
        return no_update


@app.callback(
    Output("cards_grid", "children", allow_duplicate=True),
    [Input({"type": i["name"], "index": ALL}, "n_clicks") for i in state_list],
    prevent_initial_call=True
)
def change_state(_, __, ___):
    print(ctx.triggered_id)
    idx = ctx.triggered_id["index"]
    status = ctx.triggered_id["type"]

    todo_list[idx]["state"] = status

    return generate_cards()


if __name__ == "__main__":
    app.run_server(debug=True)
