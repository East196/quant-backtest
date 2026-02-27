# Quant Backtest - 量化回测框架

一个简单实用的Python量化回测框架，适合量化入门学习。

## 特性

- ✅ 简单易用的API
- ✅ 支持自定义策略
- ✅ 内置常用技术指标
- ✅ 完整的性能分析
- ✅ 可视化回测结果
- ✅ 支持多股票回测

## 安装

```bash
cd ~/wsclaw/quant-backtest
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 快速开始

```python
from core.engine import BacktestEngine
from strategies.ma_cross import MACrossStrategy

# 创建回测引擎
engine = BacktestEngine(initial_capital=100000)

# 添加策略
engine.add_strategy(MACrossStrategy(short_window=5, long_window=20))

# 运行回测
results = engine.run(symbols=['600570'])

# 查看结果
print(results['metrics'])

# 绘制图表
engine.plot_results()
```

## 目录结构

```
quant-backtest/
├── core/              # 核心模块
│   ├── engine.py      # 回测引擎
│   ├── strategy.py    # 策略基类
│   └── data.py        # 数据管理
├── strategies/        # 策略库
│   ├── ma_cross.py    # 均线交叉
│   └── macd.py        # MACD策略
├── utils/             # 工具
│   ├── indicators.py  # 技术指标
│   └── plot.py        # 可视化
├── examples/          # 示例
├── data/              # 数据存储
└── README.md
```

## 自定义策略

```python
from core.strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def generate_signals(self, data):
        # 在这里实现你的策略逻辑
        # 返回: 1 (买入), -1 (卖出), 0 (持有)
        pass
```

## 性能指标

- 总收益率
- 年化收益率
- 最大回撤
- 夏普比率
- 胜率
- 盈亏比

## 学习路线

1. **第1周**：理解回测框架结构
2. **第2周**：学习技术指标
3. **第3周**：编写简单策略
4. **第4周**：优化和组合策略

## 注意事项

⚠️ 本框架仅供学习使用，不构成投资建议
⚠️ 历史表现不代表未来收益
⚠️ 请在充分理解后谨慎实盘

## License

MIT
