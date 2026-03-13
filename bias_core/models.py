"""Bias Engine MCP - データモデル定義"""

from typing import Literal
from pydantic import BaseModel, Field, field_validator

BiasTarget = Literal["perception", "interpretation", "reasoning", "decision", "expression"]


class Bias(BaseModel):
    """認知バイアスモデル"""
    name: str
    weight: float = Field(ge=0.0, le=1.0)
    target: BiasTarget
    description: str = ""

    @field_validator("weight")
    @classmethod
    def clamp_weight(cls, v: float) -> float:
        return max(0.0, min(1.0, v))


class BiasState(BaseModel):
    """アクティブなバイアスの状態スナップショット"""
    biases: dict[str, float]  # name -> weight


class SetBiasRequest(BaseModel):
    name: str
    weight: float = Field(ge=0.0, le=1.0)


class ActivatePresetRequest(BaseModel):
    name: str
