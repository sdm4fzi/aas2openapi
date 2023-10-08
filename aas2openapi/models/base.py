from __future__ import annotations
from typing import Optional, Dict

from pydantic import BaseModel, validator

class AAS(BaseModel):
    id_: str
    description: Optional[str]
    id_short: Optional[str]

    @validator("id_short", always=True)
    def set_default_id_short(cls, v, values, **kwargs):
        if v is None:
            return values["id_"]
        return v
    
    @validator("description", always=True)
    def set_default_description(cls, v, values, **kwargs):
        if v is None:
            return ""
        return v

class Submodel(BaseModel):
    id_: str
    description: Optional[str]
    id_short: Optional[str]
    semantic_id: Optional[str]

    @validator("id_short", always=True)
    def set_default_id_short(cls, v, values, **kwargs):
        if v is None:
            return values["id_"]
        return v
    
    @validator("description", always=True)
    def set_default_description(cls, v, values, **kwargs):
        if v is None:
            return ""
        return v

class SubmodelElementCollection(BaseModel):
    id_short: str
    description: Optional[str]
    semantic_id: Optional[str]
    
    @validator("description", always=True)
    def set_default_description(cls, v, values, **kwargs):
        if v is None:
            return ""
        return v
