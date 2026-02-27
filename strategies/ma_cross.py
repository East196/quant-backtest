"""
均线交叉策略
"""
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.strategy import BaseStrategy
from utils.indicators import SMA


class MACrossStrategy(BaseStrategy):
    """
    均线交叉策略
    
    当短期均线上穿长期均线时买入
    当短期均线下穿长期均线时卖出
    """
    
    def __init__(self, short_window: int = 5, long_window: int = 20):
        """
        初始化策略
        
        Args:
            short_window: 短期均线周期
            long_window: 长期均线周期
        """
        super().__init__(
            name=f"MA_{short_window}_{long_window}",
            short_window=short_window,
            long_window=long_window
        )
        
        self.short_window = short_window
        self.long_window = long_window
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        生成交易信号
        
        Args:
            data: 价格数据
            
        Returns:
            信号序列
        """
        # 计算均线
        short_ma = SMA(data['close'], self.short_window)
        long_ma = SMA(data['close'], self.long_window)
        
        # 生成信号
        signals = pd.Series(0, index=data.index)
        
        # 金叉买入
        signals[(short_ma > long_ma) & (short_ma.shift(1) <= long_ma.shift(1))] = 1
        
        # 死叉卖出
        signals[(short_ma < long_ma) & (short_ma.shift(1) >= long_ma.shift(1))] = -1
        
        return signals
