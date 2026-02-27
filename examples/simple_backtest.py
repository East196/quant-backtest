"""
简单回测示例
演示如何使用回测框架
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import BacktestEngine
from core.data import DataManager
from strategies.ma_cross import MACrossStrategy
from strategies.macd import MACDStrategy
from utils.plot import BacktestPlotter


def main():
    print("="*60)
    print("量化回测框架 - 示例（真实数据）")
    print("="*60)
    
    # 1. 准备数据
    print("\n步骤1: 准备数据...")
    data_manager = DataManager()
    
    # 获取真实数据
    data = data_manager.get_data(symbol='600570', use_real=True)
    print(f"数据形状: {data.shape}")
    print(f"日期范围: {data.index[0]} 至 {data.index[-1]}")
    print(f"最新收盘价: ¥{data['close'].iloc[-1]:.2f}")
    
    # 2. 创建回测引擎
    print("\n步骤2: 创建回测引擎...")
    engine = BacktestEngine(initial_capital=100000, commission=0.0003)
    
    # 3. 添加策略
    print("\n步骤3: 添加策略...")
    engine.add_strategy(MACrossStrategy(short_window=5, long_window=20))
    # 也可以添加多个策略
    # engine.add_strategy(MACDStrategy())
    
    # 4. 运行回测
    print("\n步骤4: 运行回测...")
    results = engine.run(data, symbol='600570')
    
    # 5. 查看结果
    print("\n步骤5: 查看结果...")
    engine.print_summary()
    
    # 6. 绘制图表
    print("\n步骤6: 绘制图表...")
    plotter = BacktestPlotter()
    plotter.plot_results(results)
    
    print("\n✅ 回测完成！")


if __name__ == "__main__":
    main()
