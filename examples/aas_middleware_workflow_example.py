import typing
from aas2openapi import models

from aas_middleware.core import Connector


class BillOfMaterialInfo(models.SubmodelElementCollection):
    manufacterer: str
    product_type: str


class BillOfMaterial(models.Submodel):
    components: typing.List[str]
    bill_of_material_info: BillOfMaterialInfo


class ProcessModel(models.Submodel):
    processes: typing.List[str]


class Product(models.AAS):
    bill_of_material: BillOfMaterial
    process_model: typing.Optional[ProcessModel]


class SimPlanProduct(models.AAS):
    bill_of_material: BillOfMaterial
    process_model: typing.Optional[ProcessModel]


class ProductMapper:
    def map(self, data: Product) -> SimPlanProduct:
        return SimPlanProduct(**data.dict())


from aas_middleware.connectors import http_request_connector, http_polling_connector

## Creating connectors for the data sources -> here two web services with rest APIs
mes__simple_connector = http_polling_connector.HttpRequestConnector(
    url="http://localhost:8080/mes/products"
)
simplan_connector = http_request_connector.HttpRequestConnector(
    url="http://localhost:8080/simplan/products"
)

from aas_middleware.providers import base_provider
from aas_middleware.consumers import consumers

mes_provider = base_provider.Provider(
    connector=mes__simple_connector, data_model=Product
)
simplan_consumer = consumers.Consumer(
    connector=simplan_connector, data_model=SimPlanProduct
)


async def digital_twin_workflow(
    mes_provider: base_provider.Provider[Connector, Product],
    simplan_consumer: consumers.Consumer[Connector, SimPlanProduct],
):
    mes_data = await mes_provider.execute()
    simplan_data = ProductMapper().map(mes_data)
    await simplan_consumer.execute(data=simplan_data)

import anyio

anyio.run(digital_twin_workflow, mes_provider, simplan_consumer)
# now image, we to connect to mes by polling, so that data is only received if a value changes and we want to it cyclically
    
mes_polling_connector = http_polling_connector.HttpPollingConnector(
    url="http://localhost:8080/mes/products",
    interval=1
)
mes_provider = base_provider.Provider(
    connector=mes_polling_connector, data_model=Product
)

# now we can use the same workflow as before

async def digital_twin_workflowe(
    mes_provider: base_provider.Provider[Connector, Product],
    simplan_consumer: consumers.Consumer[Connector, SimPlanProduct],
):
    while True:
        mes_data = await mes_provider.execute()
        simplan_data = ProductMapper().map(mes_data)
        await simplan_consumer.execute(data=simplan_data)


# NSince we only specific, that a connector is used in the function, we can change the connector easily:
# Lets change simplans consumer connector to a websocket server running at simplan.
        
from aas_middleware.connectors import web_socket_server_connector

simplan_websocket_connector = web_socket_server_connector.WebSocketServerConnector(
    host="localhost",
    port=8080,
)
anyio.run(simplan_websocket_connector.connect())

simplan_consumer_websocket = consumers.Consumer(
    connector=simplan_websocket_connector, data_model=SimPlanProduct
)

# now we can use the same workflow as before with the new consumer

anyio.run(digital_twin_workflow, mes_provider, simplan_consumer_websocket)