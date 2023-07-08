from __future__ import annotations
from typing import Optional, Dict

from enum import Enum

from pydantic.dataclasses import dataclass
from pydantic import BaseModel

class AAS(BaseModel):
    id_: str
    description: str
    id_short: Optional[str]

class Submodel(BaseModel):
    id_: str
    description: str
    id_short: Optional[str]
    semantic_id: Optional[str]

class SubmodelElementCollection(BaseModel):
    description: str
    id_short: Optional[str]
    semantic_id: Optional[str]
