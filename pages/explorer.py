# pages/explorer.py
from dash import register_page, html, dcc, Input, Output
from dash import dash_table
import pandas as pd
import dash
from data_loader import load_data

register_page(
    __name__,
    path="/explorer",
    name="🔍 Data Explorer",
    title="Unicorn Dashboard - Data Explorer"
)

# Load and prep data
df = load_data()
df["Year"] = df["Date Joined"].dt.year
available_countries = sorted(df["Country"].dropna().unique())
app = dash.get_app()

layout = html.Div(
    style={"display": "flex", "justifyContent": "center", "padding": "40px"},
    children=[
        html.Div(
            style={"maxWidth": "1200px", "width": "100%"},
            children=[
                html.H2("Explore Unicorn Companies", style={"textAlign": "center", "marginBottom": "30px"}),

                html.Div([
                    html.Label("Select Country:"),
                    dcc.Dropdown(
                        id="country-selector",
                        options=[{"label": c, "value": c} for c in available_countries],
                        placeholder="Select a country (optional)..."
                    ),
                ]),

                html.Br(),

                html.Div([
                    html.Label("Select City:"),
                    dcc.Dropdown(
                        id="city-selector",
                        placeholder="Select a city (optional)..."
                    )
                ]),

                html.Br(),

                html.Div([
                    html.Label("Select Year Range:"),
                    dcc.RangeSlider(
                        id="year-slider",
                        min=df["Year"].min(),
                        max=df["Year"].max(),
                        value=[df["Year"].min(), df["Year"].max()],
                        marks={int(year): str(year) for year in sorted(df["Year"].dropna().unique())},
                        tooltip={"placement": "bottom", "always_visible": False}
                    )
                ]),

                html.Br(),

                dash_table.DataTable(
                    id="unicorn-table",
                    columns=[{"name": col, "id": col} for col in [
                        "Company", "Valuation ($B)", "Industry", "City", "Country", "Date Joined", "Select Investors"]],
                    data=df.to_dict("records"),
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left"},
                    page_size=15
                )
            ]
        )
    ]
)


# --- Callbacks ---

@app.callback(
    Output("city-selector", "options"),
    Input("country-selector", "value")
)
def update_city_dropdown(selected_country):
    if selected_country:
        filtered_df = df[df["Country"] == selected_country]
        cities = sorted(filtered_df["City"].dropna().unique())
    else:
        cities = sorted(df["City"].dropna().unique())

    return [{"label": c, "value": c} for c in cities]

@app.callback(
    Output("unicorn-table", "data"),
    Input("country-selector", "value"),
    Input("city-selector", "value"),
    Input("year-slider", "value")
)
def update_table(country, city, year_range):
    filtered = df.copy()

    if country:
        filtered = filtered[filtered["Country"] == country]
    if city:
        filtered = filtered[filtered["City"] == city]
    if year_range:
        filtered = filtered[
            (filtered["Year"] >= year_range[0]) &
            (filtered["Year"] <= year_range[1])
        ]

    return filtered.to_dict("records")
