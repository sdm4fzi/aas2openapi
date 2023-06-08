from typing import Literal, Union, Optional, List

from enum import Enum

from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection
from aas2openapi.models.timemodel import TIME_MODEL_UNION


class ProcessAttributes(Submodel):
    attribute: str
    
class Execution(Submodel):
    execution: str
    
class Time_Model(Submodel):
    time_model_id: TIME_MODEL_UNION
    
class Resource_Links(Submodel):
    resource_links: str
    
class Procedure(AAS):
    process_attributes: ProcessAttributes
    execution: Execution
    time_model: Time_Model
    resource_links: Resource_Links