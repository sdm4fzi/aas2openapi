from typing import List, Optional, Tuple, Literal, Union

from enum import Enum

from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection





class KPIEnum(str, Enum):
    OUTPUT = "output"
    THROUGHPUT = "throughput"
    COST = "cost"
    WIP = "WIP"

    TRHOUGHPUT_TIME = "throughput_time"
    PROCESSING_TIME = "processing_time"

    PRODUCTIVE_TIME = "productive_time"
    STANDBY_TIME = "standby_time"
    SETUP_TIME = "setup_time"
    UNSCHEDULED_DOWNTIME = "unscheduled_downtime"

    DYNAMIC_WIP = "dynamic_WIP"
    DYNAMIC_THROUGHPUT_TIME = "dynamic_throughput_time"


class KPILevelEnum(str, Enum):
    SYSTEM = "system"
    RESOURCE = "resource"
    ALL_MATERIALS = "all_materials"
    MATERIAL_TYPE = "material_type"
    MATERIAL = "material"
    PROCESS = "process"


class KPI(SubmodelElementCollection):
    name: KPIEnum
    target: Literal["min", "max"]
    weight: Optional[float] = 1
    value: Optional[float] = None
    context: Tuple[KPILevelEnum, ...] = None
    resource: Optional[str] = None
    material_type: Optional[str] = None

class DynamicKPI(KPI):
    start_time: float
    end_time: float
    material: Optional[str] = None
    process: Optional[str] = None


class Output(KPI):
    name: Literal[KPIEnum.OUTPUT]
    target: Literal["max"] = "max"



class Throughput(KPI):
    name: Literal[KPIEnum.THROUGHPUT]
    target: Literal["max"] = "max"

   

class Cost(KPI):
    name: Literal[KPIEnum.COST]
    target: Literal["min"] = "min"

  


class WIP(KPI):
    name: Literal[KPIEnum.WIP]
    target: Literal["min"] = "min"


class DynamicWIP(DynamicKPI, WIP):
    name: Literal[KPIEnum.DYNAMIC_WIP]



class ThroughputTime(KPI):
    name: Literal[KPIEnum.TRHOUGHPUT_TIME]
    target: Literal["min"] = "min"

 

class DynamicThroughputTime(DynamicKPI, ThroughputTime):
    name: Literal[KPIEnum.DYNAMIC_THROUGHPUT_TIME]



class ProcessingTime(KPI):
    name: Literal[KPIEnum.PROCESSING_TIME]
    target: Literal["min"] = "min"



class ProductiveTime(KPI):
    name: Literal[KPIEnum.PRODUCTIVE_TIME]
    target: Literal["max"] = "max"

   

class StandbyTime(KPI):
    name: Literal[KPIEnum.STANDBY_TIME]
    target: Literal["min"] = "min"

   

class SetupTime(KPI):
    name: Literal[KPIEnum.SETUP_TIME]
    target: Literal["min"] = "min"

  

class UnscheduledDowntime(KPI):
    name: Literal[KPIEnum.UNSCHEDULED_DOWNTIME]
    target: Literal["min"] = "min"


KPI_UNION = Union[
    Output,
    Throughput,
    Cost,
    WIP,
    ThroughputTime,
    ProcessingTime,
    ProductiveTime,
    StandbyTime,
    SetupTime,
    UnscheduledDowntime,
    DynamicWIP,
    DynamicThroughputTime,
]

  
 
class Event(AAS):
    time: float
    resource: str
    state: str
    # state_type: state.StateTypeEnum
    state_type: str
    # activity: state.StateEnum
    activity: str
    material: Optional[str] = None
    expected_end_time: Optional[float] = None
    target_location: Optional[str] = None




class StaticPerformanceSM(Submodel):
    kpis: List[KPI_UNION]

class DynamicPerformanceSM(Submodel):
    event_log: List[Event]

class Performance(AAS):
    static_performance: StaticPerformanceSM
    dynamic_performance: DynamicPerformanceSM
    generalInfo: KPI
    dynamic_kpi: DynamicKPI

# class KPI(AAS):
#     kpi_enum: KPIEnum
#     kpi_level_enum: KPILevelEnum
    
#     generalInfo: KPI

#     dynamic_kpi: DynamicKPI
#     output: Output
#     throughput: Throughput
#     cost: Cost
#     wip: WIP
#     throughput_time: ThroughputTime
#     processing_time: ProcessingTime
#     productive_time: ProductiveTime
#     stanby_time: StandbyTime
#     steup_time: SetupTime
#     down_time: UnscheduledDowntime
#     dynamic_wip: DynamicWIP
#     dynamic_throughput_time: DynamicThroughputTime
    
#     event: Event
#     performance: Performance

