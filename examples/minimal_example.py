import typing
import aas2openapi
from aas2openapi.middleware import Middleware
from aas2openapi import models

# Create some examplary models that should be used in the middleware


class BillOfMaterial(models.Submodel):
    components: typing.List[str]


class ProcessModel(models.Submodel):
    processes: typing.List[str]


class Product(models.AAS):
    bill_of_material: BillOfMaterial
    process_model: typing.Optional[ProcessModel]


# Test the transformation capabilities of aas2openapi

example_product = Product(
    id_="bc2119e48d0",
    process_model=ProcessModel(
        id_="a8cd10ed",
        processes=["join", "screw"],
    ),
    bill_of_material=BillOfMaterial(
        id_="a7cba3bcd", components=["stator", "rotor", "coil", "bearing"]
    ),
)
obj_store = aas2openapi.convert_pydantic_model_to_aas(example_product)

import basyx.aas.adapter.json.json_serialization

with open("examples/simple_aas_and_submodels.json", "w", encoding="utf-8") as json_file:
    basyx.aas.adapter.json.write_aas_json_file(json_file, obj_store)


# Reverse transformation

data_model = aas2openapi.convert_object_store_to_pydantic_models(obj_store)
print(data_model)

# Create the middleware and load the models

middleware = Middleware()
# middleware.load_pydantic_models([Product])
middleware.load_pydantic_model_instances([example_product])
# middleware.load_aas_from_objectstore(obj_store) # graphQL not yet working
middleware.generate_rest_api()
middleware.generate_graphql_api()

app = middleware.app

import uvicorn

uvicorn.run(app)
