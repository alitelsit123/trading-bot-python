# Import WebSocket client library
from websocket import create_connection
import time
import json
import pprint
import talib
import numpy

# # CONFIGS
# CURRENT_START_TIME = 0
# CURRENT_END_TIME = 0
# CLOSE_PRICE = 0
# OPEN_PRICE = 0
# HIGH_PRICE = 0
# LOW_PRICE = 0
# AVERAGE_VOLUME = 0

# # Connect to WebSocket API and subscribe to trade feed for XBT/USD and XRP/USD
# ws = create_connection("wss://ws.kraken.com/")
# ws.send('{"event":"subscribe", "subscription":{"name":"ohlc", "interval": 1}, "pair":["ETH/USD"]}')

# # Infinite loop waiting for WebSocket data
# while True:
#     try:
#         data = json.loads(ws.recv())
#         if not 'event' in data:
#             CURRENT_START_TIME = data[1][0]
#             CLOSE_PRICE = data[1][5]
#             OPEN_PRICE = data[1][2]
#             HIGH_PRICE = data[1][3]
#             LOW_PRICE = data[1][4]
#             AVERAGE_VOLUME = data[1][7]

#             # END OF CANDLE
#             if float(CURRENT_START_TIME) > float(CURRENT_END_TIME):
#                 CURRENT_END_TIME = data[1][1]
#                 print('\nCandle')
#                 print('Time: {}\nClose Time {}'.format(float(CURRENT_START_TIME), float(CURRENT_END_TIME)))
#                 print('Open Price: {}\nClose Price: {}'.format(OPEN_PRICE, CLOSE_PRICE))
#                 # inputs = {
#                 #     'open': numpy.ndarray(float(OPEN_PRICE), dtype=numpy.float32),
#                 #     'high': numpy.ndarray(float(HIGH_PRICE), dtype=numpy.float32),
#                 #     'low': numpy.ndarray(float(LOW_PRICE), dtype=numpy.float32),
#                 #     'close': numpy.ndarray(float(CLOSE_PRICE), dtype=numpy.float32),
#                 #     'volume': numpy.ndarray(float(AVERAGE_VOLUME), dtype=numpy.float32)
#                 # }
#                 # SMA = abstract.SMA
#                 # sma_result = SMA(inputs, timeperiod=5)
#                 print('Simple Moving Average: {}'.format(numpy.random.random(100)))

#             elif CURRENT_END_TIME == 0:
#                 CURRENT_END_TIME = data[1][1]

#     except (KeyboardInterrupt) as e:
#         print(e)
#         break;
# ws.close()
# print(type(numpy.random.random(100)))
print(talib.SMA(numpy.random.random(20), timeperiod=5))