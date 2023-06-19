from __future__ import annotations

from typing import Optional, List, Union
from pydantic.dataclasses import dataclass

from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection

@dataclass
class subProductAttributes(SubmodelElementCollection):
    attribute: str     

@dataclass
class subProduct(SubmodelElementCollection):
    subProbductType: str
    subProductAAS: str
    status: str
    quantity: str
    subProductAttributes: Optional[List[SubmodelElementCollection]]


@dataclass
class MaterialData(Submodel):
    material_type: str
    processes: Union[List[str], str]
    transport_process: str

@dataclass
class BOM(Submodel):
    description: str
    assembly: Optional[str]
    subProductCount: Optional[str]
    subProduct: Optional[List[SubmodelElementCollection]]
    material_data: MaterialData    


@dataclass  
class ProcessReference(Submodel):
    process_id: str
    process_type: str
    
@dataclass
class Product(AAS):
    bom: BOM
    process_reference: ProcessReference

