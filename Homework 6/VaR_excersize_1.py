import pandas as pd
import math

spx=pd.read_csv("spx_returns.csv", index_col ="date", parse_dates=True)
spx_sample=spx[["TSLA","AAPL","NVDA","META"]]

#1.1
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

#2.1
#Rolling Volatility 
rolling_vol=spx_sample.rolling(26).std().shift(1)
portf_rolling_vol=spx_portf.rolling(26).std().shift(1)

#Annualize
ann_rolling_vol=rolling_vol.iloc[-1]*math.sqrt(52)
ann_portf_rolling_vol=portf_rolling_vol.iloc[-1]*math.sqrt(52)

#Normal VaR and CVaR
z=-1.65
phi = math.exp(-z**2/2) / math.sqrt(2*math.pi)   
normal_var  = portf_rolling_vol.iloc[-1] * z
normal_cvar = portf_rolling_vol.iloc[-1] * (-phi / 0.05)

print("2.1")
print("Annualized Rolling Volatility per security is\n",ann_rolling_vol)
print("Annualized Rolling Equally Balanced Portfolio Volatility is",ann_portf_rolling_vol)
print("Normal VaR is", normal_var,)
print("Normal CVaR is", normal_cvar)

#2.2
portf_rolling_vol=spx_portf.rolling(26).std().shift(1)
rolling_normal_var=portf_rolling_vol*z
portf_expanding_vol=spx_portf.expanding().std().shift(1)
expanding_normal_var=portf_expanding_vol*z

rolling_backtest = pd.DataFrame({
    "return": spx_portf,
    "Rolling VaR": rolling_normal_var,
})
expanding_backtest = pd.DataFrame({
    "return": spx_portf,
    "Expanding VaR": expanding_normal_var,
})
\
rolling_backtest["hit"] = rolling_backtest["return"] < rolling_backtest["Rolling VaR"]
rolling_hit_rate = rolling_backtest.dropna()["hit"].mean()
expanding_backtest["hit"] = expanding_backtest["return"] < expanding_backtest["Expanding VaR"]
expanding_hit_rate = expanding_backtest.dropna()["hit"].mean()

print("Rolling hit rate:", (rolling_hit_rate*100).round(2), "%")
print("Expanding hit rate:", (expanding_hit_rate*100).round(2), "%")


    
