"""
Bias Engine MCP サーバー

認知バイアスの動的管理を提供する MCP サーバー。
Claude / LangChain / OpenAI などのエージェントから呼び出し可能。

使用方法:
    python3 bias_mcp/server.py
    または
    python -m bias_mcp.server

提供ツール:
    - get_biases        : アクティブなバイアス一覧と重みを取得
    - set_bias          : バイアスをセット/更新
    - remove_bias       : バイアスを削除
    - reset_biases      : 全バイアスをリセット
    - activate_preset   : プリセットを適用
    - list_presets      : 利用可能プリセット一覧
    - get_state         : 現在の状態全体（NeuroState連携用）
"""

import json
import sys
import os
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print(
        "ERROR: mcp パッケージが見つかりません。\n"
        "インストール: pip install mcp",
        file=sys.stderr,
    )
    sys.exit(1)

from bias_core.bias_engine import BiasEngine

# --- 状態ストア ---
engine = BiasEngine(persist=True)

TOOL_DEFINITIONS: list[Tool] = [
    Tool(
        name="get_biases",
        description="アクティブなバイアスと現在の重みを返します。",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="set_bias",
        description=(
            "バイアスをセットまたは更新します。未登録の名前は自動登録されます。"
            "weight は 0.0（無効）〜 1.0（最大）で指定します。"
        ),
        inputSchema={
            "type": "object",
            "required": ["name", "weight"],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "バイアス名（例: confirmation_bias）",
                },
                "weight": {
                    "type": "number",
                    "description": "重み（0.0〜1.0）",
                    "minimum": 0.0,
                    "maximum": 1.0,
                },
            },
        },
    ),
    Tool(
        name="remove_bias",
        description="指定したバイアスをアクティブセットから削除します。",
        inputSchema={
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "削除するバイアス名",
                }
            },
        },
    ),
    Tool(
        name="reset_biases",
        description="全バイアスをクリアしてリセットします。",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="activate_preset",
        description=(
            "バイアスプリセットを適用します。既存バイアスはリセットされず上書き/追加されます。\n"
            "利用可能プリセット:\n"
            "  stubborn_engineer  : 頑固なエンジニア（確証・固執・埋没コスト重視）\n"
            "  chaotic_founder    : カオスな創業者（楽観・リスク軽視・勢い優先）\n"
            "  paranoid_reviewer  : 偏執的レビュアー（疑念・敵意解釈・権威不信）\n"
            "  empathic_assistant : 共感型アシスタント（穏やか・信頼・敵意なし）\n"
            "  neutral            : ニュートラル（全バイアスをゼロに近い状態）"
        ),
        inputSchema={
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "プリセット名",
                    "enum": [
                        "stubborn_engineer",
                        "chaotic_founder",
                        "paranoid_reviewer",
                        "empathic_assistant",
                        "neutral",
                    ],
                }
            },
        },
    ),
    Tool(
        name="list_presets",
        description="利用可能なプリセット名の一覧を返します。",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="get_state",
        description="現在のバイアス状態をフルで返します（NeuroState 連携・外部システム連携用）。",
        inputSchema={"type": "object", "properties": {}},
    ),
]


# ------------------------------------------------------------------ #
# ハンドラー
# ------------------------------------------------------------------ #

def _handle_get_biases(_args: dict[str, Any]) -> list[TextContent]:
    result = engine.get_biases()
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


def _handle_set_bias(args: dict[str, Any]) -> list[TextContent]:
    name: str = args["name"]
    weight: float = float(args["weight"])
    bias = engine.set_bias(name, weight)
    result = {"name": bias.name, "weight": bias.weight, "target": bias.target, "description": bias.description}
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


def _handle_remove_bias(args: dict[str, Any]) -> list[TextContent]:
    name: str = args["name"]
    removed = engine.remove_bias(name)
    if not removed:
        result = {"error": f"バイアス '{name}' はアクティブではありません"}
    else:
        result = {"removed": True, "name": name}
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


def _handle_reset_biases(_args: dict[str, Any]) -> list[TextContent]:
    engine.reset_biases()
    return [TextContent(type="text", text=json.dumps({"status": "ok", "message": "全バイアスをリセットしました"}, ensure_ascii=False))]


def _handle_activate_preset(args: dict[str, Any]) -> list[TextContent]:
    name: str = args["name"]
    try:
        biases = engine.activate_preset(name)
        result = {"preset": name, "applied_biases": biases}
    except ValueError as e:
        result = {"error": str(e)}
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


def _handle_list_presets(_args: dict[str, Any]) -> list[TextContent]:
    return [TextContent(type="text", text=json.dumps(engine.available_presets(), ensure_ascii=False))]


def _handle_get_state(_args: dict[str, Any]) -> list[TextContent]:
    state = engine.get_state()
    return [TextContent(type="text", text=json.dumps(state.model_dump(), ensure_ascii=False, indent=2))]


# ------------------------------------------------------------------ #
# サーバー起動
# ------------------------------------------------------------------ #

async def run_server() -> None:
    """MCP サーバーを起動する。"""
    server = Server("bias-engine")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return TOOL_DEFINITIONS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        handlers = {
            "get_biases": _handle_get_biases,
            "set_bias": _handle_set_bias,
            "remove_bias": _handle_remove_bias,
            "reset_biases": _handle_reset_biases,
            "activate_preset": _handle_activate_preset,
            "list_presets": _handle_list_presets,
            "get_state": _handle_get_state,
        }
        if name not in handlers:
            raise ValueError(f"未知のツール: {name}")
        return handlers[name](arguments)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_server())
