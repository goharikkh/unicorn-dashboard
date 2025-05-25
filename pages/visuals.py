from dash import register_page, html, dcc
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder
from data_loader import load_data
import dash

register_page(
    __name__,
    path="/visuals",
    name="📊 Visuals",
    title="Unicorn Dashboard - Visuals"
)

# Load data
df = load_data()
df["Year"] = df["Date Joined"].dt.year

# Setup Dash app instance
app = dash.get_app()

# Precompute simple visuals
top_countries = df['Country'].value_counts().nlargest(10).reset_index()
top_countries.columns = ['Country', 'Count']

top_cities = df['City'].value_counts().nlargest(10).reset_index()
top_cities.columns = ['City', 'Count']

top_industries = df['Industry'].value_counts().nlargest(10).reset_index()
top_industries.columns = ['Industry', 'Count']

# Correlation heatmap
df_encoded = df.copy()
categorical_cols = ['Country', 'City', 'Industry']
for col in categorical_cols:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df_encoded[col])

corr_matrix = df_encoded[['Valuation ($B)', 'Country', 'City', 'Industry']].corr()

heatmap_fig = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale='RdBu',
    zmin=-1, zmax=1,
    hoverongaps=False,
    text=corr_matrix.round(2).values,
    hovertemplate="Correlation: %{z}<extra></extra>"
))
heatmap_fig.update_layout(
    title="Correlation Between Valuation and Categorical Features",
    height=400,
    margin=dict(t=50)
)

# Investor Data
investor_data = (
    df.assign(Select_Investors=df["Select Investors"].str.split(", "))
      .explode("Select_Investors")
      .groupby("Select_Investors")
      .size()
      .reset_index(name="Unicorn Count")
      .rename(columns={"Select_Investors": "Investor"})
      .sort_values("Unicorn Count", ascending=True)
      .tail(20)
)

# Additional Visuals Data
industry_trend = df.groupby(['Year', 'Industry']).size().reset_index(name='Unicorn Count')
fig_industry_trend = px.line(
    industry_trend, x="Year", y="Unicorn Count", color="Industry",
    title="Unicorns Founded per Industry Over Time"
)

fig_valuation_industry = px.violin(
    df, x="Industry", y="Valuation ($B)", box=True, points="all",
    title="Valuation Distribution by Industry"
)

fig_sunburst = px.sunburst(
    df, path=["Country", "City", "Industry"], values="Valuation ($B)",
    title="Geographic and Industry Breakdown of Valuation"
)

industry_bubble = (
    df.groupby("Industry")
      .agg(avg_valuation=("Valuation ($B)", "mean"), count=("Company", "count"))
      .reset_index()
)
fig_bubble = px.scatter(
    industry_bubble, x="count", y="avg_valuation", size="count", color="Industry",
    title="Industry Analysis: Avg Valuation vs. Number of Unicorns",
    labels={"count": "Number of Unicorns", "avg_valuation": "Average Valuation ($B)"}
)

# Layout
layout = html.Div(
    style={"display": "flex", "justifyContent": "center", "padding": "40px"},
    children=[
        html.Div(
            style={"maxWidth": "1200px", "width": "100%"},
            children=[
                html.H2("Unicorn Visualizations", style={"textAlign": "center", "marginBottom": "30px"}),

                dcc.Tabs([
                    # ------------------------ SIMPLE VISUALS ------------------------
                    dcc.Tab(label="📊 Simple Visuals", children=[
                        dcc.Graph(
                            figure=px.histogram(
                                df, x="Valuation ($B)", nbins=30,
                                title="Distribution of Unicorn Valuations"
                            )
                        ),

                        dcc.Graph(
                            figure=px.bar(
                                top_countries, x='Country', y='Count',
                                title='Top 10 Countries with Most Unicorns'
                            )
                        ),

                        dcc.Graph(
                            figure=px.bar(
                                top_cities, x='City', y='Count',
                                title='Top 10 Cities with Most Unicorns'
                            )
                        ),

                        dcc.Graph(
                            figure=px.bar(
                                top_industries, x='Industry', y='Count',
                                title='Top 10 Unicorn Industries'
                            )
                        ),

                        dcc.Graph(figure=heatmap_fig),

                        html.P("""
                            🔎 This heatmap shows the correlation between valuation and categorical features.
                            As observed, there is little to no correlation between Valuation and Country, City, or Industry.
                            This implies that high-valuation startups can emerge across various locations and industries,
                            without strong geographic or sector bias.
                        """)
                    ]),

                    # ------------------------ ADVANCED VISUALS ------------------------
                    dcc.Tab(label="📈 Advanced Visuals", children=[

                        dcc.Graph(
                            figure=px.bar(
                                df.sort_values("Valuation ($B)", ascending=False).head(10),
                                x="Valuation ($B)", y="Company", orientation="h",
                                color="Valuation ($B)", text="Valuation ($B)",
                                hover_data=["Country", "Industry", "City"],
                                title="Top 10 Most Valuable Unicorn Companies",
                                color_continuous_scale="Viridis"
                            ).update_layout(
                                title_font=dict(size=24),
                                xaxis_title="Valuation in Billions ($)",
                                yaxis_title="Company",
                                yaxis=dict(categoryorder='total ascending')
                            ).update_traces(textposition="outside")
                        ),

                        dcc.Graph(
                            figure=px.scatter_geo(
                                df.groupby("Country")["Valuation ($B)"].sum().reset_index().sort_values("Valuation ($B)", ascending=False),
                                locations="Country", locationmode="country names",
                                size="Valuation ($B)", hover_name="Country",
                                title="Total Unicorn Valuation by Country",
                                projection="natural earth",
                                size_max=40, color="Valuation ($B)", color_continuous_scale="Viridis"
                            ).update_layout(
                                title_font=dict(size=24),
                                geo=dict(showframe=False, showcoastlines=True)
                            )
                        ),

                        dcc.Graph(
                            figure=px.treemap(
                                df.groupby("Industry")["Valuation ($B)"].sum().reset_index().sort_values("Valuation ($B)", ascending=False),
                                path=["Industry"], values="Valuation ($B)",
                                title="Unicorn Valuation Distribution by Industry",
                                color="Valuation ($B)", color_continuous_scale="Viridis"
                            ).update_layout(title_font=dict(size=24))
                        ),

                        dcc.Graph(
                            figure=px.line(
                                df.sort_values("Date Joined").assign(Global_Count=lambda d: range(1, len(d)+1)),
                                x="Date Joined", y="Global_Count",
                                title="Cumulative Growth of Unicorn Companies Over Time",
                                labels={"Date Joined": "Date", "Global_Count": "Cumulative Unicorns"}
                            ).update_traces(line=dict(color="royalblue", width=3)).update_layout(
                                title_font=dict(size=24),
                                xaxis_title="Date", yaxis_title="Number of Unicorns"
                            )
                        ),

                        dcc.Graph(
                            figure=px.scatter(
                                df.copy(),
                                x="Valuation ($B)", y="Industry",
                                animation_frame=df["Date Joined"].dt.year.astype(str),
                                size="Valuation ($B)", color="Industry",
                                hover_name="Company", title="Unicorns Over Time: Valuation Growth by Industry",
                                log_x=True, size_max=45, height=700
                            ).update_layout(title_font=dict(size=24))
                        ),

                        dcc.Graph(
                            figure=px.bar(
                                investor_data,
                                x="Unicorn Count", y="Investor", orientation="h",
                                title="Top 20 Most Active Unicorn Investors",
                                text="Unicorn Count", color="Unicorn Count",
                                color_continuous_scale="Viridis"
                            ).update_layout(
                                title_font=dict(size=24),
                                xaxis_title="Number of Unicorns Backed",
                                yaxis_title="Investor"
                            ).update_traces(textposition="outside")
                        ),

                        dcc.Graph(figure=fig_industry_trend),
                        dcc.Graph(figure=fig_valuation_industry),
                        dcc.Graph(figure=fig_sunburst),
                        dcc.Graph(figure=fig_bubble)
                    ])
                ])
            ]
        )
    ]
)
