from __future__ import annotations
from typing import Optional

from enum import Enum

from pydantic import dataclasses
from pydantic import AnyUrl

@dataclasses.dataclass
class AAS:
    type: str = "AssetAdministrationShell"
    id_: str
    description: str
    id_short: Optional[str]

@dataclasses.dataclass
class Submodel:
    type: str = "Submodel"
    id_: str
    description: str
    id_short: Optional[str]
    semantic_id: Optional[AnyUrl]

@dataclasses.dataclass
class SubmodelElementCollection:
    type: str = "SubmodelElementCollection"
    id_: str
    description: str
    id_short: Optional[str]
    semantic_id: Optional[AnyUrl]

@dataclasses.dataclass
class SubmodelElementList:
    type: str = "SubmodelElementList"
    id_: str
    description: str
    id_short: Optional[str]
    semantic_id: Optional[AnyUrl]
    semantic_id_list_element: Optional[AnyUrl]
    
    

