from typing import Literal, Union, List 

from enum import Enum

from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection

class FunctionTimeModelEnum(str, Enum):
    Constant = "Constant"
    Exponential = "Exponential"
    Normal = "Normal"
    Lognormal = "Lognormal"


class TimeModelEnum(str, Enum):              
    HistoryTimeModel = "HistoryTimeModel"
    FunctionTimeModel = "FunctionTimeModel"
    ManhattanDistanceTimeModel = "ManhattanDistanceTimeModel"


class HistoryTimeModelData(Submodel):
    type: Literal[TimeModelEnum.HistoryTimeModel]
    history: List[float]

    

class FunctionTimeModelData(Submodel):
    type: Literal[TimeModelEnum.FunctionTimeModel]
    distribution_function: Literal[
        FunctionTimeModelEnum.Constant,
        FunctionTimeModelEnum.Exponential,
        FunctionTimeModelEnum.Normal,
    ]
    parameters: List[float]
    batch_size: int = 100

    

class ManhattanDistanceTimeModelData(Submodel):
    type: Literal[TimeModelEnum.ManhattanDistanceTimeModel]
    speed: float
    reaction_time: float

   
TIME_MODEL_UNION= Union[HistoryTimeModelData, FunctionTimeModelData, ManhattanDistanceTimeModelData]