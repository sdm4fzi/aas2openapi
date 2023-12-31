import typing
import aas2openapi
from aas2openapi.middleware import Middleware
from aas2openapi import models
from enum import Enum



class BillOfMaterialInfo(models.SubmodelElementCollection):
    manufacterer: str
    product_type: str


class BOM_Type(Enum):
    MBOM = "MBOM"
    EBOM = "EBOM"
    SBOM = "SBOM"

class BillOfMaterial(models.Submodel):
    components: typing.List[str]
    bill_of_material_info: BillOfMaterialInfo
    bom_type: BOM_Type

class ProcessModel(models.Submodel):
    processes: typing.List[str]


class Product(models.AAS):
    bill_of_material: BillOfMaterial
    process_model: typing.Optional[ProcessModel]


class Capability(models.Submodel):
    capability: str  
    empty: typing.Optional[typing.List[str]] = []
    empty_value: typing.Optional[str] = ""

    

class Process(models.AAS):
    capability: typing.Optional[Capability]


# Test the transformation capabilities of aas2openapi

example_product = Product(
    id="Product1",
    process_model=ProcessModel(
        id="PMP1",
        processes=["join", "screw"],
        semantic_id="PMP1_semantic_id",
    ),
    bill_of_material=BillOfMaterial(
        id="BOMP1", 
        components=["stator", "rotor", "coil", "bearing"],
        semantic_id="BOMP1_semantic_id",
        bill_of_material_info=BillOfMaterialInfo(
            id_short="BOMInfoP1",
            semantic_id="BOMInfoP1_semantic_id",
            manufacterer="Bosch", 
            product_type="A542", 
        ),
        bom_type="MBOM",
    ),
)

example_process = Process(
    id="Process1",
    capability=Capability(
        id="Capability1",
        capability="screw",
        semantic_id="Capability1_semantic_id",
    ),
)
obj_store = aas2openapi.convert_pydantic_model_to_aas(example_product)

import basyx.aas.adapter.json.json_serialization

with open("examples/simple_aas_and_submodels.json", "w", encoding="utf-8") as json_file:
    basyx.aas.adapter.json.write_aas_json_file(json_file, obj_store)


# Reverse transformation

data_model = aas2openapi.convert_object_store_to_pydantic_models(obj_store)

# Create the middleware and load the models
middleware = Middleware()

middleware.load_pydantic_models([Product])
# middleware.load_pydantic_model_instances([example_product, example_process])
# middleware.load_aas_objectstore(obj_store)
# middleware.load_json_models(file_path="examples/example_json_model.json")
middleware.generate_rest_api()
middleware.generate_graphql_api()
middleware.generate_model_registry_api()

app = middleware.app
#run with: uvicorn examples.minimal_example:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
