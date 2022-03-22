import pandas as pd
import time
import numpy as np
import talib as ta
from sklearn.preprocessing import MinMaxScaler


def divergence(high: pd.Series, low: pd.Series, index: pd.Series, short_range: int, long_range: int) -> pd.Series:
    d = pd.DataFrame()
    d['high'] = high
    d['low'] = low
    d['ind'] = index
    d['high_' + str(short_range) + '_max'] = 0.0
    d['high_' + str(long_range) + '_max'] = 0.0
    d['low_' + str(short_range) + '_min'] = 0.0
    d['low_' + str(long_range) + '_min'] = 0.0
    d['ind_' + str(short_range) + '_max'] = 0.0
    d['ind_' + str(short_range) + '_min'] = 0.0
    d['ind_' + str(long_range) + '_max'] = 0.0
    d['ind_' + str(long_range) + '_min'] = 0.0
    d['ind_div'] = 0

    i = 0
    for index, row in d.iterrows():
        d.iloc[i, 3] = d['high'][i - short_range + 1:i + 1].max()
        d.iloc[i, 4] = d['high'][i - long_range + 1:i + 1].max()
        d.iloc[i, 5] = d['low'][i - short_range + 1:i + 1].min()
        d.iloc[i, 6] = d['low'][i - long_range + 1:i + 1].min()
        d.iloc[i, 7] = d['ind'][i - short_range + 1:i + 1].max()
        d.iloc[i, 8] = d['ind'][i - short_range + 1:i + 1].min()
        d.iloc[i, 9] = d['ind'][i - long_range + 1:i + 1].max()
        d.iloc[i, 10] = d['ind'][i - long_range + 1:i + 1].min()

        if d.iloc[i, 3] == d.iloc[i, 4] and d.iloc[i, 7] < d.iloc[i, 9]:
            d.iloc[i, 11] = -100
        elif d.iloc[i, 5] == d.iloc[i, 6] and d.iloc[i, 8] > d.iloc[i, 10]:
            d.iloc[i, 11] = 100
        else:
            d.iloc[i, 11] = 0
        i += 1

    return d.ind_div


def divbar(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    d = pd.DataFrame()
    d['high'] = high
    d['low'] = low
    d['close'] = close
    d['high_3_max'] = 0.0
    d['low_3_min'] = 0.0
    d['divbar'] = 0

    i = 0
    for index, row in d.iterrows():
        d.iloc[i, 3] = d['high'][i - 3 + 1:i + 1].max()
        d.iloc[i, 4] = d['low'][i - 3 + 1:i + 1].min()
        if d.iloc[i, 3] == d.iloc[i, 0] and (d.iloc[i, 2] < ((d.iloc[i, 0] - d.iloc[i, 1]) / 3 + d.iloc[i, 1])):
            d.iloc[i, 5] = -100
        if d.iloc[i, 4] == d.iloc[i, 1] and (d.iloc[i, 2] > (d.iloc[i, 0] - (d.iloc[i, 0] - d.iloc[i, 1]) / 3)):
            d.iloc[i, 5] = 100
        i += 1
    return d.divbar


def bb_touch(bbUp: pd.Series, bbDown: pd.Series, high: pd.Series, low: pd.Series, perc: float) -> pd.Series:
    d = pd.DataFrame()
    d['bbUp'] = bbUp
    d['bbDown'] = bbDown
    d['high'] = high
    d['low'] = low

    d['upBorder'] = d.bbUp - (d.bbUp - d.bbDown) * perc
    d['downBorder'] = (d.bbUp - d.bbDown) * perc + d.bbDown

    d['upTouch'] = np.where(d['high'] > d['upBorder'], -1, 0)
    d['downTouch'] = np.where(d['low'] < d['downBorder'], 1, 0)

    return d['upTouch'] + d['downTouch']


def percent_change(close: pd.Series, n: int) -> pd.Series:
    d = pd.DataFrame()
    d['close'] = close
    d['prcntChng'] = 0

    i = 0
    for index, row in d.iterrows():
        d.iloc[i, 1] = d['close'][i] / d['close'][i - n] - 1
        i += 1

    return d.prcntChng


def over_zones_indicator(indicator_value: float, overbought: float, oversold: float) -> int:
    if indicator_value > overbought:
        return -1
    elif indicator_value < oversold:
        return 1
    else:
        return 0


def regression_line_angle(data, reg_n):
    d = pd.DataFrame()
    d['data'] = data
    d['angle'] = 0

    i = 0
    for index, row in d.iterrows():
        if i < reg_n + 1:
            d.iloc[i, 1] = 0
        else:
            try:
                scaler = MinMaxScaler(feature_range=(0, 20))
                scaled_data = scaler.fit_transform(d['data'][i - reg_n + 1:i + 1].values.reshape(-1, 1)).reshape(-1)
                z = np.polyfit(range(reg_n), scaled_data, 1)

                p = np.poly1d(z)
                data_reg = p(range(reg_n))
                reg_Angle = np.rad2deg(np.arctan2(data_reg[-1] - data_reg[1], len(data_reg) - 1))
            except:
                print('Error in RegAngle: i {0}, array: {1}'.format(i, d['data'][i - reg_n + 1:i + 1]))
                reg_Angle = 0
            d.iloc[i, 1] = reg_Angle
        i += 1

    return d.angle

# TODO what to do with murray math
def murray_math_count(high: pd.Series, low: pd.Series, close: pd.Series):
    max_price = high.max()
    min_price = low.min()
    cur_price = close.values[-1]

    if max_price < 1:
        octave = 1
    elif max_price < 10:
        octave = 10
    elif max_price < 100:
        octave = 100
    elif max_price < 1000:
        octave = 1000
    elif max_price < 10000:
        octave = 10000
    else:
        octave = 100000

    main_step = octave / 8
    mm_main_lines = []
    for i in range(0, 9):
        mm_main_lines.append(main_step * i)

    i = 0
    while cur_price >= mm_main_lines[i]:
        i += 1

    q_min = mm_main_lines[i - 1]
    q_max = mm_main_lines[i]

    step = (q_max - q_min) / 8
    dict_mm_lines = dict()
    for j in range(0, 9):
        dict_mm_lines[str(j)] = q_min + step * j

    return dict_mm_lines

def get_available_features_list():
    return [
        {
            'name': 'MA',
            'description': 'Simple moving average',
            'params': {
                'period': {'type': 'integer', 'default': 8, 'description': 'Simple moving average period'},
                'extended': {'type': 'boolean', 'default': False, 'description': 'Add extended to features'},
            }
        },
        {
            'name': 'MACD',
            'description': 'MACD',
            'params': {
                'fastperiod': {'type': 'integer', 'default': 5, 'description': 'fastperiod'},
                'slowperiod': {'type': 'integer', 'default': 35, 'description': 'slowperiod'},
                'signalperiod': {'type': 'integer', 'default': 3, 'description': 'signalperiod'},
                'extended': {'type': 'boolean', 'default': False, 'description': 'Add extended to features'},
                'divergence': {'type': 'boolean', 'default': False, 'description': 'Add divergence to features'}
            }
        },
        {
            'name': 'CCI',
            'description': 'CCI',
            'params': {
                'timeperiod': {'type': 'integer', 'default': 13, 'description': 'CCI'},
                'extended': {'type': 'boolean', 'default': False, 'description': 'Add extended to features'},
                'divergence': {'type': 'boolean', 'default': False, 'description': 'Add divergence to features'}
            }
        },
        {
            'name': 'Williams',
            'description': 'Williams',
            'params': {
                'timeperiod': {'type': 'integer', 'default': 8, 'description': 'Willams percentage range'},
                'extended': {'type': 'boolean', 'default': False, 'description': 'Add extended to features'},
                'divergence': {'type': 'boolean', 'default': False, 'description': 'Add divergence to features'}
            }
        },
        {
            'name': 'Bollindger Bands',
            'description': 'Bollindger Bands',
            'params': {
                'timeperiod': {'type': 'integer', 'default': 8, 'description': 'Bollindger Bands period'},
                'extended': {'type': 'boolean', 'default': False, 'description': 'Add extended to features'},
            }
        },
        {
            'name': 'DivBar',
            'description': 'DivBar',
            'params': {}
        },
        {
            'name': 'Hummer',
            'description': 'Hummer',
            'params': {}
        },
        {
            'name': 'Shooting star',
            'description': 'Shooting star',
            'params': {}
        },
        {
            'name': 'Regression Line Angle',
            'description': 'Regression Line Angle',
            'params': {
                'timeperiod': {'type': 'integer', 'default': 8, 'description': ' Bar in row length '},
            }
        },
        {
            'name': 'Murray Math Lines',
            'description': 'Murray Math Lines',
            'params': {}
        }
    ]


def extend_dataframe_with_features(initial_dataframe: pd.DataFrame, features=[]) -> pd.DataFrame:
    df = initial_dataframe.copy()

    if len(features) > 0:
        for feature in features:

            if feature['name'] == 'MA':
                df[feature['code']] = ta.EMA(df.close, feature['params']['period'])
                if feature['params'].get('extended'):
                    df[f"{feature['code']}_position_at_price"] = df.close - df[feature['code']]
                    df[f"{feature['code']}_position_at_price"] = df[f"{feature['code']}_position_at_price"].apply(lambda x: 1 if x > 0 else 0)

            if feature['name'] == 'MACD':
                df[feature['code']], _, _ = ta.MACD(df.close,
                                                    feature['params']['fastperiod'],
                                                    feature['params']['slowperiod'],
                                                    feature['params']['signalperiod'])
                if feature['params'].get('extended'):
                    df[f"{feature['code']}_change"] = df[feature['code']].shift(1)
                    df[f"{feature['code']}_change"] = df[feature['code']] - df[f"{feature['code']}_change"]
                    df[f"{feature['code']}_change"] = df[f"{feature['code']}_change"].apply(lambda x: 1 if x > 0 else 0)
                if feature['params'].get('divergence'):
                    df[f"{feature['code']}_divergence_short"] = divergence(df.high, df.low, df[feature['code']], 3, 8)
                    df[f"{feature['code']}_divergence_long"] = divergence(df.high, df.low, df[feature['code']], 5, 35)

            if feature['name'] == 'CCI':
                df[feature['code']] = ta.CCI(df.high,
                                             df.low,
                                             df.close,
                                             feature['params']['timeperiod'])
                if feature['params'].get('extended'):
                    df[f"{feature['code']}_over_zones"] = df[feature['code']].apply(over_zones_indicator, args=[100, -100])
                if feature['params'].get('divergence'):
                    df[f"{feature['code']}_divergence_short"] = divergence(df.high, df.low, df[feature['code']], 3, 8)
                    df[f"{feature['code']}_divergence_long"] = divergence(df.high, df.low, df[feature['code']], 5, 35)

            if feature['name'] == 'Williams':
                df[feature['code']] = ta.WILLR(df.high,
                                               df.low,
                                               df.close,
                                               feature['params']['timeperiod'])
                if feature['params'].get('extended'):
                    df[f"{feature['code']}_over_zones"] = df[feature['code']].apply(over_zones_indicator, args=[100, -100])
                if feature['params'].get('divergence'):
                    df[f"{feature['code']}_divergence_short"] = divergence(df.high, df.low, df[feature['code']], 3, 8)
                    df[f"{feature['code']}_divergence_long"] = divergence(df.high, df.low, df[feature['code']], 5, 35)

            if feature['name'] == 'Bollindger Bands':
                df[f"up_{feature['code']}"], \
                df[f"mid_{feature['code']}"], \
                df[f"low_{feature['code']}"] = ta.BBANDS(df.close,
                                                        feature['params']['timeperiod'],
                                                        nbdevup=2,
                                                        nbdevdn=2,
                                                        matype=0)
                if feature['params'].get('extended'):
                    df[f"{feature['code']}_touch"] = bb_touch(df[f"up_{feature['code']}"],
                                                              df[f"low_{feature['code']}"],
                                                              df.high,
                                                              df.low,
                                                              0.1)

            if feature['name'] == 'DivBar':
                df[feature['code']] = divbar(df.high, df.low, df.close)

            if feature['name'] == 'Hummer':
                df[feature['code']] = ta.CDLHAMMER(df.open, df.high, df.low, df.close)

            if feature['name'] == 'Shooting star':
                df[feature['code']] = ta.CDLSHOOTINGSTAR(df.open, df.high, df.low, df.close)

            if feature['name'] == 'Regression Line Angle':
                df[feature['code']] = regression_line_angle(df.close, feature['params']['timeperiod'])

    df['datetime'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    df.set_index('datetime', inplace=True)

    return df
