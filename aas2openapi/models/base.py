from __future__ import annotations
from typing import Optional

from pydantic import BaseModel
from pydantic import AnyUrl


class AAS(BaseModel):
    type: str = "AssetAdministrationShell"
    ID: str
    description: str


class Submodel(BaseModel):
    type: str = "Submodel"
    ID: str
    description: str
    semanticID: Optional[AnyUrl]

    
class SubmodelElementCollection(BaseModel):
    type: str = "SubmodelElementCollection"
    ID: str
    description: str
    semanticID: Optional[AnyUrl]


class SubmodelElementList(BaseModel):
    type: str = "SubmodelElementList"
    ID: str
    description: str
    semanticID: Optional[AnyUrl]
    
    

