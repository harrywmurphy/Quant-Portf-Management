import pandas as pd

rates_data = pd.read_csv("ref_rates_data.csv", index_col="date", parse_dates=True)
