from binance.client import Client


# Your individual API KEY and API SECRET from Binance
API_KEY = ""
API_SECRET = ""

# DOGEEUR 1 minute candles stream
SOCKET = "wss://stream.binance.com:9443/ws/dogeeur@kline_1m"
# RSI parameters
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
# Instrument details
TRADE_PAIR = ("DOGE", "EUR")
ORDER_TYPE = Client.ORDER_TYPE_MARKET
TRADE_QUANTITY = 50
FEE = 0.001
TRADE_SYMBOL = f"{TRADE_PAIR[0]} + {TRADE_PAIR[1]}"
