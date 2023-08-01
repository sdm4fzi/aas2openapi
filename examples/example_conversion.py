import json
from urllib import parse

from basyx.aas import model
import basyx.aas.adapter.json.json_serialization

from typing import List

import aas2openapi
from aas2openapi.convert.convert_pydantic import ClientModel
from examples.models import product



example_smc = product.subProduct(
    id_="SMC_example",
    id_short="a",
    semantic_id="http://www.google.de/1",
    description="xyz",
    subProbductType="a",
    subProductAAS="b",
    status="c",
    quantity="5",
    subProductAttributes=None,
)

example_material = product.ProductData(
    id_="Material_example",
    description="y",
    product_type="A",
    processes="B",
    transport_process="C",
    id_short="b",
    semantic_id="http://www.google.de23",
)

example_bom = product.BOM(
    id_="Example_Bom_Submodel",
    description="this is an example",
    assembly="assembly",
    subProduct=[example_smc],
    subProductCount="http://193.196.37.23:4001/aasServer/shells/AAS_caesar_id/aas",
    id_short="cd",
    semantic_id="http://www.google.de3",
)

example_process_reference = product.ProcessReference(
    id_="example_process_reference",
    description="this is an example",
    process_id="2",
    process_type="3",
    id_short="d",
    semantic_id="http://www.google.de4",
)


example_product = product.Product(
    id_="Example_Product",
    description="456",
    bom=example_bom,
    process_reference=example_process_reference,
    product_data=example_material,
    id_short="e",
)
with open("examples/example_model_instance.json", "w", encoding="utf-8") as json_file:
    json.dump({"products": [example_product.dict()]}, json_file, indent=4)

obj_store = aas2openapi.convert_pydantic_model_to_aas(example_product)

# print(obj_store)

with open("examples/generated_aas_and_submodels_from_models.json", "w", encoding="utf-8") as json_file:
    basyx.aas.adapter.json.write_aas_json_file(json_file, obj_store)


aas: model.AssetAdministrationShell = obj_store.get("Example_Product")
aas_for_client = ClientModel(basyx_object=aas)

from ba_syx_aas_repository_client import Client
from ba_syx_aas_repository_client.types import Response, Unset

client = Client("http://localhost:8081")


from ba_syx_aas_repository_client.api.asset_administration_shell_repository_api import (
    post_asset_administration_shell,
    get_all_asset_administration_shells,
    get_asset_administration_shell_by_id,
)

my_data = aas_for_client

print(my_data.to_dict())

import asyncio

response = asyncio.run(
    post_asset_administration_shell.asyncio_detailed(client=client, json_body=my_data)
)
data = asyncio.run(get_all_asset_administration_shells.asyncio(client=client))

print(data)

from aas2openapi.util import client_utils

base64_str = client_utils.get_base64_from_string(example_product.id_)

data = asyncio.run(get_asset_administration_shell_by_id.asyncio(aas_identifier=base64_str, client=client))

print("retrieved aas:", data)



submodels = []
for item in obj_store:
    item = obj_store.get(item.id)
    if isinstance(item, model.Submodel):
        submodels.append(ClientModel(basyx_object=item))


from ba_syx_submodel_repository_client import Client

client = Client("http://localhost:8082")

from ba_syx_submodel_repository_client.api.submodel_repository_api import (
    post_submodel
    
)
import pprint
for submodel in submodels:
    response = asyncio.run(
        post_submodel.asyncio(client=client, json_body=submodel)
    )
    print("Added submodel", submodel.basyx_object.id_short, "to repository")
