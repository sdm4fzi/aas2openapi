from typing import TypeVar, Generic, Type
from aas_middleware.core import Connector
from aas2openapi.models import base

C = TypeVar("C", bound=Connector)
D = TypeVar("D", bound=base.Identifiable)

class Provider(Generic[C, D]):
    def __init__(self, connector: C, data_model: Type[D]) -> None:
        self.connector = connector
        self.data_model = data_model

    async def set_connector(self, connector: C):
        self.connector = connector

    async def get_connector(self) -> C:
        return self.connector
    
    async def set_model(self, model: Type[D]):
        self.data_model = model

    async def get_model(self) -> Type[D]:
        return self.data_model
    
    async def execute(self) -> D:
        response = await self.connector.receive()
        data_model_type = type(self.data_model)
        return data_model_type.parse_raw(response)
    

class MultiProvider:
    """
    Provider with multiple connectors to get data from.
    """
    pass