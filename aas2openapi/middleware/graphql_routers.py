from aas2openapi.client.aas_client import get_aas_from_server, get_all_aas_from_server
from aas2openapi.convert.convert_pydantic import get_vars
from aas2openapi.models import base
from aas2openapi.util import convert_util
from aas2openapi.util.convert_util import get_all_submodel_elements_from_submodel, get_all_submodels_from_model

import typing

import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.experimental.pydantic.conversion_types import (
        PydanticModel,
        StrawberryTypeFromPydantic,
    )
from fastapi import APIRouter
from pydantic import BaseModel, create_model
from pydantic.fields import ModelField
from pydantic import BaseConfig


from typing import List, Type


def generate_strawberry_type_for_model(model: Type[BaseModel]) -> StrawberryTypeFromPydantic:
    """
    Generates a strawberry type for the given pydantic model.

    Args:
        model (Type[BaseModel]): Pydantic model for which the strawberry type should be generated.

    Returns:
        strawberry.type: Strawberry type for the given pydantic model.
    """
    class_name = model.__name__ + "Type"
    @strawberry.experimental.pydantic.type(model=model, all_fields=True, name=class_name)
    class StrawberryModel:
        pass
    StrawberryModel.__name__ = class_name
    StrawberryModel.__qualname__ = class_name
    return StrawberryModel

def update_type_with_field(new_type: Type[BaseModel], field_name: str, field_type: StrawberryTypeFromPydantic | list | str | bool | float | int):
    print("ff", field_name, field_type)
    class Config(BaseConfig):
        arbitrary_types_allowed = True
        validation = False

        def prepare_field(self):
            pass

    field = ModelField(
            name=field_name,
            type_=field_type,
            class_validators=None,
            model_config=Config,
    )
    new_type.__fields__.update({
        field_name: field
    })

def create_new_smc(smc: Type[base.SubmodelElementCollection]) -> Type[BaseModel]:
    new_submodel_type = create_model(__model_name=smc.__name__, **base.SubmodelElementCollection.__annotations__)
    return new_submodel_type


def add_submodel_elements_to_submodel_type(submodel_type: Type[BaseModel], attribute_name, submodel_element_type: Type[BaseModel]):
    print("submodel_element_type", submodel_element_type)
    try:
        if issubclass(submodel_element_type, base.SubmodelElementCollection):
            print("smc")
            new_smc = create_new_smc(submodel_element_type)
            strawberry_submodel_element_class = generate_strawberry_type_for_model(new_smc)
            update_type_with_field(submodel_type, attribute_name, strawberry_submodel_element_class)
            return
        elif issubclass(submodel_element_type, list):
            print("list")
            if issubclass(submodel_element_type[0], base.SubmodelElementCollection):
                strawberry_submodel_element_class = generate_strawberry_type_for_model(submodel_element_type)
                add_submodel_elements_to_submodel_type(submodel_type, attribute_name, List[strawberry_submodel_element_class])
            else:
                update_type_with_field(submodel_type, attribute_name, submodel_element_type)
            return
    except:
        print("error", submodel_element_type)
    update_type_with_field(submodel_type, attribute_name, submodel_element_type)

def generate_graphql_endpoint(models: List[Type[BaseModel]]) -> APIRouter:
    """
    Generates a GraphQL endpoint for the given pydantic models.
    Args:
        models (List[Type[BaseModel]]): List of pydantic models.
    Returns:
        APIRouter: FastAPI router with GraphQL endpoint for the given pydantic models.
    """
    for model in models:
        model_name = model.__name__
        model_type = create_model(__model_name=model_name, **base.AAS.__annotations__)
        
        submodels = get_all_submodels_from_model(model)
        for submodel in submodels:
            new_submodel_type = create_model(__model_name=submodel.__name__, **base.Submodel.__annotations__)
            print("submodel", submodel.__fields__, "###", submodel.__annotations__)
            sme_dict = get_all_submodel_elements_from_submodel(submodel)
            # FIXME: fix this to correctly add submodel elements to submodel -> Problem with union types!
            # for sme_name, sme in sme_dict.items():
            #     print("sme", sme_name, sme)
            #     add_submodel_elements_to_submodel_type(new_submodel_type, sme_name, sme)
            strawberry_submodel_class = generate_strawberry_type_for_model(new_submodel_type)
            attribute_name_of_submodel = convert_util.convert_camel_case_to_underscrore_str(new_submodel_type.__name__)
            update_type_with_field(model_type, attribute_name_of_submodel, strawberry_submodel_class)

        strawberry_aas_class = generate_strawberry_type_for_model(model_type)


        @strawberry.type
        class Query:
            @strawberry.field(name="get_" + model_name)
            async def get_model(self, id: str) -> strawberry_aas_class:
                aas = await get_aas_from_server(id)
                print(aas)
                return strawberry_aas_class.from_pydantic(aas)
            
            @strawberry.field(name="get_all_" + model_name)
            async def get_all_models(self) -> List[strawberry_aas_class]:
                aas_list = await get_all_aas_from_server()
                return [strawberry_aas_class.from_pydantic(aas) for aas in aas_list]

    schema = strawberry.Schema(query=Query)
    return GraphQLRouter(schema, "/graphql")