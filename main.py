import math
import websocket
import json
import pprint
import talib
import ssl
import numpy as np
from binance import Client
import config


# Connecting to API using  API_KEY and API_SECRET
client = Client(config.API_KEY, config.API_SECRET, tld="com")
net_quantity = math.floor(config.TRADE_QUANTITY - (config.TRADE_QUANTITY * config.FEE))
close_prices = []
is_position_active = False


# Functions that handling connection status when opened, closed and error occurred
def on_open(ws):
    print("Opened connection")


def on_close(ws, close_status_code, close_msg):
    print("Closed connection")


def on_error(ws, error):
    print("ERROR")
    print(error)


# Load json data from candle stream
def load_json_message(message):
    json_message = json.loads(message)
    pprint.pprint(json_message)
    return json_message


# Calculate values of RSI indicator
def calculate_rsi(close_prices):
    np_closes = np.array(close_prices)
    rsi_values = talib.RSI(np_closes, config.RSI_PERIOD)
    print(rsi_values)
    return rsi_values


# Check if strategy met buy/sell conditions
def check_strategy_condition(signal_trigger):
    # BUY SIGNAL
    if signal_trigger < config.RSI_OVERSOLD:
        if is_position_active:
            print("You are already in")
            # ws.close()
        else:
            print("Buy")
            send_order(Client.SIDE_BUY)
            # ws.close()
    # SELL SIGNAL
    if signal_trigger > config.RSI_OVERBOUGHT:
        if is_position_active:
            print("Sell")
            send_order(Client.SIDE_SELL)
            # ws.close()
        else:
            print("You've got nothing to sell")
            # ws.close()


# Executing order
def order(side, quantity, symbol, order_type=config.ORDER_TYPE):
    try:
        print("sending order")
        order = client.create_order(
            symbol=symbol, side=side, type=order_type, quantity=quantity
        )
        print(order)
    except Exception as e:
        print("Something wrong")
        print(e)
        return False
    return True


# Place order
def send_order(order_side):
    global is_position_active
    if order_side == Client.SIDE_BUY:
        print("Oversold")
    else:
        print("Overbought")
    order_succeeded = order(order_side, config.TRADE_QUANTITY, config.TRADE_SYMBOL)
    if order_succeeded and order_side == Client.SIDE_BUY:
        is_position_active = True
    elif order_succeeded and order_side == Client.SIDE_SELL:
        is_position_active = False


# On every candle tick
def on_message(ws, message):
    global close_prices, is_position_active
    print("Received message")

    # Print assets balance account info
    first_asset_balance = client.get_asset_balance(asset=config.TRADE_PAIR[0])
    print(first_asset_balance)
    second_asset_balance = client.get_asset_balance(asset=config.TRADE_PAIR[1])
    print(second_asset_balance)

    # Receive candles data in json
    json_message = load_json_message(message)

    # Retrive candles from json
    candle_dict = json_message["k"]  # dictionary candle representation in the stream
    candle_close_price = candle_dict["c"]  # candle closed price
    is_closed = candle_dict["x"]  # True/False indicates if candle is closed

    # Candle is fully formed, append closed price
    if is_closed == True:
        print(f"Candle closed price is: {candle_close_price}")
        close_prices.append(float(candle_close_price))

        print("Close prices:")
        print(close_prices)

        # If enough data to calculate RSI
        if len(close_prices) > config.RSI_PERIOD:
            # Start calculating RSI
            last_rsi = calculate_rsi(close_prices=close_prices)[-1]
            print(f"Last calculated rsi value: {last_rsi}")

            # Checking strategy conditions
            check_strategy_condition(last_rsi)


ws = websocket.WebSocketApp(
    config.SOCKET,
    on_open=on_open,
    on_close=on_close,
    on_message=on_message,
    on_error=on_error,
)
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
