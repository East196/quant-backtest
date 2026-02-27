"""
策略基类
所有策略都继承此类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd


class BaseStrategy(ABC):
    """
    策略基类
    
    所有交易策略都应该继承这个类并实现 generate_signals 方法
    """
    
    def __init__(self, name: str = None, **kwargs):
        """
        初始化策略
        
        Args:
            name: 策略名称
            **kwargs: 策略参数
        """
        self.name = name or self.__class__.__name__
        self.params = kwargs
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        生成交易信号
        
        Args:
            data: 包含价格数据的DataFrame，至少包含 'close' 列
            
        Returns:
            信号Series: 1=买入, -1=卖出, 0=持有
        """
        pass
    
    def get_params(self) -> Dict[str, Any]:
        """获取策略参数"""
        return self.params
    
    def set_params(self, **kwargs):
        """设置策略参数"""
        self.params.update(kwargs)
        
    def __str__(self):
        return f"{self.name}({self.params})"
    
    def __repr__(self):
        return self.__str__()
