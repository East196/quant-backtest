# 5分钟快速开始

## 最快上手方式

```bash
# 1. 进入目录
cd ~/wsclaw/quant-backtest

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 运行示例
python examples/simple_backtest.py
```

## 你的第一个策略

创建文件 `my_first_strategy.py`:

```python
import sys
sys.path.insert(0, '.')

from core.engine import BacktestEngine
from core.data import DataManager
from strategies.ma_cross import MACrossStrategy

# 1. 准备数据
dm = DataManager()
data = dm.generate_sample_data('600570', days=200)

# 2. 创建回测引擎（10万初始资金）
engine = BacktestEngine(initial_capital=100000)

# 3. 添加策略（5日均线上穿20日均线）
engine.add_strategy(MACrossStrategy(short_window=5, long_window=20))

# 4. 运行回测
results = engine.run(data, symbol='600570')

# 5. 查看结果
engine.print_summary()
```

运行：
```bash
python my_first_strategy.py
```

## 修改参数测试

```python
# 尝试不同的均线组合
engine.add_strategy(MACrossStrategy(short_window=10, long_window=30))
```

## 下一步

1. 阅读 [GUIDE.md](GUIDE.md) - 详细使用指南
2. 阅读 [30_DAY_PLAN.md](30_DAY_PLAN.md) - 30天学习计划
3. 修改示例代码 - 实践出真知
