# pages/insights.py
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

layout = html.Div([
    html.H2("Key Insights"),

    html.P(f"🌍 The country with the most unicorns is **{top_country}**."),
    html.P(f"💰 The average unicorn valuation is **${avg_valuation} billion**."),
    html.P("📈 Most unicorns were founded after 2015, indicating rapid startup growth."),
    html.P("💡 Dominant industries include fintech, e-commerce, and AI."),
])
