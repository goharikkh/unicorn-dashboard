from dash import register_page, html
from data_loader import load_data

register_page(
    __name__,
    path="/insights",
    name="📈 Insights",
    title="Unicorn Dashboard - Insights"
)

df = load_data()
top_country = df["Country"].value_counts().idxmax()
avg_valuation = round(df["Valuation ($B)"].mean(), 2)

layout = html.Div(
    style={"display": "flex", "justifyContent": "center", "padding": "40px"},
    children=[
        html.Div(
            style={"maxWidth": "700px", "width": "100%", "textAlign": "center"},
            children=[
                html.H2("📈 Key Insights"),

                html.P(f"🌍 The United States leads in unicorn count, with {top_country} topping the list."),
                html.P(f"💰 The average unicorn is valued at ${avg_valuation} billion."),
                html.P("🚀 Most unicorns were founded after 2015, showing a surge in startup creation."),
                html.P("🏦 Fintech, E-commerce, and AI are the top industries driving unicorn growth."),
                html.P("🌎 Cities like San Francisco, Beijing, and New York dominate the unicorn landscape."),
            ]
        )
    ]
)
