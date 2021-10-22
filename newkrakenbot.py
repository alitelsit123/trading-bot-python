import pprint
import numpy
import schedule
from indicators import *
from kraken_func import *

_TOTAL_ASSET = 0
_CURRENT_POSITION = 'buy'
_BUY_PRICE = 0
_CURRENT_SMA_SHORT = 0
_CURRENT_SMA_MIDDLE = 0
_SKIPPED = True

def buy():
    indicators()
    print('ITS TIME BABY!!!')
    print('BUY BUY BUY!!!')

def sell():
    indicators()
    print('ITS TIME BABY!!!')
    print('SELL SELL SELL!!!')

def mn():
    global _BUY_PRICE
    global _SKIPPED
    global _CURRENT_POSITION

    ohlc_history_data_response = request_get({
        'path': '/public/OHLC?pair=ETHUSDC&interval=1&since=1623046499',
        'api_key': API_KEY,
        'api_secret': API_SECRET
    })
    
    # print(numpy.array(resp.json()['result']['ETHUSDC'][:]))
    original_data = ohlc_history_data_response.json()['result']['ETHUSDC']
    filtered_data = [float(original_data[i][4]) for i in range(0, len(original_data))]
    
    sma_result_short = simple_moving_average(data=filtered_data, timeperiod=5)
    sma_result_middle = simple_moving_average(data=filtered_data, timeperiod=20)
    
    print('')
    show_info({
        'asset': 'ETH',
        'using': 'USDC',
        'p': _CURRENT_POSITION[0]
    })
    print('SMA_5: {}'.format(sma_result_short[-1]))
    print('SMA_20: {}'.format(sma_result_middle[-1]))
    print('PRICE: {}'.format(filtered_data[-1]))

    if sma_result_short[-1] >= sma_result_middle[-1]:
        if _CURRENT_POSITION == 'sell':
            print('TEMP ACTION: {}'.format('b'))
            if not _SKIPPED:
                buy()
                _SKIPPED = False
                _BUY_PRICE = filtered_data[-1]
                print('BUY PRICE: {}'.format(_BUY_PRICE))
            _CURRENT_POSITION = 'buy'
        else:
            print('ACTION: {}'.format('-'))
    if sma_result_middle[-1] >= sma_result_short[-1]:
        if _CURRENT_POSITION == 'buy':
            print('TEMP ACTION: {}'.format('s'))
            if not _SKIPPED:
                sell()
                _SKIPPED = False
            _CURRENT_POSITION = 'sell'
        else:
            print('ACTION: {}'.format('-'))

def run_forever():
    schedule.every(5).seconds.do(mn)
    while True:
        schedule.run_pending()
        time.sleep(5)

run_forever()
