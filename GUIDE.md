# 量化回测框架使用指南

## 快速开始

### 1. 安装依赖

```bash
cd ~/wsclaw/quant-backtest
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 运行示例

```bash
cd examples
python simple_backtest.py
```

### 3. 使用真实数据

如果你想使用真实数据，需要：
1. 下载股票数据（CSV格式）
2. 确保包含列：date, open, close, high, low, volume

```python
from core.data import DataManager

dm = DataManager()
data = dm.load_from_csv('600570.csv')
```

## 自定义策略

### 创建新策略

```python
from core.strategy import BaseStrategy
import pandas as pd

class MyStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="MyStrategy")
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        实现你的策略逻辑
        
        返回:
        - 1: 买入信号
        - -1: 卖出信号
        - 0: 持有/观望
        """
        signals = pd.Series(0, index=data.index)
        
        # 示例：价格突破20日高点买入
        high_20 = data['high'].rolling(20).max()
        signals[data['close'] > high_20.shift(1)] = 1
        
        # 价格跌破20日低点卖出
        low_20 = data['low'].rolling(20).min()
        signals[data['close'] < low_20.shift(1)] = -1
        
        return signals
```

### 使用自定义策略

```python
from core.engine import BacktestEngine

engine = BacktestEngine(initial_capital=100000)
engine.add_strategy(MyStrategy())

results = engine.run(data)
```

## 技术指标

框架内置了常用技术指标：

```python
from utils.indicators import SMA, EMA, MACD, RSI, BOLL, KDJ

# 均线
sma = SMA(data['close'], window=20)

# MACD
macd_data = MACD(data['close'])
# 返回: {'macd': MACD线, 'signal': 信号线, 'histogram': 柱状图}

# RSI
rsi = RSI(data['close'], window=14)

# 布林带
boll = BOLL(data['close'])
# 返回: {'upper': 上轨, 'middle': 中轨, 'lower': 下轨}
```

## 性能指标说明

- **总收益率**: 整个回测期间的收益百分比
- **年化收益率**: 按年计算的收益率（假设252个交易日）
- **最大回撤**: 从峰值到谷值的最大跌幅
- **夏普比率**: 风险调整后的收益（>1为良好，>2为优秀）
- **胜率**: 盈利交易占比
- **盈亏比**: 平均盈利/平均亏损

## 学习建议

### 第1周：理解框架
- 阅读核心代码
- 运行示例
- 理解回测逻辑

### 第2周：学习指标
- 研究技术指标计算
- 理解指标含义
- 尝试组合指标

### 第3周：编写策略
- 实现简单策略（均线、MACD）
- 回测并分析结果
- 调整参数优化

### 第4周：进阶应用
- 组合多个策略
- 风险管理
- 编写完整交易系统

## 注意事项

⚠️ **重要提示**:
1. 本框架仅供学习使用
2. 模拟数据不能代表真实市场
3. 历史表现不代表未来收益
4. 实盘前务必充分测试
5. 注意交易成本和滑点

## 常见问题

### Q: 如何获取真实数据？
A: 可以使用akshare、tushare等库，或者从券商软件导出CSV

### Q: 回测结果为什么和实际不同？
A: 可能原因：
- 滑点（买卖价格差异）
- 交易限制（涨跌停、停牌）
- 数据质量问题
- 未来函数（使用了未来数据）

### Q: 如何优化策略？
A: 建议：
- 避免过度拟合
- 使用样本外数据测试
- 考虑交易成本
- 注意风险控制

## 下一步

1. 尝试运行示例代码
2. 加载真实股票数据
3. 编写自己的策略
4. 分析回测结果
5. 不断优化改进

祝学习愉快！📈
