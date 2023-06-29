from __future__ import annotations

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, parse_obj_as, create_model
import json

from typing import List, Union, TypeVar, Generic, Type, Dict

from ba_syx_aas_repository_client import Client as AASClient
from ba_syx_submodel_repository_client import Client as SMClient

import asyncio
from anyio import run
from basyx.aas import model

from ba_syx_aas_repository_client.api.asset_administration_shell_repository_api import (
    post_asset_administration_shell,
    get_all_asset_administration_shells,
    get_asset_administration_shell_by_id,
    put_asset_administration_shell_by_id,
    delete_asset_administration_shell_by_id,
)
from ba_syx_submodel_repository_client.api.submodel_repository_api import (
    post_submodel, get_all_submodels, get_submodel_by_id, delete_submodel_by_id, put_submodel_by_id
    
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


def aas_is_on_server(aas_id: str) -> bool:
    try: 
        get_aas_from_server(aas_id)
        return True
    except Exception as e:
        return False
    
def submodel_is_on_server(submodel_id: str) -> bool:
    try: 
        get_submodel_from_server(submodel_id)
        return True
    except Exception as e:
        return False

async def post_aas_to_server(aas: base.AAS):
    if aas_is_on_server(aas.id_):
        raise HTTPException(status_code=400, detail=f"AAS with id {aas.id_} already exists")
    obj_store = aas2openapi.convert_pydantic_model_to_aas(aas)
    basyx_aas = obj_store.get(aas.id_)
    aas_for_client = ClientModel(basyx_object=basyx_aas)
    client = AASClient("http://localhost:8081")
    response = asyncio.run(
        post_asset_administration_shell.asyncio(
            client=client, json_body=aas_for_client
        )
    )

    submodels = get_all_submodels_from_object_store(basyx_aas)
    for submodel in submodels:
        post_submodel_to_server(submodel)

async def put_aas_to_server(aas: base.AAS):
    if not aas_is_on_server(aas.id_):
        raise HTTPException(status_code=400, detail=f"AAS with id {aas.id_} does not exist")
    obj_store = aas2openapi.convert_pydantic_model_to_aas(aas)
    basyx_aas = obj_store.get(aas.id_)
    aas_for_client = ClientModel(basyx_object=basyx_aas)
    client = AASClient("http://localhost:8081")
    base_64_id = client_utils.get_base64_from_string(aas.id_)
    response = asyncio.run(
        put_asset_administration_shell_by_id.asyncio(
            aas_identifier=base_64_id, client=client, json_body=aas_for_client
        )
    )

    submodels = get_all_submodels_from_object_store(basyx_aas)
    for submodel in submodels:
        put_submodel_to_server(submodel)

async def get_aas_from_server(aas_id: str) -> base.AAS:
    client = AASClient("http://localhost:8081")
    base_64_id = client_utils.get_base64_from_string(aas_id)
    aas_data = run(
        get_asset_administration_shell_by_id.asyncio(client=client, aas_identifier=base_64_id)
    )
    model_data = aas2openapi.convert_object_store_to_pydantic_models(aas_data).pop()
    return model_data

async def delete_aas_from_server(aas_id: str):
    client = AASClient("http://localhost:8081")
    base_64_id = client_utils.get_base64_from_string(aas_id)
    response = await delete_asset_administration_shell_by_id.asyncio(client=client, aas_identifier=base_64_id)


async def get_all_aas_from_server() -> List[base.AAS]:
    client = AASClient("http://localhost:8081")
    aas_data = await get_all_asset_administration_shells.asyncio(client=client)
    model_data = []
    for aas in aas_data:
        model_data.append(aas2openapi.convert_object_store_to_pydantic_models(aas))
    return model_data


async def post_submodel_to_server(pydantic_submodel: base.Submodel):
    if submodel_is_on_server(pydantic_submodel.id_):
        raise HTTPException(status_code=400, detail=f"Submodel with id {pydantic_submodel.id} already exists")
    basyx_submodel = aas2openapi.convert_pydantic_model_to_submodel(pydantic_submodel)
    submodel_for_client = ClientModel(basyx_object=basyx_submodel)
    client = SMClient("http://localhost:8082")
    response = asyncio.run(
        post_submodel.asyncio(client=client, json_body=submodel_for_client)
    )

async def put_submodel_to_server(submodel: base.Submodel):
    if not submodel_is_on_server(submodel.id_):
        raise HTTPException(status_code=400, detail=f"Submodel with id {submodel.id} does not exist")
    basyx_submodel = aas2openapi.convert_pydantic_model_to_submodel(submodel)
    submodel_for_client = ClientModel(basyx_object=basyx_submodel)
    client = SMClient("http://localhost:8082")
    base_64_id = client_utils.get_base64_from_string(submodel.id_)
    response = await put_submodel_by_id.asyncio(
            submodel_identifier=base_64_id, client=client, json_body=submodel
        )
        

async def get_submodel_from_server(submodel_id: str) -> base.Submodel:
    client = SMClient("http://localhost:8082")
    base_64_id = client_utils.get_base64_from_string(submodel_id)
    submodel_data = asyncio.run(
        get_submodel_by_id.asyncio(client=client, submodel_identifier=base_64_id)
    )
    model_data = aas2openapi.convert_sm_to_pydantic_model(submodel_data)
    return model_data

async def get_all_submodels_from_server() -> List[base.Submodel]:
    client = SMClient("http://localhost:8082")
    submodel_data = asyncio.run(get_all_submodels.asyncio(client=client))
    model_data = []
    for submodel in submodel_data:
        model_data.append(aas2openapi.convert_sm_to_pydantic_model(submodel))
    return model_data

async def delete_submodel_from_server(submodel_id: str):
    client = SMClient("http://localhost:8082")
    base_64_id = client_utils.get_base64_from_string(submodel_id)
    response = asyncio.run(
        delete_submodel_by_id.asyncio(client=client, submodel_identifier=base_64_id)
    )


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
        delete_submodel_from_server(submodel_id)
        return {"message": f"Succesfully deleted submodel with id {submodel_id}"}

    # @app.put(
    #     f"/{model_name}/{{submodel_id}}/{submodel_name}", tags=[submodel_name]
    # )
    # async def put_submodel(submodel_id: int, submodel: submodel_type) -> Dict[str, str]:
    #     put_submodel_to_server(submodel)
    #     return {"message": f"Succesfully updated submodel with id {submodel_id}"}

    # @app.post(
    #     f"/{model_name}/{{item_id}}/{submodel_name}",
    #     tags=[submodel_name],
    #     response_model=submodel_type,
    # )
    # async def post_item(submodel: submodel_type) -> Dict[str, str]:
    #     post_submodel_to_server(submodel)
    #     return submodel


def generate_endpoints_from_model(pydantic_model: Type[BaseModel]):
    model_name = pydantic_model.__name__

    @app.get(f"/{model_name}/", tags=[model_name], response_model=List[pydantic_model])
    async def get_aas():
        data_retrieved = await get_all_aas_from_server()
        return data_retrieved

    @app.get(f"/{model_name}/{{item_id}}", tags=[model_name], response_model=pydantic_model)
    async def get_aas_by_id(aas_id: str):
        aas = await get_aas_from_server(aas_id)
        return aas

    @app.delete(f"/{model_name}/{{item_id}}", tags=[model_name])
    async def delete_aas(aas_id: str):
        await delete_aas_from_server(aas_id)
        return {"message": f"Succesfully deleted aas with id {aas_id}"}

    @app.put(f"/{model_name}/{{item_id}}", tags=[model_name])
    async def put_aas(aas_id: str, model_instance: pydantic_model) -> Dict[str, str]:
        await put_aas_to_server(model_instance)
        return {"message": f"Succesfully updated aas with id {aas_id}"}

    # @app.post(f"/{model_name}/", tags=[model_name], response_model=pydantic_model)
    # async def post_aas(model_instance: pydantic_model) -> Dict[str, str]:
    #     await post_aas_to_server(model_instance)
    #     return model_instance

    submodels = get_all_submodels_from_model(pydantic_model)
    for submodel in submodels:
        generate_submodel_endpoints_from_model(model=pydantic_model, submodel_type=submodel)


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
