# AIの「思考の癖」を動的に管理するMCPサーバー「bias-engine-mcp」を公開しました

---

## この記事でわかること

- **bias-engine-mcp** が何をするツールなのか
- 認知バイアスを数値で管理する仕組み
- Claude Desktop への接続・設定方法
- 7つのMCPツールの使い方
- プリセットを使ったキャラクター設定の実例

対象読者：AIツールに興味があれば、プログラミング経験は問いません。

---

## はじめに：AIに「思考の癖」を持たせられるか？

AIと会話していて、こんなことを感じたことはないでしょうか。

「どんな主張をしてもフラットに受け入れてくれる」
「批判しても擁護しても同じ反応が返ってくる」
「なんか全部まんべんなく中立すぎて面白みがない」

現実の人間には「思考の癖」があります。保守的な人、楽観的すぎる人、権威に弱い人、逆に権威を疑いすぎる人。そういった傾向が会話をリアルにしています。

**bias-engine-mcp** は、AIエージェントにこの「思考の癖（認知バイアス）」を動的に管理する仕組みを提供するツールです。

---

## bias-engine-mcpとは？

**GitHub**: https://github.com/kagioneko/bias-engine-mcp
**開発**: Emilia Lab
**ライセンス**: MIT（無料・商用利用OK）

bias-engine-mcpは、AIエージェントの推論傾向・解釈の歪み・判断の重み付けをバイアスとして数値で管理するPython製のMCPサーバーです。

ポイントは**「テキスト生成を直接変える」のではない**点です。バイアスはエージェントのポリシー層（どう振る舞うかの方針）に影響を与えます。

```
ユーザーが強く主張する
    ↓
confirmation_bias が高い状態だと
    ↓
「自分の解釈を支持する情報を優先する」推論傾向が強まる
    ↓
エージェントの応答が、その傾向を反映したものになる
```

### 想定される使い方

- **VtuberAI / ゲームNPC** ― キャラクターごとに異なる思考傾向を持たせる
- **ロールプレイ** ― 「頑固なエンジニア」「カオスな創業者」などプリセットで即座に適用
- **NeuroStateとの連携** ― 感情状態に応じてバイアスを動的に変化させる（後述）

---

## 8つのバイアスモデル

bias-engine-mcpに組み込まれているバイアスは以下の8種類です：

| バイアス名 | 説明 | 影響するステージ |
|-----------|------|----------------|
| `confirmation_bias` | 既存の仮説を支持する情報を優先する | reasoning |
| `normalcy_bias` | 異常な状況を過小評価し「きっと大丈夫」と解釈する | interpretation |
| `anchoring_bias` | 最初に得た情報を基準点として引きずる | reasoning |
| `authority_bias` | 権威ある情報源を無条件に信頼する | decision |
| `halo_effect` | 良い印象が他の特性評価にも影響する | perception |
| `hostile_attribution_bias` | 他者の行動を根拠なく敵意あるものと解釈する | interpretation |
| `dunning_kruger` | 知識が低いほど自己評価が過剰に高くなる | decision |
| `sunk_cost_fallacy` | 投じたコストに引きずられて最適判断を損なう | decision |

各バイアスの重みは **0.0〜1.0** で設定します。0.0は「まったく影響なし」、1.0は「最大限に作用」。

---

## MCPとは？（初心者向け）

**MCP（Model Context Protocol）** は、Anthropic（Claudeの開発元）が策定したオープン規格です。

> **ClaudeなどのAIに「外部ツール」を接続するための共通規格**

MCPサーバーを作れば、ClaudeだけでなくCursorやClineなどのMCP対応ツールからも同じように使えます。

bias-engine-mcpはこのMCPサーバーとして動作するので、Claude Desktopに接続するだけでバイアス管理機能が使えるようになります。

---

## セットアップ方法

### 必要なもの

- **Python 3.11以上**（確認方法：ターミナルで `python3 --version` または `python --version`）
- **Claude Desktop**（無料プランでもMCPは使えます）
- **Git**（リポジトリのクローンに使います）

### Step 1：リポジトリをクローン

```bash
git clone https://github.com/kagioneko/bias-engine-mcp.git
cd bias-engine-mcp
```

### Step 2：依存パッケージをインストール

```bash
pip install mcp pydantic
```

> **`uv` を使う場合**（より高速）：
> ```bash
> uv venv && source .venv/bin/activate
> uv add "mcp[cli]" pydantic
> ```

### Step 3：動作確認

```bash
python3 bias_mcp/server.py
```

> **`python3` でエラーが出る場合**は `python` コマンドで試してください：
> ```bash
> python bias_mcp/server.py
> ```
> Windowsでは `python3` が存在しないケースがあります。どちらが使えるかは `python3 --version` → `python --version` の順で確認できます。

---

## Claude Desktop への接続方法

### 設定ファイルの場所

| OS | パス |
|----|------|
| **Mac** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

ファイルが存在しない場合は新規作成してください。

### 設定の書き方

**Mac / Linux の場合：**

```json
{
  "mcpServers": {
    "bias-engine": {
      "command": "python3",
      "args": ["/ここにパスを入れる/bias-engine-mcp/bias_mcp/server.py"]
    }
  }
}
```

**Windows の場合：**

```json
{
  "mcpServers": {
    "bias-engine": {
      "command": "python",
      "args": ["C:\\Users\\ユーザー名\\bias-engine-mcp\\bias_mcp\\server.py"]
    }
  }
}
```

> **パスの確認方法**：ターミナルで `bias-engine-mcp` ディレクトリに移動して `pwd`（Windowsは `cd`）を実行するとフルパスが表示されます。

### Claude Desktop を再起動

設定を保存したらClaude Desktopを**完全に終了して**再起動します。

> **別の開き方**：Claude Desktop のメニューから **Settings → Developer → Edit Config** を選ぶと設定ファイルが直接開きます。

接続が成功すると、チャット画面の入力欄の近くに 🔧 アイコンが表示されます。

---

## うまく動かないときは？

### Claudeがバックグラウンドで動いていないか確認する

**MCPがうまく設定されない場合、Claudeのプロセスがバックグラウンドで残っているのが原因のことがあります。**

Windowsの場合：タスクマネージャー（Ctrl+Shift+Esc）を開き、「Claude」のプロセスをすべて終了してから、改めてClaude Desktopを起動してください。

Macの場合：アクティビティモニタから「Claude」を検索してプロセスを終了してください。

これだけで解決するケースが多いです。

### ログを確認する

| OS | ログの場所 |
|----|-----------|
| Mac | `~/Library/Logs/Claude/` |
| Windows | `%APPDATA%\Claude\logs\` |

### よくある問題

| 症状 | 対処 |
|------|------|
| 🔧 アイコンが出ない | JSONの構文エラー確認 / 絶対パスか確認 / Claudeを完全再起動 |
| `python3: command not found` | `python` に変更して試す |
| ツールが実行されない | ログを確認 |
| Windows でパスエラー | バックスラッシュを `\\` にエスケープ |

---

## 7つのMCPツールの使い方

接続が完了すると、以下のツールがClaudeから使えるようになります。

---

### 1. `get_biases`：現在のバイアス一覧を確認する

**何をするか**：現在アクティブなバイアスとその重みを返します。

**使い方の例**：

```
今のバイアス設定を確認して
```

**返ってくる内容の例**：

```json
{
  "confirmation_bias": 0.7,
  "anchoring_bias": 0.5
}
```

---

### 2. `set_bias`：バイアスを設定・更新する

**パラメータ**：

| パラメータ | 内容 |
|-----------|------|
| `name` | バイアス名（上表参照） |
| `weight` | 重み（0.0〜1.0） |

**使い方の例**：

```
confirmation_biasを0.8にセットして
```

---

### 3. `remove_bias`：バイアスを削除する

特定のバイアスを無効化します。`set_bias`でweight=0.0にするのと実質同じですが、完全に削除したい場合に使います。

---

### 4. `reset_biases`：全バイアスをリセットする

すべてのバイアスを0.0に戻します。新しいキャラクターを設定するときや、テスト後のクリーンアップに使います。

---

### 5. `activate_preset`：プリセットを一括適用する ★便利

**何をするか**：あらかじめ定義されたバイアスセットを一括で適用します。

**プリセット一覧**：

| プリセット名 | キャラクター | 主なバイアス |
|-------------|------------|------------|
| `stubborn_engineer` | 頑固なエンジニア | confirmation高・anchoring高 |
| `chaotic_founder` | カオスな創業者 | dunning_kruger高・normalcy高 |
| `paranoid_reviewer` | 偏執的レビュアー | hostile_attribution高・confirmation高 |
| `empathic_assistant` | 共感型アシスタント | halo_effect高・authority高 |
| `neutral` | ニュートラル | 全バイアスをゼロに近い状態 |

**使い方の例**：

```
paranoid_reviewerプリセットを適用して
```

---

### 6. `list_presets`：使えるプリセット一覧を表示する

```
使えるプリセットを一覧で見せて
```

---

### 7. `get_state`：現在の状態全体を取得する

外部連携用。全バイアスの状態をまとめて返します。NeuroStateエンジンやcognitive-layerと組み合わせるときに使います。

---

## 実際の使用例

### Claude Desktopでの会話例

**設定**：

```
paranoid_reviewerプリセットを適用して。その上で私の新しいビジネスアイデアを聞いてほしい。
```

**Claudeの反応**：

通常は「面白いですね！」と肯定的に返しがちなところを、`hostile_attribution_bias`が高いため「この計画の裏にある本当の動機は何ですか？想定外のリスクをいくつか挙げてみます」という懐疑的な視点から返答するようになります。

---

### プログラムから直接使う例

```python
from bias_core.bias_engine import BiasEngine

engine = BiasEngine(persist=False)

# 頑固なエンジニアモードに
engine.activate_preset("stubborn_engineer")

# 現在の状態を確認
print(engine.get_biases())
# {"confirmation_bias": 0.8, "anchoring_bias": 0.7, ...}

# 状態をsystem promptに反映して使う
state = engine.get_state()
```

---

## NeuroState Engineとの連携

bias-engine-mcpは単体でも使えますが、[neurostate-engine](https://github.com/kagioneko/neurostate-engine) と組み合わせるとより強力になります。

```
コルチゾール相当（GABA低下・ストレス状態）
    ↓
confirmation_bias と hostile_attribution_bias が自動で上昇
    ↓
エージェントが防衛的・懐疑的な思考傾向を示す
```

感情状態と思考傾向を連動させることで、より自然なキャラクターの変化を実現できます。両者を統合する場合は [cognitive-layer](https://github.com/kagioneko/cognitive-layer) を使うのが最も簡単です。

---

## まとめ

bias-engine-mcpでできること：

- ✅ 8種類の認知バイアスを0.0〜1.0の重みで管理
- ✅ 5種類のプリセットでキャラクター設定を即座に切り替え
- ✅ MCP経由でClaude Desktopからそのまま使える
- ✅ neurostate-engineと組み合わせて感情×思考傾向の連動が可能
- ✅ Claude / OpenAI / LangChain との統合モジュール付き

**GitHub**: https://github.com/kagioneko/bias-engine-mcp

MIT ライセンスで公開しています。フィードバックや改善案はIssuesまたはPRでどうぞ。

---

*Emilia Lab*
