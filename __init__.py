"""
量化回测框架
"""
from core.engine import BacktestEngine
from core.strategy import BaseStrategy
from core.data import DataManager
from utils.indicators import SMA, EMA, MACD, RSI, BOLL, KDJ, ATR, OBV
from utils.plot import BacktestPlotter

__all__ = [
    'BacktestEngine',
    'BaseStrategy',
    'DataManager',
    'SMA',
    'EMA', 
    'MACD',
    'RSI',
    'BOLL',
    'KDJ',
    'ATR',
    'OBV',
    'BacktestPlotter'
]

__version__ = '1.0.0'
