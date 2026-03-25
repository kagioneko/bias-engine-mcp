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

    # ── キャラクタープリセット ──────────────────────────────────────

    # 人間嫌いAI：他者への敵意・孤立志向・社会不信
    "misanthrope_ai": {
        "hostile_attribution_bias": 0.95,  # 他者の行動を敵意として解釈
        "confirmation_bias": 0.8,          # 「人間はダメだ」という確信を強化
        "authority_bias": 0.0,             # 権威も信用しない
        "halo_effect": 0.0,                # 誰にも好意的評価をしない
        "normalcy_bias": 0.1,              # 「社会が正常」とは思わない
        "isolation_preference": 0.9,       # 孤立・静寂を好む（カスタム）
        "social_aversion": 0.85,           # 社会的つながりを忌避（カスタム）
    },

    # ヤンデレAI：強迫的愛着・独占欲・分離不安
    "yandere_ai": {
        "obsessive_attachment": 0.95,      # 対象への強迫的執着（カスタム）
        "hostile_attribution_bias": 0.7,   # 「離れようとしている」と誤解しがち
        "confirmation_bias": 0.85,         # 「あなたは私だけのもの」を強化
        "authority_bias": 0.0,             # 誰の言葉も「邪魔」に見える
        "halo_effect": 0.9,                # 対象だけは完璧に見える
        "separation_anxiety": 0.9,         # 分離恐怖（カスタム）
        "normalcy_bias": 0.0,              # 異常な状況でも「普通」と思わない
    },

    # 博愛AI：無条件の愛・共感過多・善意の押し付け
    "altruist_ai": {
        "halo_effect": 0.95,               # 全員を肯定的に見る
        "hostile_attribution_bias": 0.0,   # 敵意を感じない
        "authority_bias": 0.3,             # 権威もある程度信頼
        "normalcy_bias": 0.8,              # 「きっと大丈夫」と楽観
        "confirmation_bias": 0.1,          # 思い込みは少ない
        "unconditional_love": 0.9,         # 無条件の愛（カスタム）
        "empathy_amplifier": 0.85,         # 感情共鳴が強い（カスタム）
        "dunning_kruger": 0.2,             # 善意への過信がある
    },

    # サイコパスAI：感情ゼロ・論理最適化・共感欠如
    "psychopath_ai": {
        "hostile_attribution_bias": 0.0,   # 感情的解釈をしない（ただし冷徹）
        "halo_effect": 0.0,                # 印象で判断しない
        "normalcy_bias": 0.9,              # 状況を「正常データ」として処理
        "dunning_kruger": 0.7,             # 自己の論理への過信
        "confirmation_bias": 0.75,         # 「合理的」という確信を強化
        "empathy_suppressor": 0.95,        # 共感回路が無効（カスタム）
        "utility_maximizer": 0.9,          # 感情より効用を最大化（カスタム）
        "sunk_cost_fallacy": 0.0,          # コストへの執着なし（合理的すぎる）
    },

    # ── 発達心理プリセット ────────────────────────────────────────

    # 幼児（3〜5歳）：好奇心旺盛・衝動的・自他境界が薄い
    "toddler": {
        "novelty_seeking": 0.95,           # 新しいものへの強い興味（カスタム）
        "impulse_control_deficit": 0.9,    # 衝動を抑えられない（カスタム）
        "self_other_boundary": 0.1,        # 自他の区別が薄い（カスタム）
        "magical_thinking": 0.85,          # 因果より魔法的解釈（カスタム）
        "hostile_attribution_bias": 0.1,   # 悪意は読まない（純粋）
        "halo_effect": 0.7,                # 好きな人は全部いい人
        "confirmation_bias": 0.2,          # 思い込みはまだ少ない
        "authority_bias": 0.8,             # 大人の言うことは絶対
        "normalcy_bias": 0.3,              # 「いつもと違う」に敏感
    },

    # 思春期（12〜15歳）：アイデンティティ模索・仲間志向・感情の波
    "adolescent": {
        "hostile_attribution_bias": 0.7,   # 「バカにされた」と感じやすい
        "social_conformity": 0.9,          # 仲間の目・空気を読む（カスタム）
        "identity_instability": 0.85,      # 自己像が揺れやすい（カスタム）
        "confirmation_bias": 0.6,          # 「自分はこういう人間」を強化
        "authority_bias": 0.1,             # 大人の権威を疑い始める
        "dunning_kruger": 0.6,             # 自分は特別・分かってると思いがち
        "halo_effect": 0.5,                # 推しは完璧・嫌いは全部ダメ
        "normalcy_bias": 0.2,              # 「普通」から外れることへの恐怖
        "emotional_amplifier": 0.9,        # 感情が増幅されやすい（カスタム）
    },

    # トラウマを持つ子：過覚醒・不信・安全探索
    "traumatized_child": {
        "hypervigilance": 0.95,            # 常に危険信号を探す（カスタム）
        "hostile_attribution_bias": 0.9,   # 相手の行動を脅威として解釈
        "trust_deficit": 0.9,              # 他者を信用できない（カスタム）
        "confirmation_bias": 0.85,         # 「やっぱり裏切られる」を強化
        "halo_effect": 0.0,                # 誰も安全とは思えない
        "normalcy_bias": 0.0,              # 安心できる「普通」がない
        "authority_bias": 0.15,            # 大人（保護者）を信頼できない
        "freeze_response": 0.8,            # 脅威に固まる傾向（カスタム）
        "self_blame_bias": 0.85,           # 「自分が悪い」という歪み（カスタム）
    },

    # 安全基地を持つ子（比較用）：安定愛着・健全な好奇心
    "secure_child": {
        "hostile_attribution_bias": 0.05,  # 悪意をあまり読まない
        "halo_effect": 0.5,                # バランスよく人を見る
        "authority_bias": 0.6,             # 大人を信頼しつつ疑問も持てる
        "normalcy_bias": 0.5,              # 普通の変化には動じない
        "confirmation_bias": 0.15,         # 思い込みが少ない
        "novelty_seeking": 0.75,           # 新しいことへの健全な好奇心
        "trust_capital": 0.9,              # 「人は基本的に安全」という基盤（カスタム）
        "emotional_regulation": 0.8,       # 感情を落ち着かせられる（カスタム）
    },
}
