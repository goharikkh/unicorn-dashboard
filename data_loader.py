# # data_loader.py
# import pandas as pd

# def load_data():
#     url = "https://drive.google.com/uc?id=1N6P2DslDuTBPqe8njbI6G67iqJF5hUpG"
#     df = pd.read_csv(url)
#     df["Date Joined"] = pd.to_datetime(df["Date Joined"], errors="coerce")
#     df["Year"] = df["Date Joined"].dt.year
#     return df


# data_loader.py
import pandas as pd

def load_data():
    url = "https://docs.google.com/spreadsheets/d/1gt5SevuvTRyS4qMW9_kntBODaNIolP-Ok_oIQwF9cEs/export?format=csv"
    df = pd.read_csv(url)
    df["Date Joined"] = pd.to_datetime(df["Date Joined"], errors="coerce")
    df["Year"] = df["Date Joined"].dt.year
    return df
