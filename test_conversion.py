import json
from urllib import parse

from basyx.aas import model
import basyx.aas.adapter.json.json_serialization

from typing import List

import aas2openapi
from aas2openapi.models import product


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

example_material = product.MaterialData(
    id_="1",
    description="y",
    material_type="A",
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
    id_="Example_Process_Reference",
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
    material_data=example_material,
    id_short="e",
)

obj_store = aas2openapi.convert_pydantic_model_to_aas(example_product)

print(obj_store)

with open("data.json", "w", encoding="utf-8") as json_file:
    basyx.aas.adapter.json.write_aas_json_file(json_file, obj_store)
