"""Bias Engine - 基本デモ

python3 examples/basic/demo.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from bias_core.bias_engine import BiasEngine

engine = BiasEngine(persist=False)

print("=== Bias Engine デモ ===\n")

# 単体バイアス設定
engine.set_bias("confirmation_bias", 0.7)
engine.set_bias("anchoring_bias", 0.5)
print("手動設定後:")
for name, weight in engine.get_biases().items():
    print(f"  {name}: {weight:.2f}")

print()

# プリセット適用
engine.reset_biases()
engine.activate_preset("paranoid_reviewer")
print("paranoid_reviewer プリセット適用後:")
for name, weight in engine.get_biases().items():
    print(f"  {name}: {weight:.2f}")

print()

# バイアス削除
engine.remove_bias("authority_bias")
print("authority_bias 削除後:")
for name, weight in engine.get_biases().items():
    print(f"  {name}: {weight:.2f}")
