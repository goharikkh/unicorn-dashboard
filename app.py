# app.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    pages_folder="pages",  # this is your page directory
    external_stylesheets=[dbc.themes.FLATLY]
)
server = app.server

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dcc.Link(page["name"], href=page["path"], className="nav-link")
            for page in dash.page_registry.values()
        ],
        brand="🦄 Unicorn Dashboard",
        color="primary",
        dark=True,
    ),
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True)