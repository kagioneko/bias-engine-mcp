"""OpenAI 向け Bias Engine インテグレーション

Usage:
    from integrations.openai import build_system_message

    message = build_system_message(engine)
    # messages リストの先頭に追加して使う
"""

from bias_core.bias_engine import BiasEngine


def build_system_message(engine: BiasEngine) -> dict:
    """現在のバイアス状態を OpenAI system message 形式で返す。"""
    biases = engine.get_biases()
    active = {k: v for k, v in biases.items() if v > 0.0}

    if not active:
        return {"role": "system", "content": ""}

    lines = ["[Cognitive Bias State]"]
    for name, weight in active.items():
        lines.append(f"  {name}: {weight:.2f}")
    lines.append("These biases influence your reasoning tendencies.")

    return {"role": "system", "content": "\n".join(lines)}
