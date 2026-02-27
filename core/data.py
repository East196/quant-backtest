"""
数据管理模块
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional
import os


class DataManager:
    """
    数据管理器
    
    负责获取、存储和管理股票数据
    """
    
    def __init__(self, data_dir: str = None):
        """
        初始化数据管理器
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), '../data')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def generate_sample_data(self, symbol: str, days: int = 500) -> pd.DataFrame:
        """
        生成模拟数据（用于测试）
        
        Args:
            symbol: 股票代码
            days: 天数
            
        Returns:
            包含OHLCV数据的DataFrame
        """
        np.random.seed(42)
        
        # 生成日期
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # 生成价格（随机游走）
        returns = np.random.normal(0.001, 0.02, days)
        price = 50  # 初始价格
        prices = []
        
        for ret in returns:
            price *= (1 + ret)
            prices.append(price)
            
        # 生成OHLCV数据
        data = pd.DataFrame({
            'date': dates,
            'open': prices,
            'close': prices,
            'high': [p * (1 + np.random.uniform(0, 0.02)) for p in prices],
            'low': [p * (1 - np.random.uniform(0, 0.02)) for p in prices],
            'volume': np.random.randint(1000000, 10000000, days)
        })
        
        data.set_index('date', inplace=True)
        
        return data
    
    def load_from_csv(self, filepath: str) -> pd.DataFrame:
        """
        从CSV文件加载数据
        
        Args:
            filepath: CSV文件路径
            
        Returns:
            DataFrame
        """
        df = pd.read_csv(filepath)
        
        # 确保有日期列
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
        elif '日期' in df.columns:
            df['date'] = pd.to_datetime(df['日期'])
            df.set_index('date', inplace=True)
            
        return df
    
    def save_to_csv(self, data: pd.DataFrame, filename: str):
        """
        保存数据到CSV
        
        Args:
            data: 数据
            filename: 文件名
        """
        filepath = os.path.join(self.data_dir, filename)
        data.to_csv(filepath)
        print(f"数据已保存到: {filepath}")
