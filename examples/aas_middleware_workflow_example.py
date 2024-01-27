import typing
from aas2openapi import models, middleware
from aas_middleware import core

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

mes_provider = base_provider.ConnectorProvider(
    connector=mes__simple_connector, data_model=Product
)
simplan_consumer = consumers.Consumer(
    connector=simplan_connector, data_model=SimPlanProduct
)


# TODO: add functionality with decorators to easily load providers and consumers, name of the workflow object will be the name
# of the function (digital_twin_workflow) and the execute function will inject the values from the decorator into or
# the workflow_function will be called in the execute function of the workflow object and the parameters are provided
# the function. 
# providers and consumers are added as instance variables to the workflow object (e.g. in dict)

def retrieve_arguments_decorator(actor: core.Provider[models.AAS]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Extract specified arguments from the function
            retrieved_args = {name: value for name, value in zip(arg_names, args)}
            # Add them to kwargs to maintain compatibility with the original function
            kwargs.update(retrieved_args)
            
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


# @workflow(mes_provider, simplan_consumer, on_start_up=True, delay_rate=10000)
@retrieve_arguments_decorator(mes_provider)
async def digital_twin_workflow(
    mes_provider: base_provider.ConnectorProvider[Product],
    simplan_consumer: consumers.Consumer[Connector, SimPlanProduct],
):
    mes_data = await mes_provider.execute()
    simplan_data = ProductMapper().map(mes_data)
    await simplan_consumer.execute(data=simplan_data)

mware = middleware.Middleware()
mware.add(digital_twin_workflow)
# mware.run()
# now image, we to connect to mes by polling, so that data is only received if a value changes and we want to it cyclically
    
mes_polling_connector = http_polling_connector.HttpPollingConnector(
    url="http://localhost:8080/mes/products",
    interval=1
)
mes_provider = base_provider.ConnectorProvider(
    connector=mes_polling_connector, data_model=Product
)

# now we can use the same workflow as before
@Workflow(mes_provider, simplan_consumer, on_start_up=True, delay_rate=10000)
async def digital_twin_workflow2(
    mes_provider: base_provider.ConnectorProvider[Product],
    simplan_consumer: consumers.Consumer[Connector, SimPlanProduct],
):
    while True:
        mes_data = await mes_provider.execute()
        simplan_data = ProductMapper().map(mes_data)
        await simplan_consumer.execute(data=simplan_data)


mware.add(digital_twin_workflow2)



# NSince we only specific, that a connector is used in the function, we can change the connector easily:
# Lets change simplans consumer connector to a websocket server running at simplan.
        
from aas_middleware.connectors import web_socket_server_connector

simplan_websocket_connector = web_socket_server_connector.WebSocketServerConnector(
    host="localhost",
    port=8080,
)

workflow = mware.get_workflow("digital_twin_workflow2")
workflow.set_connector(simplan_websocket_connector)
mware.run()


# now we can use the same workflow as before with the new consumer

