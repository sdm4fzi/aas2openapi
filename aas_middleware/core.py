from typing import Any, Protocol, Optional
from aas2openapi.models import base

class Mapper(Protocol):
    def map(self, data: base.Identifiable) -> base.Identifiable:
        ...

class Connector(Protocol):
    async def connect(self):
        ...

    async def disconnect(self):
        ...

    async def send(self, body: str) -> Optional[str]:
        ...

    async def receive(self) -> str:
        ...

class Actor(Protocol):
    async def set_connector(self, connector: Connector):
        ...

    async def get_connector(self) -> Connector: 
        ...

    async def set_model(self, model: Any):
        ...

    async def get_model(self) -> Any:
        ...


class Provider(Actor, Protocol):
    async def execute(self) -> base.Identifiable:
        ...

    
class Consumer(Actor, Protocol):
    async def execute(self, data: base.Identifiable):
        ...


class Processor(Actor, Protocol):
    async def execue(self, data: base.Identifiable) -> base.Identifiable:
        ...


class Persistence(Actor, Protocol):
    async def save(self, data: base.Identifiable):
        ...

    async def load(self) -> base.Identifiable:
        ...

    async def delete(self):
        ...

class WorkFlow(Protocol):
    async def execute(self):
        ...
