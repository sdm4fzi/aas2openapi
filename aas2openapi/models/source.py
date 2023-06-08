from typing import List, Tuple

from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection

from enum import Enum


class RouterType(str, Enum):
    SimpleRouter = "SimpleRouter"
    CapabilityRouter = "CapabilityRouter"


class RoutingHeuristic(str, Enum):
    random = "random"
    shortest_queue = "shortest_queue"
    FIFO = "FIFO"
    
class GeneralInformation(Submodel) :
    location: Tuple[float, float]
    material_type: str
    time_model_id: str
    output_queues: List[str]


class SourceData(AAS):
    generalInformation: GeneralInformation
    router: RouterType
    routing_heuristic: RoutingHeuristic
    
