# Binance API connection demo

[![](https://img.shields.io/badge/python-3.9%2B-informational)](https://www.python.org/downloads/release/python-370/)

### This repo contains example usage of Binance API using [python-binance](https://python-binance.readthedocs.io/en/latest/index.html) wrapper.

Main idea behind this was not to build outstanding bot with excellent profitable strategy, but just to show a way of connection to the Binance API.

Strategy in this example is implemented with the most basic RSI indicator and it's using overbought/oversold pattern to place orders.

_<span style="background-color: #cc0000">Please remember then that if you do use this strategy on the real market it is at your own risk.</span>_

---

## Usage instructions

Install required dependencies:

```bash
$ pip install -r requirements.txt
```

Enter your **API_KEY** and **API_SECRET** into _config.py_ file:

```python
API_KEY = ""
API_SECRET = ""
```

_Optionally you can change parameters of the strategy and desired instrument in *config.py*:_

```python
SOCKET = "wss://stream.binance.com:9443/ws/dogeeur@kline_1m"
# RSI parameters
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
# Instrument details
TRADE_PAIR = ("DOGE", "EUR")
```

Run in the terminal:

```bash
$ python3 main.py
```

## Links

[Binance API docs](https://binance-docs.github.io/apidocs/spot/en/#change-log)
