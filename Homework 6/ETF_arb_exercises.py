import pandas as pd
import matplotlib.pyplot as plt

#1.1 ETF Arb
#Importing the csvs
prices = pd.read_csv("etf_arb_data_prices.csv", index_col="date", parse_dates=True)
nav = pd.read_csv("etf_arb_data_nav.csv", index_col="date", parse_dates=True)

# premium/discount in bps, all funds at once
premium = (prices / nav - 1) * 1e4

#getting the analysis stats for spy prem/discount
spy_stats = premium["SPY"].describe()[["mean", "std", "min", "max"]]
print(spy_stats.round(2))

#plotting with matplotlib
"""
fig, ax = plt.subplots(figsize=(11, 4))
premium["SPY"].plot(ax=ax, lw=0.7)
ax.axhline(0, color="black", lw=0.8)
ax.set_ylabel("premium/discount (bps)")
ax.set_title("SPY price vs NAV")
plt.show()
"""
# 1.2
nav_last = nav["SPY"].dropna().iloc[-1]
last_date = nav["SPY"].dropna().index[-1]

units = 50000
premium = 0.005

basket_cost = units * nav_last          # what the AP pays for the shares/basket
proceeds = units * nav_last * (1 + premium)  # what the AP sells the new shares for
gross_profit = proceeds - basket_cost

print(f"NAV as of {last_date.date()}: ${nav_last:,.2f}")
print(f"Creation unit notional: ${basket_cost:,.0f}")
print(f"Gross profit: ${gross_profit:,.0f}")

#1.3
fixed_fee = 3_000
trading_cost = 0.0003          # 3 bps on the basket
notional = units * nav_last    # units = 50_000 from 1.2

breakeven = (fixed_fee / notional + trading_cost)*100

print("Breakeven point is at a", breakeven,"percent premium")

#2.1
hyg_prices = prices["HYG"]
hyg_nav = nav["HYG"]

hyg_premium = (hyg_prices/hyg_nav-1)*1e4
hyg_premium=hyg_premium.dropna()
hyg_premium=hyg_premium.loc["2020"]
print(hyg_premium)

hyg_stats=hyg_premium.sort_values()
print("Max premium in 2020:",hyg_stats.iloc[-1],"bps on", hyg_stats.index[-1].date(),
      "\nMin Discount in 2020:",hyg_stats.iloc[0],"bps on", hyg_stats.index[0].date())

fig, ax = plt.subplots(figsize=(11, 4))
hyg_premium.plot(ax=ax, lw=0.7)
ax.axhline(0, color="black", lw=0.8)
ax.set_ylabel("premium/discount (bps)")
ax.set_title("HYG price vs NAV")
plt.show()

#2.2
"""Yes, buying HYG shares at the discount rate in March 2020 and redeeming the bonds to
sell them would be an arbitrage, but it would not have been easily exploitable. In order
to even redeem HYG shares for bonds, you need to be an authorized participant (like a large Asset Manager)
and would also then need to sell thousands of illiquid bonds on an exchange. """

#2.3
""""""