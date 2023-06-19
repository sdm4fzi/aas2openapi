from __future__ import annotations

from typing import Optional, List, Union

from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection



class subProductAttributes(SubmodelElementCollection):
    attribute: str     

class subProduct(SubmodelElementCollection):
    subProbductType: str
    subProductAAS: str
    status: str
    quantity: str
    subProductAttributes: Optional[List[SubmodelElementCollection]]
    
   
class MaterialData(Submodel):
    material_type: str
    processes: Union[List[str], str]
    transport_process: str

 
class BOM(Submodel):
    description: str
    assembly: Optional[str]
    subProductCount: Optional[str]
    subProduct: Optional[List[SubmodelElementCollection]]
    material_data: MaterialData    
    
class ProcessReference(Submodel):
    process_id: str
    process_type: str
    
    
class Product(AAS):
    description: str
    bom: BOM
    process_reference: ProcessReference 