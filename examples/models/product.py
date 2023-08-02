from __future__ import annotations

from typing import Optional, List, Union

from aas2openapi.models import base

class subProductAttributes(base.SubmodelElementCollection):
    attribute: str     

class subProduct(base.SubmodelElementCollection):
    subProbductType: str
    subProductAAS: str
    status: str
    quantity: str
    subProductAttributes: Optional[List[base.SubmodelElementCollection]]

class ProductData(base.Submodel):
    product_type: str
    processes: Union[List[str], str]
    transport_process: str

class BOM(base.Submodel):
    assembly: Optional[str]
    subProductCount: Optional[str]
    subProduct: Optional[List[base.SubmodelElementCollection]]

class ProcessReference(base.Submodel):
    process_id: str
    process_type: str    

class Product(base.AAS):
    bom: BOM
    process_reference: ProcessReference
    product_data: Optional[ProductData]


