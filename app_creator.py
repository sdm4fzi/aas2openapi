from fastapi import FastAPI, Request
from pydantic import BaseModel, parse_obj_as, create_model
import json

from typing import List, Union, TypeVar, Generic, Type, Dict

from aas2openapi.models import base, product, processes

app = FastAPI()

all_types = Union[product.Product, processes.ProcessData]

def create_pydantic_model(model_definition):
    return parse_obj_as(all_types, model_definition)

def get_all_submodels_from_model(model: Type[BaseModel]):
    submodels = []
    for field in model.__fields__.values():
        if issubclass(field.type_, base.Submodel):
            submodels.append(field.type_)
    return submodels

def generate_submodel_endpoints_from_model(model: Type[BaseModel], submodel: Type[base.Submodel]):
    model_name = model.__name__
    submodel_name = submodel.__name__

    @app.get(f"/{model_name}/{{item_id}}/{submodel_name}/", tags=[model_name, submodel_name], response_model=submodel)
    async def get_item(item_id: int):
        # TODO: query aas server for submodel
        # TODO: convert aas data to pydantic models and return it
        data_retrieved = []
        return data_retrieved
    
    @app.delete(f"/{model_name}/{{item_id}}/{submodel_name}", tags=[model_name, submodel_name])
    async def delete_item(item_id: int):
        # TODO: query aas server for submodel deletion
        return {"message": "Item deleted"}
    
    @app.put(f"/{model_name}/{{item_id}}/{submodel_name}", tags=[model_name, submodel_name])
    async def put_item(item_id: int, item: submodel) -> Dict[str, str]:
        # TODO: query aas server for submodel update with put method if it already exists
        return {"message": "Item updated"}
    
    @app.post(f"/{model_name}/{{item_id}}/{submodel_name}", tags=[model_name, submodel_name], response_model=submodel)
    async def post_item(item: submodel) -> Dict[str, str]:
        # TODO: query aas server for submodel creation with post method, if it does not exist yet
        return item

def generate_endpoints_from_model(model: Type[BaseModel]):
    model_name = model.__name__

    @app.get(f"/{model_name}/", tags=[model_name], response_model=List[model])
    async def get_items():
        # TODO: query aas server for objects
        # TODO: convert aas data to pydantic models and return it
        data_retrieved = []
        return data_retrieved
    
    @app.get(f"/{model_name}/{{item_id}}", tags=[model_name], response_model=model)
    async def get_item(item_id: int):
        # TODO: query aas server for object
        # TODO: convert aas data to pydantic model and return it
        data_retrieved = []
        return data_retrieved
    
    @app.delete(f"/{model_name}/{{item_id}}", tags=[model_name])
    async def delete_item(item_id: int):
        # TODO: query aas server for object deletion
        return {"message": "Item deleted"}        
    
    @app.put(f"/{model_name}/{{item_id}}", tags=[model_name])
    async def put_item(item_id: int, item: model) -> Dict[str, str]:
        # TODO: query aas server for object update with put method if it already exists
        return {"message": "Item updated"}
    
    @app.post(f"/{model_name}/", tags=[model_name], response_model=model)
    async def post_item(item: model) -> Dict[str, str]:
        # TODO: query aas server for object creation with post method, if it does not exist yet
        return item
    
    submodels = get_all_submodels_from_model(model)
    for submodel in submodels:
        print(submodel)
        generate_submodel_endpoints_from_model(model=model, submodel=submodel)

def generate_endpoints_from_instances(instances: List[BaseModel]):
    items = []
    model_name = type(instances[0]).__name__
    pydantic_model = create_model(model_name, **vars(instances[0]))

    generate_endpoints_from_model(pydantic_model)

def generate_fastapi_app(json_file: str):
    with open(json_file) as file:
        models = json.load(file)

    for model_definitions in models.values():
        models = []
        for model_definition in model_definitions:
            model = create_pydantic_model(model_definition)
            models.append(model)
        generate_endpoints_from_instances(models)


# Example usage
generate_fastapi_app("model.json")
