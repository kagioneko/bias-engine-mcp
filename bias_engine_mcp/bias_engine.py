"""Bias Engine MCP - コアエンジン（バイアス状態管理）"""

import json
import logging
from pathlib import Path

from bias_engine_mcp.models import Bias, BiasState
from bias_engine_mcp.bias_registry import BIAS_CATALOG
from bias_engine_mcp.presets import PRESETS

logger = logging.getLogger(__name__)

PERSISTENCE_PATH = Path("bias_state.json")


class BiasEngine:
    """認知バイアスの登録・重み管理・スタッキングを担う中核エンジン"""

    def __init__(self, persist: bool = True) -> None:
        # name → Bias（現在アクティブなバイアスセット）
        self._biases: dict[str, Bias] = {}
        self._persist = persist
        if persist and PERSISTENCE_PATH.exists():
            self._load()

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def get_biases(self) -> dict[str, float]:
        """アクティブなバイアスと重みを返す"""
        return {name: bias.weight for name, bias in self._biases.items()}

    def set_bias(self, name: str, weight: float) -> Bias:
        """バイアスをセット（未登録なら自動登録）。weightはclamp済み。"""
        weight = max(0.0, min(1.0, weight))

        if name in self._biases:
            # 既存バイアスの weight だけ更新（イミュータブルパターン）
            existing = self._biases[name]
            updated = existing.model_copy(update={"weight": weight})
            self._biases = {**self._biases, name: updated}
        elif name in BIAS_CATALOG:
            # カタログから雛形を取得して weight を適用
            template = BIAS_CATALOG[name]
            new_bias = template.model_copy(update={"weight": weight})
            self._biases = {**self._biases, name: new_bias}
        else:
            # 未知のバイアスはカスタム登録（target=reasoningをデフォルト）
            new_bias = Bias(name=name, weight=weight, target="reasoning")
            self._biases = {**self._biases, name: new_bias}
            logger.info("カスタムバイアスを登録しました: %s", name)

        self._save()
        return self._biases[name]

    def remove_bias(self, name: str) -> bool:
        """バイアスを削除。存在すればTrue、なければFalse。"""
        if name not in self._biases:
            return False
        self._biases = {k: v for k, v in self._biases.items() if k != name}
        self._save()
        return True

    def reset_biases(self) -> None:
        """全バイアスをクリア"""
        self._biases = {}
        self._save()

    def activate_preset(self, preset_name: str) -> dict[str, float]:
        """
        プリセットを適用する。
        既存のバイアスはリセットされず、プリセットの値で上書き/追加される。
        """
        if preset_name not in PRESETS:
            raise ValueError(f"プリセット '{preset_name}' は存在しません。利用可能: {list(PRESETS)}")
        for name, weight in PRESETS[preset_name].items():
            self.set_bias(name, weight)
        logger.info("プリセット適用: %s", preset_name)
        return self.get_biases()

    def get_state(self) -> BiasState:
        return BiasState(biases=self.get_biases())

    def available_presets(self) -> list[str]:
        return list(PRESETS)

    # ------------------------------------------------------------------ #
    # Persistence
    # ------------------------------------------------------------------ #

    def _save(self) -> None:
        if not self._persist:
            return
        data = {
            name: {
                "weight": b.weight,
                "target": b.target,
                "description": b.description,
            }
            for name, b in self._biases.items()
        }
        PERSISTENCE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def _load(self) -> None:
        try:
            raw = json.loads(PERSISTENCE_PATH.read_text())
            loaded: dict[str, Bias] = {}
            for name, attrs in raw.items():
                loaded[name] = Bias(name=name, **attrs)
            self._biases = loaded
            logger.info("バイアス状態をファイルから復元しました (%d 件)", len(self._biases))
        except Exception as e:
            logger.warning("バイアス状態の読み込みに失敗しました: %s", e)
            self._biases = {}
