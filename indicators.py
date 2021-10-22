import talib
import numpy

def indicators():
    print('SMA: {}'.format('pass'))
    print('EMA: {}'.format('-'))
    print('MACD: {}'.format('-'))
    print('RSI: {}'.format('-'))

def simple_moving_average(data, timeperiod):
    return talib.SMA(numpy.array(data[:]), timeperiod=timeperiod)