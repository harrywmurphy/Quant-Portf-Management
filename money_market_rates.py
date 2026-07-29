import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
rates_data = pd.read_csv("ref_rates_data.csv", index_col="date", parse_dates=True)

#1.1 Plot the Time Series

fig, ax = plt.subplots(figsize=(11, 4))
rates_data.plot(ax=ax, lw=0.7)
ax.axhline(0, color="black", lw=0.8)
ax.set_ylabel("Rate")
ax.set_title("SOFR, DFF, and DTB3 Rates 2018-2026")

#plt.show()


#1.2 Calculate coorelations among the 3 rates, filtering for when all three rates have values

common=rates_data.dropna()
level_corr=common.corr()
dif_corr=common.diff().corr()

print(level_corr)
print(dif_corr)

#1.3 Estimate an autoregression for SOFR
sofr=rates_data["SOFR"].dropna()

sofr_ar= pd.DataFrame({"y":sofr,"x":sofr.shift(1)})    #Create lagged time series
sofr_ar=sofr_ar.dropna()                               #Clean
print (sofr_ar)

X = sm.add_constant(sofr_ar['x'])
y = sofr_ar['y']

ols_model = sm.OLS(y, X).fit()

print(ols_model.summary())


"""Comment on what this regression tells us about the nature of interest rates.
That is, can we forecast the next periods rate?
Does the series have autocorrelation?"""