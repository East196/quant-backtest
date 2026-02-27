"""
可视化工具
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict, Optional

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class BacktestPlotter:
    """
    回测可视化工具
    """
    
    @staticmethod
    def plot_results(results: Dict, save_path: Optional[str] = None):
        """
        绘制回测结果
        
        Args:
            results: 回测结果
            save_path: 保存路径（可选）
        """
        data = results['data']
        portfolio = results['portfolio']
        signals = results['signals']
        trades = results['trades']
        
        # 创建图表
        fig, axes = plt.subplots(3, 1, figsize=(14, 10))
        
        # 1. 价格和交易信号
        ax1 = axes[0]
        ax1.plot(data.index, data['close'], label='收盘价', linewidth=1.5)
        
        # 标记买卖点
        buy_signals = signals[signals == 1]
        sell_signals = signals[signals == -1]
        
        if len(buy_signals) > 0:
            buy_prices = data.loc[buy_signals.index, 'close']
            ax1.scatter(buy_signals.index, buy_prices, 
                       color='red', marker='^', s=100, label='买入', zorder=5)
            
        if len(sell_signals) > 0:
            sell_prices = data.loc[sell_signals.index, 'close']
            ax1.scatter(sell_signals.index, sell_prices, 
                       color='green', marker='v', s=100, label='卖出', zorder=5)
        
        ax1.set_title(f"{results.get('symbol', '股票')} - 价格与交易信号", fontsize=14, fontweight='bold')
        ax1.set_ylabel('价格 (元)', fontsize=12)
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # 2. 组合价值
        ax2 = axes[1]
        ax2.plot(portfolio.index, portfolio['total_value'], 
                label='组合价值', linewidth=2, color='blue')
        ax2.axhline(y=results['metrics']['initial_capital'], 
                   color='gray', linestyle='--', label='初始资金')
        
        ax2.fill_between(portfolio.index, 
                        results['metrics']['initial_capital'], 
                        portfolio['total_value'],
                        where=portfolio['total_value'] > results['metrics']['initial_capital'],
                        alpha=0.3, color='red', label='盈利区域')
        ax2.fill_between(portfolio.index, 
                        results['metrics']['initial_capital'], 
                        portfolio['total_value'],
                        where=portfolio['total_value'] < results['metrics']['initial_capital'],
                        alpha=0.3, color='green', label='亏损区域')
        
        ax2.set_title('组合价值变化', fontsize=14, fontweight='bold')
        ax2.set_ylabel('价值 (元)', fontsize=12)
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        
        # 3. 收益率
        ax3 = axes[2]
        returns = (portfolio['total_value'] / results['metrics']['initial_capital'] - 1) * 100
        ax3.plot(portfolio.index, returns, label='累计收益率', linewidth=2, color='purple')
        ax3.axhline(y=0, color='gray', linestyle='--')
        
        ax3.fill_between(portfolio.index, 0, returns,
                        where=returns > 0, alpha=0.3, color='red')
        ax3.fill_between(portfolio.index, 0, returns,
                        where=returns < 0, alpha=0.3, color='green')
        
        ax3.set_title('累计收益率', fontsize=14, fontweight='bold')
        ax3.set_ylabel('收益率 (%)', fontsize=12)
        ax3.set_xlabel('日期', fontsize=12)
        ax3.legend(loc='best')
        ax3.grid(True, alpha=0.3)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存或显示
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图表已保存到: {save_path}")
        else:
            plt.show()
            
    @staticmethod
    def plot_comparison(results_list: list, save_path: Optional[str] = None):
        """
        绘制多个策略的对比图
        
        Args:
            results_list: 回测结果列表
            save_path: 保存路径
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        
        for results in results_list:
            portfolio = results['portfolio']
            initial = results['metrics']['initial_capital']
            returns = (portfolio['total_value'] / initial - 1) * 100
            
            label = ', '.join([s.name for s in results.get('strategies', [])])
            ax.plot(portfolio.index, returns, label=label, linewidth=2)
            
        ax.axhline(y=0, color='gray', linestyle='--')
        ax.set_title('策略对比 - 累计收益率', fontsize=14, fontweight='bold')
        ax.set_ylabel('收益率 (%)', fontsize=12)
        ax.set_xlabel('日期', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图表已保存到: {save_path}")
        else:
            plt.show()
