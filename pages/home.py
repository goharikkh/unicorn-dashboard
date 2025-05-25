# pages/home.py
from dash import register_page, html
from data_loader import load_data

register_page(
    __name__,
    path="/",
    name="🏠 Home",
    title="Unicorn Dashboard - Home"
)

df = load_data()
total_unicorns = len(df)

layout = html.Div([
    html.H1("Welcome to the Unicorn Dashboard"),

    html.H3("🦄 What is a Unicorn Company?"),
    html.P("""
        A unicorn company is a privately held startup valued at over $1 billion.
        The term was coined to emphasize how rare these ventures used to be — 
        like spotting a unicorn in the wild. Today, hundreds of such companies 
        exist globally, particularly in the technology, fintech, and e-commerce sectors.
    """),

    html.H3("📊 About This Dashboard"),
    html.P(f"""
        This dashboard includes a total of {total_unicorns} unicorn companies sourced from a 
        public dataset. You can explore trends by country, city, industry, and company valuation.
    """),

    html.H3("🇦🇲 Note on Armenian Unicorns"),
    html.P("""
        The original dataset did not include Armenia's two well-known unicorns: 
        Picsart and ServiceTitan. These companies were manually added to ensure 
        representation. While Picsart remains private, ServiceTitan has already gone public.
    """),

    html.H3("🔍 Use this dashboard to:"),
    html.Ul([
        html.Li("Explore the distribution of unicorns by geography and industry"),
        html.Li("Understand average company valuations and growth trends"),
        html.Li("Gain insights into the global startup landscape"),
    ])
])
