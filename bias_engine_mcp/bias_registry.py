"""Bias Engine MCP - 組み込みバイアス定義レジストリ"""

from bias_engine_mcp.models import Bias

# 初期実装に含める最低限のバイアスセット
DEFAULT_BIAS_DEFINITIONS: list[Bias] = [
    Bias(
        name="confirmation_bias",
        weight=0.0,
        target="reasoning",
        description="既存の仮説を支持する情報を優先する。矛盾する証拠を軽視しやすい。",
    ),
    Bias(
        name="normalcy_bias",
        weight=0.0,
        target="interpretation",
        description="異常な状況を過小評価し、「きっと大丈夫」と解釈しがちになる。",
    ),
    Bias(
        name="anchoring_bias",
        weight=0.0,
        target="reasoning",
        description="最初に得た情報を基準点として、その後の判断を過度に引きずる。",
    ),
    Bias(
        name="authority_bias",
        weight=0.0,
        target="decision",
        description="権威のある情報源・人物の意見を無条件に信頼しやすくなる。",
    ),
    Bias(
        name="halo_effect",
        weight=0.0,
        target="perception",
        description="ある特性が良い印象を与えると、他の特性も肯定的に評価してしまう。",
    ),
    Bias(
        name="hostile_attribution_bias",
        weight=0.0,
        target="interpretation",
        description="他者の行動を根拠なく敵意あるものとして解釈する。",
    ),
    Bias(
        name="dunning_kruger",
        weight=0.0,
        target="decision",
        description="知識・能力が低いほど自己評価が過剰に高くなる。自信過剰傾向。",
    ),
    Bias(
        name="sunk_cost_fallacy",
        weight=0.0,
        target="decision",
        description="すでに投じたコスト（時間・資金・労力）に引きずられて最適判断を損なう。",
    ),
]

# 名前 → Bias の辞書
BIAS_CATALOG: dict[str, Bias] = {b.name: b for b in DEFAULT_BIAS_DEFINITIONS}
