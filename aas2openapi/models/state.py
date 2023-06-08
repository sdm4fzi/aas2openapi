from typing import Literal, Union, List 

from enum import Enum

from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection


class StateTypeEnum(str, Enum):         
    BreakDownState = "BreakDownState"
    ProductionState = "ProductionState"
    TransportState = "TransportState"
    SetupState = "SetupState"
    ProcessBreakDownState = "ProcessBreakDownState"


   
# TODO: use smart inheritance and Submodel or SMC -> should be a SM / SMC of resources
class BreakDownStateData(Submodel):
    time_model_id: str
    type: Literal[StateTypeEnum.BreakDownState]
    repair_time_model_id: str

  

class ProcessBreakDownStateData(Submodel):
    time_model_id: str 
    type: Literal[StateTypeEnum.ProcessBreakDownState]
    repair_time_model_id: str
    process_id: str

   

class ProductionStateData(Submodel):
    time_model_id: str
    type: Literal[StateTypeEnum.ProductionState]

 

class TransportStateData(Submodel):
    time_model_id: str
    type: Literal[StateTypeEnum.TransportState]

  

class SetupStateData(Submodel):
    time_model_id: str
    type: Literal[StateTypeEnum.SetupState]
    origin_setup: str
    target_setup: str


# class StateData(AAS):
#     time_model_id: str
#     type: Literal[
#         StateTypeEnum.BreakDownState,
#         StateTypeEnum.ProductionState,
#         StateTypeEnum.TransportState,
#         StateTypeEnum.SetupState,
#     ]
#     state_type_enum: StateTypeEnum
#     breakdown_state: BreakDownStateData
#     production_state: ProductionStateData
#     transport_state: TransportStateData
#     steup_state: SetupStateData
#     processbreakdown_state: ProcessBreakDownStateData
    

