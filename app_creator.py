from fastapi import FastAPI, Request
from pydantic import BaseModel, parse_obj_as, create_model
import json

from typing import List, Union, TypeVar, Generic, Type, Dict

from ba_syx_aas_repository_client import Client as AASClient
from ba_syx_submodel_repository_client import Client as SMClient

import asyncio
from basyx.aas import model

from ba_syx_aas_repository_client.api.asset_administration_shell_repository_api import (
    post_asset_administration_shell,
    get_all_asset_administration_shells,
    get_asset_administration_shell_by_id,
)
from ba_syx_submodel_repository_client.api.submodel_repository_api import (
    post_submodel, get_all_submodels, get_submodel_by_id
    
)

import aas2openapi
from aas2openapi.convert.convert_pydantic import ClientModel
from aas2openapi.models import base, product, processes
from aas2openapi.util import client_utils

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


def get_all_submodels_from_object_store(obj_store: model.DictObjectStore) -> List[model.Submodel]:
    submodels = []
    for item in obj_store:
        item = obj_store.get(item.id)
        if isinstance(item, model.Submodel):
            submodels.append(ClientModel(basyx_object=item))
    return submodels


async def push_aas_to_server(aas: base.AAS):
    obj_store = aas2openapi.convert_pydantic_model_to_aas(aas)
    basyx_aas = obj_store.get(aas.id_)
    aas_for_client = ClientModel(basyx_object=basyx_aas)
    client = AASClient("http://localhost:8081")
    try:
        response = asyncio.run(
            post_asset_administration_shell.sync(
                client=client, json_body=aas_for_client
            )
        )
    except Exception as e:
        print("Error:", e)

    submodels = get_all_submodels_from_object_store(basyx_aas)
    for submodel in submodels:
        push_submodel_to_server(submodel)


def retrieve_aas_from_server(aas_id: str) -> base.AAS:
    client = AASClient("http://localhost:8081")
    base_64_id = client_utils.get_base64_from_string(aas_id)
    aas_data = asyncio.run(
        get_asset_administration_shell_by_id.asyncio(client=client, aas_identifier=base_64_id)
    )
    model_data = aas2openapi.convert_object_store_to_pydantic_models(aas_data)
    return model_data


def retrieve_all_aas_from_server() -> List[base.AAS]:
    client = AASClient("http://localhost:8081")
    aas_data = asyncio.run(get_all_asset_administration_shells.asyncio(client=client))
    model_data = []
    for aas in aas_data:
        model_data.append(aas2openapi.convert_object_store_to_pydantic_models(aas))
    return model_data


def push_submodel_to_server(submodel: model.Submodel):
    client = SMClient("http://localhost:8082")
    try:
        response = asyncio.run(
            post_submodel.asyncio(client=client, json_body=submodel)
        )
        print(response)
    except Exception as e:
        print("Error:", e)

def get_submodel_from_server(submodel_id: str) -> base.Submodel:
    client = SMClient("http://localhost:8082")
    base_64_id = client_utils.get_base64_from_string(submodel_id)
    submodel_data = asyncio.run(
        get_submodel_by_id.asyncio(client=client, submodel_identifier=base_64_id)
    )
    model_data = aas2openapi.convert_sm_to_pydantic_model(submodel_data)
    return model_data

def get_all_submodels_from_server() -> List[base.Submodel]:
    client = SMClient("http://localhost:8082")
    submodel_data = asyncio.run(get_all_submodels.asyncio(client=client))
    model_data = []
    for submodel in submodel_data:
        model_data.append(aas2openapi.convert_sm_to_pydantic_model(submodel))
    return model_data

def post_submodel_to_server(submodel: base.Submodel) -> base.Submodel:
    client = SMClient("http://localhost:8082")
    try:
        response = asyncio.run(
            post_submodel.asyncio(client=client, json_body=submodel)
        )
    except Exception as e:
        print("Error:", e)
    return submodel


def generate_submodel_endpoints_from_model(
    model: Type[BaseModel], submodel_type: Type[base.Submodel]
):
    model_name = model.__name__
    submodel_name = submodel_type.__name__

    @app.get(
        f"/{model_name}/{{submodel_id}}/{submodel_name}/",
        tags=[submodel_name],
        response_model=submodel_type,
    )
    async def get_submodel(submodel_id: str):
        submodel = get_submodel_from_server(submodel_id)
        return submodel

    @app.delete(
        f"/{model_name}/{{submodel_id}}/{submodel_name}", tags=[submodel_name]
    )
    async def delete_submodel(submodel_id: str):
        # TODO: query aas server for submodel deletion
        return {"message": "Item deleted"}

    @app.put(
        f"/{model_name}/{{submodel_id}}/{submodel_name}", tags=[submodel_name]
    )
    async def put_submodel(submodel_id: int, submodel: submodel_type) -> Dict[str, str]:
        # TODO: query aas server for submodel update with put method if it already exists
        return {"message": "Item updated"}

    @app.post(
        f"/{model_name}/{{item_id}}/{submodel_name}",
        tags=[submodel_name],
        response_model=submodel_type,
    )
    async def post_item(submodel: submodel_type) -> Dict[str, str]:
        # TODO: check if submodel already exists, if so, raise an error
        # TODO: query aas server for submodel creation with post method, if it does not exist yet
        push_submodel_to_server(submodel)
        return submodel


def generate_endpoints_from_model(model: Type[BaseModel]):
    model_name = model.__name__

    @app.get(f"/{model_name}/", tags=[model_name], response_model=List[model])
    async def get_aas():
        data_retrieved = retrieve_all_aas_from_server()
        return data_retrieved

    @app.get(f"/{model_name}/{{item_id}}", tags=[model_name], response_model=model)
    async def get_aas_by_id(aas_id: str):
        aas = retrieve_aas_from_server(aas_id)
        return aas

    @app.delete(f"/{model_name}/{{item_id}}", tags=[model_name])
    async def delete_aas(item_id: str):
        # TODO: query aas server for object deletion
        return {"message": "Item deleted"}

    @app.put(f"/{model_name}/{{item_id}}", tags=[model_name])
    async def put_aas(item_id: str, item: model) -> Dict[str, str]:
        # TODO: query aas server for object update with put method if it already exists
        return {"message": "Item updated"}

    @app.post(f"/{model_name}/", tags=[model_name], response_model=model)
    async def post_aas(item: model) -> Dict[str, str]:
        # TODO: check if aas already exists, if so, raise an error
        print("____________push the aas")
        print(item)
        await push_aas_to_server(item)
        return {"haha": "haha"}

    submodels = get_all_submodels_from_model(model)
    for submodel in submodels:
        print(submodel)
        generate_submodel_endpoints_from_model(model=model, submodel_type=submodel)


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
