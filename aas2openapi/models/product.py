from __future__ import annotations

from typing import Optional, List, Union
from pydantic.dataclasses import dataclass

from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection

class subProductAttributes(SubmodelElementCollection):
    attribute: str     

class subProduct(SubmodelElementCollection):
    subProbductType: str
    subProductAAS: str
    status: str
    quantity: str
    subProductAttributes: Optional[List[SubmodelElementCollection]]


class ProductData(Submodel):
    product_type: str
    processes: Union[List[str], str]
    transport_process: str

class BOM(Submodel):
    assembly: Optional[str]
    subProductCount: Optional[str]
    subProduct: Optional[List[SubmodelElementCollection]]


class ProcessReference(Submodel):
    process_id: str
    process_type: str
    
class Product(AAS):
    bom: BOM
    process_reference: ProcessReference
    product_data: ProductData    


