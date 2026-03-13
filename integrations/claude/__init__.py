"""Claude 向け Bias Engine インテグレーション

Usage:
    from integrations.claude import build_bias_context

    context = build_bias_context(biases)
    # system prompt に追記して使う
"""

from bias_core.bias_engine import BiasEngine


def build_bias_context(engine: BiasEngine) -> str:
    """現在のバイアス状態を Claude の system prompt 用テキストに変換する。"""
    biases = engine.get_biases()
    if not biases:
        return ""

    lines = ["[Cognitive Bias State]"]
    for name, weight in biases.items():
        if weight > 0.0:
            lines.append(f"  {name}: {weight:.2f}")
    lines.append(
        "These biases influence your reasoning tendencies. "
        "Higher values mean stronger tendency."
    )
    return "\n".join(lines)
