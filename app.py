from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, parse_obj_as, create_model
import json

from typing import List, Union, TypeVar, Generic, Type, Dict

from aas2openapi.client.aas_client import post_aas_to_server, put_aas_to_server, get_aas_from_server, delete_aas_from_server, get_all_aas_from_server
from aas2openapi.client.submodel_client import post_submodel_to_server, put_submodel_to_server, get_submodel_from_aas_id_and_class_name, delete_submodel_from_server
from aas2openapi.models import base, product, processes
from aas2openapi.util.convert_util import get_all_submodels_from_model

app = FastAPI()

all_types = Union[product.Product, processes.ProcessData]

def create_pydantic_model(model_definition):
    return parse_obj_as(all_types, model_definition)


def generate_submodel_endpoints_from_model(
    pydantic_model: Type[BaseModel], submodel: Type[base.Submodel]
):
    model_name = pydantic_model.__name__
    submodel_name = submodel.__name__
    @app.get(
        f"/{model_name}/{{item_id}}/{submodel_name}/",
        tags=[submodel_name],
        response_model=submodel,
    )
    async def get_item(item_id: str):
        return await get_submodel_from_aas_id_and_class_name(item_id, submodel_name)
    
    @app.delete(f"/{model_name}/{{item_id}}/{submodel_name}", tags=[submodel_name])
    async def delete_item(item_id: str):
        submodel = await get_submodel_from_aas_id_and_class_name(item_id, submodel_name)
        await delete_submodel_from_server(submodel.id_)
        return {"message": f"Succesfully deleted submodel with id {item_id}"}

    @app.put(f"/{model_name}/{{item_id}}/{submodel_name}", tags=[submodel_name])
    async def put_item(item_id: str, item: submodel) -> Dict[str, str]:
        submodel = await get_submodel_from_aas_id_and_class_name(item_id, submodel_name)
        await put_submodel_to_server(item)
        return {"message": f"Succesfully updated submodel with id {item_id}"}

    @app.post(
        f"/{model_name}/{{item_id}}/{submodel_name}",
        tags=[submodel_name],
        response_model=submodel,
    )
    async def post_item(item_id: str, item: submodel) -> Dict[str, str]:
        try:
            await get_submodel_from_aas_id_and_class_name(item_id, submodel_name)
        except HTTPException as e:
            if e.status_code == 400:
                await post_submodel_to_server(item)
                return item
            else:
                raise e


def generate_endpoints_from_model(pydantic_model: Type[BaseModel]):
    model_name = pydantic_model.__name__

    @app.get(f"/{model_name}/", tags=[model_name], response_model=List[pydantic_model])
    async def get_items():
        data_retrieved = await get_all_aas_from_server()
        return data_retrieved

    @app.get(
        f"/{model_name}/{{item_id}}", tags=[model_name], response_model=pydantic_model
    )
    async def get_item(item_id: str):
        data_retrieved = await get_aas_from_server(item_id)
        return data_retrieved

    @app.delete(f"/{model_name}/{{item_id}}", tags=[model_name])
    async def delete_item(item_id: str):
        await delete_aas_from_server(item_id)
        return {"message": "Item deleted"}

    @app.put(f"/{model_name}/{{item_id}}", tags=[model_name])
    async def put_item(item_id: str, item: pydantic_model) -> Dict[str, str]:
        await put_aas_to_server(item)
        return {"message": "Item updated"}

    @app.post(f"/{model_name}/", tags=[model_name], response_model=pydantic_model)
    async def post_item(item: pydantic_model) -> Dict[str, str]:
        # TODO: decide if reference on existing submodel should be updated or a an error is raised.
        await post_aas_to_server(item)
        return item

    submodels = get_all_submodels_from_model(pydantic_model)
    for submodel in submodels:
        generate_submodel_endpoints_from_model(
            pydantic_model=pydantic_model, submodel=submodel
        )


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


# Example usage to generate endpoints from a json file (models need to exist and be provided in all_types variable)
generate_fastapi_app("model.json")

# Example usage to generate endpoints from a list of instances
# generate_endpoints_from_instances([product.Product(id_="test", name="test", ...)])

# Example usage to generate endpoints from a list of types 
# generate_endpoints_from_model([product.Product])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)

