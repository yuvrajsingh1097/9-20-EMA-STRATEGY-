



# import ccxt
# import pandas as pd
# import numpy as np

# # Function to calculate EMA
# def calculate_ema(data, period):
#     return data.ewm(span=period, adjust=False).mean()

# # Function to detect crossover signals
# def detect_signals(df):
#     df['Signal'] = 0  # 0: Hold, 1: Buy, -1: Sell
#     df['Prev_EMA9'] = df['EMA9'].shift(1)
#     df['Prev_EMA20'] = df['EMA20'].shift(1)
    
#     # Bullish crossover: EMA9 crosses above EMA20
#     bullish = (df['EMA9'] > df['EMA20']) & (df['Prev_EMA9'] <= df['Prev_EMA20'])
#     df.loc[bullish, 'Signal'] = 1
    
#     # Bearish crossover: EMA9 crosses below EMA20
#     bearish = (df['EMA9'] < df['EMA20']) & (df['Prev_EMA9'] >= df['Prev_EMA20'])
#     df.loc[bearish, 'Signal'] = -1
    
#     return df

# # Main function
# def main():
#     # Initialize exchange (Binance)
#     exchange = ccxt.binance()
    
#     # Fetch historical data (last 100 candles, 1-hour timeframe for BTC/USDT)
#     symbol = 'BTC/USDT'
#     timeframe = '1h'
#     limit = 100
#     ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    
#     # Convert to DataFrame
#     df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
#     df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
#     df.set_index('timestamp', inplace=True)
    
#     # Calculate EMAs
#     df['EMA9'] = calculate_ema(df['close'], 9)
#     df['EMA20'] = calculate_ema(df['close'], 20)
    
#     # Detect signals
#     df = detect_signals(df)
    
#     # Print recent signals
#     print("Recent EMA Crossover Signals for BTC/USDT:")
#     recent_signals = df.tail(10)[['close', 'EMA9', 'EMA20', 'Signal']]
#     print(recent_signals)
    
#     # Example: Count signals
#     buys = (df['Signal'] == 1).sum()
#     sells = (df['Signal'] == -1).sum()
#     print(f"\nTotal Buy Signals: {buys}")
#     print(f"Total Sell Signals: {sells}")

# if __name__ == "__main__":
#     main()



import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate EMA
def calculate_ema(data, period):
    return data.ewm(span=period, adjust=False).mean()

# Function to detect crossover signals
def detect_signals(df):
    df['Signal'] = 0  # 0: Hold, 1: Buy, -1: Sell
    df['Prev_EMA9'] = df['EMA9'].shift(1)
    df['Prev_EMA20'] = df['EMA20'].shift(1)
    
    # Bullish crossover: EMA9 crosses above EMA20 (golden cross) - Go Up
    bullish = (df['EMA9'] > df['EMA20']) & (df['Prev_EMA9'] <= df['Prev_EMA20'])
    df.loc[bullish, 'Signal'] = 1
    
    # Bearish crossover: EMA9 crosses below EMA20 (death cross) - Go Down
    bearish = (df['EMA9'] < df['EMA20']) & (df['Prev_EMA9'] >= df['Prev_EMA20'])
    df.loc[bearish, 'Signal'] = -1
    
    return df

# Function to plot the chart with signals and trend indications
def plot_chart(df, symbol):
    plt.figure(figsize=(14, 7))
    
    # Plot close price
    plt.plot(df.index, df['close'], label='Close Price', color='blue', alpha=0.5)
    
    # Plot EMAs
    plt.plot(df.index, df['EMA9'], label='EMA9', color='green')
    plt.plot(df.index, df['EMA20'], label='EMA20', color='red')
    
    # Plot buy signals with annotation
    buy_signals = df[df['Signal'] == 1]
    plt.scatter(buy_signals.index, buy_signals['close'], marker='^', color='green', s=100, label='Buy Signal')
    for idx, row in buy_signals.iterrows():
        plt.annotate('Buy: Go Up', (idx, row['close']), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, color='green')
    
    # Plot sell signals with annotation
    sell_signals = df[df['Signal'] == -1]
    plt.scatter(sell_signals.index, sell_signals['close'], marker='v', color='red', s=100, label='Sell Signal')
    for idx, row in sell_signals.iterrows():
        plt.annotate('Sell: Go Down', (idx, row['close']), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=9, color='red')
    
    # Determine current trend based on latest EMAs
    latest_ema9 = df['EMA9'].iloc[-1]
    latest_ema20 = df['EMA20'].iloc[-1]
    if latest_ema9 > latest_ema20:
        current_trend = "Current Trend: EMA9 > EMA20 - Likely Go Up (Bullish)"
        trend_color = 'green'
    else:
        current_trend = "Current Trend: EMA9 < EMA20 - Likely Go Down (Bearish)"
        trend_color = 'red'
    
    # Add current trend text on the chart
    plt.text(0.02, 0.98, current_trend, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor=trend_color, alpha=0.5), color='white')
    
    plt.title(f'{symbol} Price with EMA9/EMA20 Crossover Signals')
    plt.xlabel('Time')
    plt.ylabel('Price (USDT)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function
def main():
    # Initialize exchange (Binance)
    exchange = ccxt.binance()
    
    # Fetch historical data (last 100 candles, 1-hour timeframe for BTC/USDT)
    symbol = 'BTC/USDT'
    timeframe = '1h'
    limit = 100
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    
    # Convert to DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    # Calculate EMAs
    df['EMA9'] = calculate_ema(df['close'], 9)
    df['EMA20'] = calculate_ema(df['close'], 20)
    
    # Detect signals
    df = detect_signals(df)
    
    # Print recent signals
    print("Recent EMA Crossover Signals for BTC/USDT:")
    recent_signals = df.tail(10)[['close', 'EMA9', 'EMA20', 'Signal']]
    print(recent_signals)
    
    # Example: Count signals
    buys = (df['Signal'] == 1).sum()
    sells = (df['Signal'] == -1).sum()
    print(f"\nTotal Buy Signals: {buys}")
    print(f"Total Sell Signals: {sells}")
    
    # Plot the chart
    plot_chart(df, symbol)

if __name__ == "__main__":
    main()