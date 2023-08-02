from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, create_model
from pydantic.fields import ModelField

from typing import List, Type, Dict

from aas2openapi.client.aas_client import (
    post_aas_to_server,
    put_aas_to_server,
    get_aas_from_server,
    delete_aas_from_server,
    get_all_aas_from_server,
)
from aas2openapi.client.submodel_client import (
    post_submodel_to_server,
    put_submodel_to_server,
    get_submodel_from_aas_id_and_class_name,
    delete_submodel_from_server,
)
from aas2openapi.models import base
from aas2openapi.util.convert_util import get_all_submodels_from_model, convert_camel_case_to_underscrore_str


def is_optional_field(field: ModelField):
    return field.required is False

def check_if_submodel_is_optional_in_aas(aas: Type[base.AAS], submodel: Type[base.Submodel]) -> bool:
    """
    Checks if a submodel is an optional attribute in an aas.

    Args:
        aas (Type[base.AAS]): AAS model.
        submodel (Type[base.Submodel]): Submodel to be checked.

    Raises:
        ValueError: If the submodel is not a submodel of the aas.

    Returns:
        bool: True if the submodel is an optional attribute in the aas, False otherwise.
    """
    for field_name, field in aas.__fields__.items():
        if field.type_.__name__ ==  submodel.__name__:
            if is_optional_field(field):
                return True
            else:
                return False
    raise ValueError(f"Submodel {submodel.__name__} is not a submodel of {aas.__name__}.")

def generate_submodel_endpoints_from_model(
    pydantic_model: Type[BaseModel], submodel: Type[base.Submodel]
) -> APIRouter:
    """
    Generates CRUD endpoints for a submodel of a pydantic model representing an aas.

    Args:
        pydantic_model (Type[BaseModel]): Pydantic model representing the aas of the submodel.
        submodel (Type[base.Submodel]): Pydantic model representing the submodel.

    Returns:
        APIRouter: FastAPI router with CRUD endpoints for the given submodel that performs Middleware syxnchronization.
    """
    model_name = pydantic_model.__name__
    submodel_name = submodel.__name__
    optional_submodel = check_if_submodel_is_optional_in_aas(pydantic_model, submodel)
    router = APIRouter(
        prefix=f"/{model_name}/{{item_id}}/{submodel_name}",
        tags=[model_name],
        responses={404: {"description": "Not found"}},
    )

    @router.get(
        "/",
        response_model=submodel,
    )
    async def get_item(item_id: str):
        return await get_submodel_from_aas_id_and_class_name(item_id, submodel_name)

    if optional_submodel:
        @router.post(
            "/",
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
    
    @router.put("/")
    async def put_item(item_id: str, item: submodel) -> Dict[str, str]:
        submodel = await get_submodel_from_aas_id_and_class_name(item_id, submodel_name)
        await put_submodel_to_server(item)
        return {"message": f"Succesfully updated submodel with id {item_id}"}

    if optional_submodel:
        @router.delete("/")
        async def delete_item(item_id: str):
            submodel = await get_submodel_from_aas_id_and_class_name(item_id, submodel_name)
            await delete_submodel_from_server(submodel.id_)
            return {"message": f"Succesfully deleted submodel with id {item_id}"}

    return router


def generate_aas_endpoints_from_model(pydantic_model: Type[BaseModel]) -> APIRouter:
    """
    Generates CRUD endpoints for a pydantic model representing an aas.

    Args:
        pydantic_model (Type[BaseModel]): Pydantic model representing an aas

    Returns:
        APIRouter: FastAPI router with CRUD endpoints for the given pydantic model that performs Middleware syxnchronization.
    """
    router = APIRouter(
        prefix=f"/{pydantic_model.__name__}",
        tags=[pydantic_model.__name__],
        responses={404: {"description": "Not found"}},
    )

    @router.get("/", response_model=List[pydantic_model])
    async def get_items():
        data_retrieved = await get_all_aas_from_server()
        return data_retrieved

    @router.post(f"/", response_model=pydantic_model)
    async def post_item(item: pydantic_model) -> Dict[str, str]:
        await post_aas_to_server(item)
        return item

    @router.get("/{item_id}", response_model=pydantic_model)
    async def get_item(item_id: str):
        data_retrieved = await get_aas_from_server(item_id)
        return data_retrieved

    @router.put("/{item_id}")
    async def put_item(item_id: str, item: pydantic_model) -> Dict[str, str]:
        await put_aas_to_server(item)
        return {"message": "Item updated"}

    @router.delete("/{item_id}")
    async def delete_item(item_id: str):
        await delete_aas_from_server(item_id)
        return {"message": "Item deleted"}


    return router


def generate_endpoints_from_model(pydantic_model: Type[BaseModel]) -> List[APIRouter]:
    """
    Generates CRUD endpoints for a pydantic model representing an aas and its submodels.

    Args:
        pydantic_model (Type[BaseModel]): Pydantic model representing an aas with submodels.

    Returns:
        List[APIRouter]: List of FastAPI routers with CRUD endpoints for the given pydantic model and its submodels that perform Middleware syxnchronization.
    """
    routers = []
    routers.append(generate_aas_endpoints_from_model(pydantic_model))
    submodels = get_all_submodels_from_model(pydantic_model)
    for submodel in submodels:
        routers.append(generate_submodel_endpoints_from_model(pydantic_model, submodel))

    return routers


def set_required_fields(model: Type[BaseModel], origin_model: Type[BaseModel]) -> Type[BaseModel]:
    """
    Sets the required fields of a pydantic model.

    Args:
        model (Type[BaseModel]): Pydantic model.
        origin_model (Type[BaseModel]): Pydantic model from which the required fields should be copied.

    Returns:
        Type[BaseModel]: Pydantic model with the required fields set.
    """
    for field_name, field in origin_model.__fields__.items():
        if field.required:
            model.__fields__[field_name].required = True
    return model


def get_pydantic_model_from_imstances(
    instances: List[BaseModel],
) -> List[Type[BaseModel]]:
    """
    Functions that creates pydantic models from instances.

    Args:
        instances (typing.List[BaseModel]): List of pydantic model instances.

    Returns:
        List[Type[BaseModel]]: List of pydantic models.
    """
    models = []
    for instance in instances:
        model_name = type(instance).__name__
        pydantic_model = create_model(model_name, **vars(instance))
        pydantic_model = set_required_fields(pydantic_model, instance.__class__)
        print(instance.__fields__)
        print(pydantic_model.__fields__)
        models.append(pydantic_model)
    return models
