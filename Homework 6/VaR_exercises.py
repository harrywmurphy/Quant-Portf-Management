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

print("Discussion Question: Calculate the statistics of 1.1 for this portfolio, and compare the results to the individual return statistics. What do you find? What is driving this result?")

print("Answer:The average portfolio volatility was 0.0432 whyich was about 25% lower than the average individual volatility at 0.0578; furthermore, the VaR (-0.606 vs -0.0824) and CVaR (-0.0842 vs 0.1131) were also both around 26% lower in the equally weighted porfolio versus an aggregated analysis of individual positions. These numbers show that subadditivity holds and the porfolio risk is lower than the average of individual risks. This is driven by the fact that these different investments are not perfectly coorelated, so they respond differently to different regimes. In practice, the price of TSLA could fall while the 3 other investments here peform well, so their ups and downs often offset eachother")

#1.3
#Volatility Adjusted Portfolio
highest_vol=summary["Volatility"].idxmax()
spx_vol_filter=spx_sample.copy()
spx_vol_filter[highest_vol]=0
spx_vol_filter_portf=spx_vol_filter.mean(axis=1)
print("1.3\n",risk_stats(spx_vol_filter_portf))

print("Discussion Question: In comparing the answer here to 1.2, how much risk is your most volatile asset adding to the portfolio? Is this in line with the amount of risk we measured in the stand-alone risk-assessment of 1.1?")

print("Answer: TSLA was our most volatile asset, having double the volatility of AAPL, and though diversification helps hamper risk, removing it still led to a 30.5% reduction in volatility, 30.3% reduction in VaR, and 28.7% reduction in CVaR. The increase in risk is significant and it is in line with a reasonable prediction given only the numbers from 1.1")

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

print("Discussion Question: How do these compare to the answers in 1.2?")

print("Answer: With conditional analysis, VaR was 7% less severe and CVaR was 17% less severe, and, after annualizing 1.2 volatility:0.043229 * sqrt(52) = 0.3117 annualized vol, we find that volatiltiy is 21% lower")

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

rolling_backtest["hit"] = rolling_backtest["return"] < rolling_backtest["Rolling VaR"]
rolling_hit_rate = rolling_backtest.dropna()["hit"].mean()
expanding_backtest["hit"] = expanding_backtest["return"] < expanding_backtest["Expanding VaR"]
expanding_hit_rate = expanding_backtest.dropna()["hit"].mean()

print("Rolling hit rate:", (rolling_hit_rate*100).round(2), "%")
print("Expanding hit rate:", (expanding_hit_rate*100).round(2), "%")


