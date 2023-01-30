import backtrader as bt
import datetime
from strategiesTestowa import TestStrategy
import matplotlib
import itertools 
# from backtrader_plotting import Bokeh
# from backtrader_plotting.schemes import Tradimo
import numpy as np
import backtrader.analyzers as btanalyzers
import pandas as pd


def objective(trial):

    # Mateusz: Tutaj prosimy o sugestię float z danego zakresu.
    alpha = trial.suggest_float('alpha', 0.001, 0.02)
    open_threshold = trial.suggest_float('open_threshold', 0.3, 0.99)
    close_threshold = trial.suggest_float('close_threshold', 1.001, 2)
    pip_av_days = trial.suggest_int('pip_av_days', 10, 700)
    n_days= trial.suggest_int('n_days', 10, 700)
    max_module_period = trial.suggest_int('max_module_period', 50, 1000)
    min_swap = trial.suggest_float('min_swap', 0,0)
    av_VIX_days = trial.suggest_int('av_VIX_days', 10,400)
    open_VIX = trial.suggest_float('open_VIX', 0.3, 0.999)
    close_vix = trial.suggest_float('close_vix', 1.001, 6)



    cerebro = bt.Cerebro()

    cerebro.broker.set_cash(1000000)

    instruments = ['USDDKK wyrownane ceny', 'USDPLN wyrownane ceny', 'USDDKK wyrownane swapy', 'USDPLN wyrownane swapy', 'VIX']
    for instrument in instruments:
        datapath = f"{instrument}.csv"
        # Create a Data Feed
        data = bt.feeds.GenericCSVData(
            dataname=datapath,
            fromdate=datetime.datetime(2005, 1, 3),
            todate=datetime.datetime(2022, 1, 5),
            reverse=False,
            dtformat="%Y-%m-%d",
            #dtformat = "%d%m%Y",
            openinterest=-1)
        cerebro.adddata(data, name=instrument)

    # Mateusz: zmieniłem inicjalizację TestStrategy, żeby przyjmowała parametr alpha.
    # Parametr alpha (z linii 17) przekazuję do strategii.
    cerebro.addstrategy(TestStrategy, alpha=alpha, open_threshold=open_threshold, close_threshold=close_threshold,
    pip_av_days=pip_av_days, n_days=n_days, max_module_period=max_module_period, min_swap=min_swap, av_VIX_days=av_VIX_days, open_VIX=open_VIX, close_vix=close_vix)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    value = cerebro.run() 

    
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.addwriter(bt.WriterFile, csv=True)

    # Mateusz: tutaj musisz uzupełnić jak wyciągnąć prawdziwy profit.
    profit = cerebro.broker.getvalue()

    # Mateusz: wartość minimalizujemy, więc musi być "minus" profit czy "minus" SR.
    return (-1) * value[0].test_swap_priceChange
