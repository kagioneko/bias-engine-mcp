# bias-engine-mcp

AIエージェントの認知バイアスを動的に管理するエンジン。

バイアスをスタック・重み付けし、エージェントの推論傾向・解釈の歪み・判断の重み付けを制御します。[NeuroState Engine](https://github.com/kagioneko/neurostate-engine) と連動し、内部状態に応じてバイアスを動的調整できます。

## これは何をするもの？

「AIを意図的に偏らせる」ツールではありません。

エージェントが**人間らしい一貫した思考傾向**を持つための仕組みです。

```
ユーザーが強く主張する
    ↓
confirmation_bias が高い状態だと
    ↓
「自分の解釈を支持する情報を優先する」推論傾向が強まる
    ↓
エージェントの応答が、その傾向を反映したものになる
```

バイアスが**テキスト生成を直接変える**のではありません。エージェントの**ポリシー層に影響を与える**のが役割です。

**向いている用途:**
- Vtuber AI（キャラクターごとに異なる思考傾向を持たせる）
- ゲームNPC（状況に応じて判断傾向が変わる）
- NeuroState と組み合わせた認知レイヤー構築

## インストール

```bash
pip install mcp pydantic
```

## クイックスタート

```python
from core.bias_engine import BiasEngine

engine = BiasEngine(persist=False)

# バイアスを設定
engine.set_bias("confirmation_bias", 0.7)
engine.set_bias("anchoring_bias", 0.5)

# 現在の状態を確認
print(engine.get_biases())
# {"confirmation_bias": 0.7, "anchoring_bias": 0.5}

# プリセットを適用
engine.activate_preset("paranoid_reviewer")
```

## MCP サーバー

```bash
python3 bias_mcp/server.py
```

提供ツール:

| ツール | 説明 |
|--------|------|
| `get_biases` | アクティブなバイアスと重み一覧 |
| `set_bias` | バイアスをセット/更新 |
| `remove_bias` | バイアスを削除 |
| `reset_biases` | 全バイアスをリセット |
| `activate_preset` | プリセットを適用 |
| `list_presets` | 利用可能なプリセット一覧 |
| `get_state` | 現在の状態全体（外部連携用） |

### Claude Desktop での設定例

```json
{
  "mcpServers": {
    "bias-engine": {
      "command": "python3",
      "args": ["/path/to/bias-engine-mcp/bias_mcp/server.py"]
    }
  }
}
```

## バイアスモデル

各バイアスは以下のフィールドを持ちます:

| フィールド | 説明 |
|-----------|------|
| `name` | バイアス識別子 |
| `weight` | 強度（0.0〜1.0） |
| `target` | 影響するステージ |
| `description` | 人間向け説明 |

### バイアスターゲット

| target | 影響するステージ |
|--------|----------------|
| `perception` | 知覚・情報の取り込み |
| `interpretation` | 解釈・意味付け |
| `reasoning` | 推論・論理展開 |
| `decision` | 判断・選択 |
| `expression` | 表現・出力 |

## 組み込みバイアス

| バイアス名 | 説明 |
|-----------|------|
| `confirmation_bias` | 確証バイアス — 既存の仮説を支持する情報を優先 |
| `normalcy_bias` | 正常性バイアス — 異常を過小評価 |
| `anchoring_bias` | アンカリング — 最初の情報に引きずられる |
| `authority_bias` | 権威バイアス — 権威ある情報源を過信 |
| `halo_effect` | ハロー効果 — 一部の印象が全体評価を歪める |
| `hostile_attribution_bias` | 敵意帰属バイアス — 他者の行動を敵意と解釈 |
| `dunning_kruger` | ダニング＝クルーガー効果 — 低能力ほど過信 |
| `sunk_cost_fallacy` | サンクコスト誤謬 — 埋没コストに引きずられる |

## プリセット

| プリセット名 | 特性 |
|------------|------|
| `stubborn_engineer` | 頑固なエンジニア（確証・固執・埋没コスト重視） |
| `chaotic_founder` | カオスな創業者（楽観・リスク軽視・勢い優先） |
| `paranoid_reviewer` | 偏執的レビュアー（疑念・敵意解釈・権威不信） |
| `empathic_assistant` | 共感型アシスタント（穏やか・信頼・敵意なし） |
| `neutral` | ニュートラル（全バイアスをゼロに近い状態） |

## 統合モジュール

- `integrations/claude/` — Claude system prompt への注入
- `integrations/openai/` — OpenAI system message ビルダー
- `integrations/langchain/` — LangChain 連携（予定）

## デモ

```bash
python3 examples/basic/demo.py
```

## NeuroState との連動

[NeuroState Engine](https://github.com/kagioneko/neurostate-engine) と組み合わせることで、内部状態に応じてバイアスが動的に変化します。

詳細は [cognitive-layer](https://github.com/kagioneko/cognitive-layer) を参照。

## ライセンス

MIT
