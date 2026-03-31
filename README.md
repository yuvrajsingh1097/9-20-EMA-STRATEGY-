# 9-20-EMA-STRATEGY-
Python script for 9-20 EMA crossover strategy on crypto: Fetches data from Binance, calculates EMAs, and generates buy/sell signals for BTC/USDT.



Step A: Identifying the Crossover
Look for the point where the two lines intersect. A "Bullish Cross" indicates that average prices over the last 9 periods are rising faster than the last 20, suggesting upward momentum.

Step B: The Trigger Candle
Don't enter the moment the lines touch. Wait for the entry candle to close. If you are going long, the candle should ideally be green and closing near its high to confirm strength.

Step C: Stop Loss and Take Profit
Stop Loss: Usually placed just below the EMA 20 (for longs) or above the EMA 20 (for shorts). Alternatively, use the recent "swing high" or "swing low."

Exit: Many traders exit when the EMA 9 crosses back over the EMA 20 in the opposite direction, or when price action shows a clear reversal pattern.
