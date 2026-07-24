import pandas as pd

spx=pd.read_csv("spx_returns.csv", index_col ="date", parse_dates=True)
spx_sample=spx[["TSLA","AAPL","NVDA","META"]]

#Empirical Stats: Volatility, VaR, CVaR
def risk_stats(returns, q=0.05):
    vol=returns.std()
    var=returns.quantile(q)
    cvar=returns[returns<=var].mean()
    return pd.Series({"Volatility": vol, "VaR":var, "CVaR":cvar})

summary = spx_sample.apply(risk_stats).T
print("1.1\n",summary)

#1.2
#Equally Weighted Portfolio
spx_portf=spx_sample.mean(axis=1)
print("1.2\n",risk_stats(spx_portf))

#1.3
#Volatility Adjusted Portfolio
highest_vol=summary["Volatility"].idxmax()
spx_vol_filter=spx_sample.copy()
spx_vol_filter[highest_vol]=0
spx_vol_filter_portf=spx_vol_filter.mean(axis=1)
print("1.3\n",risk_stats(spx_vol_filter_portf))
