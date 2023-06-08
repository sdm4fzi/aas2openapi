from typing import List, Optional, Tuple, Literal, Union

from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection



class GeneralInformation(Submodel):
    location: Tuple[float, float] # (10, 5) -> conversion to string
    capacity: int
    process_capacity: Optional[List[int]]
    process_ids: List[str]

class ControlLogic(Submodel):
    controller: Literal["SimpleController", "TransportController"] # conversion to string
    control_policy: Literal["FIFO", "SPT_transport", "LIFO", "SPT"]

class ResourceQueues(Submodel):
    input_queues: Optional[List[str]]
    output_queues: Optional[List[str]]
    

class QueueData(AAS):
    capacity: Union[int, float] = 0.0
    
class SinkData(AAS):
    location: Tuple[float, float]
    material_type: str
    input_queues: List[str]
    
    
    
class ResourceHierarchy(Submodel):
    resource_data: Optional[List[str]]
    resource_hierarchy: Optional[List[str]]
    resource_links: Optional[List[str]]
    resource_ids: Optional[List[str]]
    resource_type: Optional[str]
    
class Capabilities(Submodel):
    capability: Optional[List[str]]
    
class ResourceStates(Submodel):
    state_ids: Optional[List[str]]

class Layout(Submodel):
    layout: Optional[List[str]]
    
class Resource(AAS):
    general_information: GeneralInformation
    control_logic: ControlLogic
    queues: ResourceQueues
    resource_hierarchy: ResourceHierarchy
    capabilities: Capabilities
    states: ResourceStates
    layout: Layout
   


