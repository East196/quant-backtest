"""
回测引擎
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.strategy import BaseStrategy
from utils.indicators import SMA


class BacktestEngine:
    """
    回测引擎
    
    支持单股票和多股票回测，计算各种性能指标
    """
    
    def __init__(self, initial_capital: float = 100000, commission: float = 0.0003):
        """
        初始化回测引擎
        
        Args:
            initial_capital: 初始资金
            commission: 手续费率（默认0.03%）
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.strategies = []
        self.results = None
        
    def add_strategy(self, strategy: BaseStrategy):
        """
        添加策略
        
        Args:
            strategy: 策略实例
        """
        self.strategies.append(strategy)
        
    def run(self, data: pd.DataFrame, symbol: str = None) -> Dict:
        """
        运行回测
        
        Args:
            data: 价格数据，必须包含 'close' 列，可选 'open', 'high', 'low', 'volume'
            symbol: 股票代码（可选）
            
        Returns:
            回测结果字典
        """
        if not self.strategies:
            raise ValueError("请先添加策略！")
            
        # 准备数据
        data = data.copy()
        
        # 生成信号
        signals = pd.DataFrame(index=data.index)
        for strategy in self.strategies:
            signal = strategy.generate_signals(data)
            signals[strategy.name] = signal
            
        # 合并信号（取平均）
        combined_signal = signals.mean(axis=1)
        combined_signal = combined_signal.apply(lambda x: 1 if x > 0.5 else (-1 if x < -0.5 else 0))
        
        # 执行回测
        results = self._execute_backtest(data, combined_signal)
        
        # 计算性能指标
        metrics = self._calculate_metrics(results)
        
        self.results = {
            'data': data,
            'signals': combined_signal,
            'trades': results['trades'],
            'portfolio': results['portfolio'],
            'metrics': metrics,
            'symbol': symbol
        }
        
        return self.results
    
    def _execute_backtest(self, data: pd.DataFrame, signals: pd.Series) -> Dict:
        """
        执行回测逻辑
        
        Args:
            data: 价格数据
            signals: 交易信号
            
        Returns:
            回测结果
        """
        # 初始化
        cash = self.initial_capital
        position = 0  # 持仓数量
        portfolio_value = []
        trades = []
        
        # 遍历每一天
        for i in range(len(data)):
            date = data.index[i]
            close = data['close'].iloc[i]
            signal = signals.iloc[i]
            
            # 买入信号
            # 买入信号
            if signal == 1 and position == 0 and cash > 0:
                # 计算可买数量（考虑手续费）
                # 资金 = 数量 * 价格 * (1 + 手续费率)
                # 数量 = 资金 / (价格 * (1 + 手续费率))
                max_shares = cash / (close * (1 + self.commission))
                commission_fee = max_shares * close * self.commission
                cost = max_shares * close
                
                # 执行买入
                position = max_shares
                cash -= (cost + commission_fee)
                
                trades.append({
                    'date': date,
                    'type': 'BUY',
                    'price': close,
                    'shares': max_shares,
                    'cost': cost,
                    'commission': commission_fee,
                    'cash': cash
                })
                
            # 卖出信号
            elif signal == -1 and position > 0:
                # 计算卖出金额
                sell_amount = position * close
                commission_fee = sell_amount * self.commission
                
                # 执行卖出
                cash += (sell_amount - commission_fee)
                
                trades.append({
                    'date': date,
                    'type': 'SELL',
                    'price': close,
                    'shares': position,
                    'commission': commission_fee,
                    'cash': cash
                })
                
                position = 0
                
            # 记录组合价值
            total_value = cash + position * close
            portfolio_value.append({
                'date': date,
                'cash': cash,
                'position': position,
                'position_value': position * close,
                'total_value': total_value
            })
            
        # 转换为DataFrame
        portfolio_df = pd.DataFrame(portfolio_value)
        portfolio_df.set_index('date', inplace=True)
        
        return {
            'trades': trades,
            'portfolio': portfolio_df
        }
    
    def _calculate_metrics(self, results: Dict) -> Dict:
        """
        计算性能指标
        
        Args:
            results: 回测结果
            
        Returns:
            性能指标字典
        """
        portfolio = results['portfolio']
        trades = results['trades']
        
        # 总收益率
        total_return = (portfolio['total_value'].iloc[-1] / self.initial_capital - 1) * 100
        
        # 年化收益率（假设252个交易日）
        days = len(portfolio)
        annual_return = ((1 + total_return/100) ** (252/days) - 1) * 100 if days > 0 else 0
        
        # 最大回撤
        cumulative = portfolio['total_value']
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        
        # 夏普比率（假设无风险利率为3%）
        returns = portfolio['total_value'].pct_change().dropna()
        if len(returns) > 0 and returns.std() != 0:
            sharpe_ratio = (returns.mean() * 252 - 0.03) / (returns.std() * np.sqrt(252))
        else:
            sharpe_ratio = 0
            
        # 交易统计
        buy_trades = [t for t in trades if t['type'] == 'BUY']
        sell_trades = [t for t in trades if t['type'] == 'SELL']
        
        # 计算盈利交易（考虑手续费）
        profits = []
        for i in range(min(len(buy_trades), len(sell_trades))):
            buy_cost = buy_trades[i]['price'] * buy_trades[i]['shares']
            sell_revenue = sell_trades[i]['price'] * sell_trades[i]['shares']
            total_commission = buy_trades[i]['commission'] + sell_trades[i]['commission']
            profit = sell_revenue - buy_cost - total_commission
            profits.append(profit)
            
        win_trades = [p for p in profits if p > 0]
        lose_trades = [p for p in profits if p < 0]
        
        win_rate = (len(win_trades) / len(profits) * 100) if profits else 0
        avg_profit = np.mean(win_trades) if win_trades else 0
        avg_loss = np.mean(lose_trades) if lose_trades else 0
        profit_loss_ratio = abs(avg_profit / avg_loss) if avg_loss != 0 else 0
        
        return {
            'initial_capital': self.initial_capital,
            'final_value': portfolio['total_value'].iloc[-1],
            'total_return': total_return,
            'annual_return': annual_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'total_trades': len(trades),
            'win_rate': win_rate,
            'profit_loss_ratio': profit_loss_ratio,
            'avg_profit': avg_profit,
            'avg_loss': avg_loss
        }
    
    def print_summary(self):
        """打印回测摘要"""
        if not self.results:
            print("还没有运行回测！")
            return
            
        metrics = self.results['metrics']
        
        print("\n" + "="*60)
        print("回测结果摘要")
        print("="*60)
        print(f"股票代码: {self.results.get('symbol', 'N/A')}")
        print(f"策略: {', '.join([s.name for s in self.strategies])}")
        print("-"*60)
        print(f"初始资金: ¥{metrics['initial_capital']:,.2f}")
        print(f"最终价值: ¥{metrics['final_value']:,.2f}")
        print(f"总收益率: {metrics['total_return']:.2f}%")
        print(f"年化收益率: {metrics['annual_return']:.2f}%")
        print(f"最大回撤: {metrics['max_drawdown']:.2f}%")
        print(f"夏普比率: {metrics['sharpe_ratio']:.2f}")
        print("-"*60)
        print(f"总交易次数: {metrics['total_trades']}")
        print(f"胜率: {metrics['win_rate']:.2f}%")
        print(f"盈亏比: {metrics['profit_loss_ratio']:.2f}")
        print(f"平均盈利: ¥{metrics['avg_profit']:,.2f}")
        print(f"平均亏损: ¥{metrics['avg_loss']:,.2f}")
        print("="*60 + "\n")
