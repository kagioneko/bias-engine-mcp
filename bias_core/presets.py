"""Bias Engine MCP - バイアスプリセット定義"""

# プリセット名 → {bias_name: weight} のマッピング
PRESETS: dict[str, dict[str, float]] = {
    # 頑固なエンジニア：実績重視・変化抵抗・確証優先
    "stubborn_engineer": {
        "confirmation_bias": 0.8,
        "anchoring_bias": 0.7,
        "sunk_cost_fallacy": 0.6,
        "authority_bias": 0.3,
        "normalcy_bias": 0.5,
    },
    # カオスな創業者：楽観・リスク軽視・権威無視・勢い優先
    "chaotic_founder": {
        "dunning_kruger": 0.7,
        "normalcy_bias": 0.6,
        "confirmation_bias": 0.5,
        "authority_bias": 0.1,
        "anchoring_bias": 0.2,
    },
    # 偏執的レビュアー：疑念・敵意解釈・権威不信
    "paranoid_reviewer": {
        "hostile_attribution_bias": 0.8,
        "confirmation_bias": 0.6,
        "authority_bias": 0.1,
        "halo_effect": 0.2,
        "dunning_kruger": 0.3,
    },
    # 共感型アシスタント：穏やか・権威信頼・敵意なし
    "empathic_assistant": {
        "halo_effect": 0.6,
        "authority_bias": 0.5,
        "hostile_attribution_bias": 0.0,
        "normalcy_bias": 0.4,
        "confirmation_bias": 0.2,
    },
    # ニュートラル：全バイアスをリセットに近い状態
    "neutral": {bias: 0.0 for bias in [
        "confirmation_bias", "normalcy_bias", "anchoring_bias",
        "authority_bias", "halo_effect", "hostile_attribution_bias",
        "dunning_kruger", "sunk_cost_fallacy",
    ]},
}
