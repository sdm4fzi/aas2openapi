import json
from pydantic import parse_obj_as
from typing import Union

from aas2openapi.models import product, processes

all_types = Union[product.Product, processes.ProcessData]

def create_pydantic_model(model_definition):
    return parse_obj_as(all_types, model_definition)

with open("model.json") as file:
    models = json.load(file)


for model_definitions in models.values():
    models = []
    for model_definition in model_definitions:
        model = create_pydantic_model(model_definition)
        models.append(model)


### Now create the Middleware and load the models

from aas2openapi.middleware.middleware import Middleware

middleware = Middleware()
middleware.load_pydantic_model_instances(models)
# middleware.load_pydantic_models([product.Product, processes.ProcessData])
middleware.generate_rest_api()

app = middleware.app

# Start server by running: uvicorn app:app --reload