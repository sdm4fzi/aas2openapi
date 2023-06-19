from __future__ import annotations
from typing import Optional

from enum import Enum

from pydantic.dataclasses import dataclass
from pydantic import AnyUrl

@dataclass
class AAS:
    id_: str
    description: str
    id_short: Optional[str]

@dataclass
class Submodel:
    id_: str
    description: str
    id_short: Optional[str]
    semantic_id: Optional[str]

@dataclass
class SubmodelElementCollection:
    id_: str
    description: str
    id_short: Optional[str]
    semantic_id: Optional[str]
