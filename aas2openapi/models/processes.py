from typing import Literal, Union, Optional, List

from enum import Enum

from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection
from aas2openapi.models.timemodel import TIME_MODEL_UNION



class ProcessTypeEnum(str, Enum):                
    ProductionProcesses = "ProductionProcesses"
    TransportProcesses = "TransportProcesses"
    CapabilityProcesses = "CapabilityProcesses"


class GeneralInfo(Submodel):
    #time_model_id: str
    type: ProcessTypeEnum  
    

class Capability (Submodel):
    capability: Optional[str]  

class ProcessAttributes(Submodel):
    process_attributes: Optional[str] 
    

class ProcessData(AAS):
    general_Info: GeneralInfo
    # time_model_id: TIME_MODEL_UNION
    capability: Capability
    process_attributes: ProcessAttributes










