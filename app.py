from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, parse_obj_as, create_model
import json

from typing import List, Union, TypeVar, Generic, Type, Dict

from ba_syx_aas_repository_client import Client as AASClient
from ba_syx_submodel_repository_client import Client as SMClient

import asyncio

from basyx.aas import model
import basyx.aas.adapter.json


from ba_syx_aas_repository_client.api.asset_administration_shell_repository_api import (
    post_asset_administration_shell,
    get_all_asset_administration_shells,
    get_asset_administration_shell_by_id,
    put_asset_administration_shell_by_id,
    delete_asset_administration_shell_by_id,
)
from ba_syx_submodel_repository_client.api.submodel_repository_api import (
    post_submodel,
    get_all_submodels,
    get_submodel_by_id,
    delete_submodel_by_id,
    put_submodel_by_id,
)

import aas2openapi
from aas2openapi.convert.convert_pydantic import ClientModel, get_vars, rename_data_specifications_for_basyx, rename_semantic_id_for_basyx, remove_empty_lists
from aas2openapi.models import base, product, processes
from aas2openapi.util import client_utils

app = FastAPI()

all_types = Union[product.Product, processes.ProcessData]

# TODO: refactor this file for utils, routers and convenience functions needed to generate the server

def create_pydantic_model(model_definition):
    return parse_obj_as(all_types, model_definition)


def get_all_submodels_from_model(model: Type[BaseModel]):
    submodels = []
    for field in model.__fields__.values():
        if issubclass(field.type_, base.Submodel):
            submodels.append(field.type_)
    return submodels


def get_all_submodels_from_object_store(
    obj_store: model.DictObjectStore,
) -> List[model.Submodel]:
    submodels = []
    for item in obj_store:
        if isinstance(item, model.Submodel):
            submodels.append(item)
    return submodels


async def aas_is_on_server(aas_id: str) -> bool:
    try:
        await get_aas_from_server(aas_id)
        return True
    except Exception as e:
        return False


async def submodel_is_on_server(submodel_id: str) -> bool:
    try:
        await get_submodel_from_server(submodel_id)
        return True
    except Exception as e:
        return False


async def post_aas_to_server(aas: base.AAS):
    if await aas_is_on_server(aas.id_):
        raise HTTPException(
            status_code=400, detail=f"AAS with id {aas.id_} already exists"
        )
    obj_store = aas2openapi.convert_pydantic_model_to_aas(aas)
    basyx_aas = obj_store.get(aas.id_)
    aas_for_client = ClientModel(basyx_object=basyx_aas)
    client = AASClient("http://localhost:8081")
    response = await post_asset_administration_shell.asyncio(
        client=client, json_body=aas_for_client
    )

    aas_attributes = get_vars(aas)
    for submodel in aas_attributes.values():
        await post_submodel_to_server(submodel)


async def put_aas_to_server(aas: base.AAS):
    if not await aas_is_on_server(aas.id_):
        raise HTTPException(
            status_code=400, detail=f"AAS with id {aas.id_} does not exist"
        )
    obj_store = aas2openapi.convert_pydantic_model_to_aas(aas)
    basyx_aas = obj_store.get(aas.id_)
    aas_for_client = ClientModel(basyx_object=basyx_aas)
    client = AASClient("http://localhost:8081")
    base_64_id = client_utils.get_base64_from_string(aas.id_)
    response = await delete_asset_administration_shell_by_id.asyncio(
        aas_identifier=base_64_id, client=client, json_body=aas_for_client
    )

    submodels = get_all_submodels_from_object_store(basyx_aas)
    for submodel in submodels:
        put_submodel_to_server(submodel)


async def get_basyx_aas_from_server(aas_id: str) -> model.AssetAdministrationShell:
    client = AASClient("http://localhost:8081")
    base_64_id = client_utils.get_base64_from_string(aas_id)
    aas_data = await get_asset_administration_shell_by_id.asyncio(
        client=client, aas_identifier=base_64_id
    )
    return transform_client_to_basyx_model(aas_data.to_dict())

async def get_aas_from_server(aas_id: str) -> base.AAS:
    aas = await get_basyx_aas_from_server(aas_id)
    aas_submodels = await get_all_basyx_submodels_from_server(aas)
    obj_store = model.DictObjectStore()
    obj_store.add(aas)
    [obj_store.add(submodel) for submodel in aas_submodels]

    model_data = aas2openapi.convert_object_store_to_pydantic_models(obj_store).pop()
    return model_data


async def delete_aas_from_server(aas_id: str):
    client = AASClient("http://localhost:8081")
    base_64_id = client_utils.get_base64_from_string(aas_id)
    response = await delete_asset_administration_shell_by_id.asyncio(
        client=client, aas_identifier=base_64_id
    )


def transform_client_to_basyx_model(response_model: dict) -> Union[model.AssetAdministrationShell, model.Submodel]:
    rename_data_specifications_for_basyx(response_model)
    rename_semantic_id_for_basyx(response_model)
    remove_empty_lists(response_model)
    json_model = json.dumps(response_model, indent=4)
    basyx_model = json.loads(json_model, cls=basyx.aas.adapter.json.AASFromJsonDecoder)
    return basyx_model

async def get_basyx_submodel_from_server(submodel_id: str) -> model.Submodel:
    client = SMClient("http://localhost:8082")
    base_64_id = client_utils.get_base64_from_string(submodel_id)
    submodel_data = await get_submodel_by_id.asyncio(
        client=client, submodel_identifier=base_64_id
    )
    return transform_client_to_basyx_model(submodel_data.to_dict())


async def get_all_basyx_submodels_from_server(aas: model.AssetAdministrationShell) -> List[model.Submodel]:
    submodels = []
    for submodel_reference in aas.submodel:
        basyx_submodel = await get_basyx_submodel_from_server(submodel_reference.key[0].value)
        submodels.append(basyx_submodel)
    return submodels


async def get_all_aas_from_server() -> List[base.AAS]:
    client = AASClient("http://localhost:8081")
    result_string = await get_all_asset_administration_shells.asyncio(client=client)
    aas_data = result_string["result"]
    aas_list = [transform_client_to_basyx_model(aas) for aas in aas_data]

    submodels = []
    for aas in aas_list:
        aas_submodels = await get_all_basyx_submodels_from_server(aas)
        submodels.extend(aas_submodels)
    obj_store = model.DictObjectStore()
    [obj_store.add(aas) for aas in aas_list]
    [obj_store.add(submodel) for submodel in submodels]
    
    model_data = aas2openapi.convert_object_store_to_pydantic_models(obj_store)
    return model_data


async def post_submodel_to_server(pydantic_submodel: base.Submodel):
    if await submodel_is_on_server(pydantic_submodel.id_):
        raise HTTPException(
            status_code=400,
            detail=f"Submodel with id {pydantic_submodel.id_} already exists",
        )
    basyx_submodel = aas2openapi.convert_pydantic_model_to_submodel(pydantic_submodel)
    submodel_for_client = ClientModel(basyx_object=basyx_submodel)
    client = SMClient("http://localhost:8082")
    response = await post_submodel.asyncio(client=client, json_body=submodel_for_client)


async def put_submodel_to_server(submodel: base.Submodel):
    if not await submodel_is_on_server(submodel.id_):
        raise HTTPException(
            status_code=400, detail=f"Submodel with id {submodel.id_} does not exist"
        )
    basyx_submodel = aas2openapi.convert_pydantic_model_to_submodel(submodel)
    submodel_for_client = ClientModel(basyx_object=basyx_submodel)
    client = SMClient("http://localhost:8082")
    base_64_id = client_utils.get_base64_from_string(submodel.id_)
    response = await put_submodel_by_id.asyncio(
        submodel_identifier=base_64_id, client=client, json_body=submodel
    )


async def get_submodel_from_server(submodel_id: str) -> base.Submodel:
    basyx_submodel = await get_basyx_submodel_from_server(submodel_id)    
    model_data = aas2openapi.convert_sm_to_pydantic_model(basyx_submodel)
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
        aas = await get_basyx_aas_from_server(item_id)
        for sm in aas.submodel:
            submodel_id = sm.key[0].value
            submodel = await get_submodel_from_server(submodel_id)
            if submodel.__class__.__name__ == submodel_name:
                return submodel
        raise HTTPException(
            status_code=400,
            detail=f"Submodel with name {submodel_name} does not exist for AAS with id {item_id}",
        )
    
    @app.delete(f"/{model_name}/{{item_id}}/{submodel_name}", tags=[submodel_name])
    async def delete_item(item_id: str):
        # TODO: test
        await delete_submodel_from_server(item_id)
        return {"message": f"Succesfully deleted submodel with id {item_id}"}

    @app.put(f"/{model_name}/{{item_id}}/{submodel_name}", tags=[submodel_name])
    async def put_item(item_id: str, item: submodel) -> Dict[str, str]:
        # TODO: test
        await put_submodel_to_server(item)
        return {"message": f"Succesfully updated submodel with id {item_id}"}

    @app.post(
        f"/{model_name}/{{item_id}}/{submodel_name}",
        tags=[submodel_name],
        response_model=submodel,
    )
    async def post_item(item: submodel) -> Dict[str, str]:
        # TODO: test
        await post_submodel_to_server(item)
        return item


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
        # TODO: test
        await delete_aas_from_server(item_id)
        return {"message": "Item deleted"}

    @app.put(f"/{model_name}/{{item_id}}", tags=[model_name])
    async def put_item(item_id: str, item: pydantic_model) -> Dict[str, str]:
        # TODO: test
        await put_aas_to_server(item)
        return {"message": "Item updated"}

    @app.post(f"/{model_name}/", tags=[model_name], response_model=pydantic_model)
    async def post_item(item: pydantic_model) -> Dict[str, str]:
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


# Example usage
generate_fastapi_app("model.json")
