"""
MACD策略
"""
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.strategy import BaseStrategy
from utils.indicators import MACD


class MACDStrategy(BaseStrategy):
    """
    MACD策略
    
    当MACD线上穿信号线时买入
    当MACD线下穿信号线时卖出
    """
    
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9):
        """
        初始化策略
        
        Args:
            fast: 快线周期
            slow: 慢线周期
            signal: 信号线周期
        """
        super().__init__(
            name=f"MACD_{fast}_{slow}_{signal}",
            fast=fast,
            slow=slow,
            signal=signal
        )
        
        self.fast = fast
        self.slow = slow
        self.signal = signal
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        生成交易信号
        
        Args:
            data: 价格数据
            
        Returns:
            信号序列
        """
        # 计算MACD
        macd_data = MACD(data['close'], self.fast, self.slow, self.signal)
        macd_line = macd_data['macd']
        signal_line = macd_data['signal']
        
        # 生成信号
        signals = pd.Series(0, index=data.index)
        
        # 金叉买入
        signals[(macd_line > signal_line) & (macd_line.shift(1) <= signal_line.shift(1))] = 1
        
        # 死叉卖出
        signals[(macd_line < signal_line) & (macd_line.shift(1) >= signal_line.shift(1))] = -1
        
        return signals
