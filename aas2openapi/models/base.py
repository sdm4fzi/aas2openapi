from __future__ import annotations
from typing import Optional

from pydantic import BaseModel


class AAS(BaseModel):
    type: str = "AssetAdministrationShell"
    ID: str
    description: str


class Submodel(BaseModel):
    type: str = "Submodel"
    ID: str
    description: str
    semanticID: Optional[str]    #URI statt str?

    
class SubmodelElementCollection(BaseModel):
    type: str = "SubmodelElementCollection"
    ID: str
    description: str
    semanticID: Optional[str]     #URI?
    
    

