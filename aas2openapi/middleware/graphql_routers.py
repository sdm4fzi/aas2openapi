from aas2openapi.client.aas_client import get_aas_from_server, get_all_aas_from_server
from aas2openapi.convert.convert_pydantic import get_vars
from aas2openapi.models import base
from aas2openapi.util import convert_util
from aas2openapi.util.convert_util import get_all_submodels_from_model


import strawberry
from fastapi import APIRouter
from pydantic import BaseModel, create_model


from typing import List, Type


def generate_graphql_endpoint(models: List[Type[BaseModel]]) -> APIRouter:
    """
    Generates a GraphQL endpoint for the given pydantic models.
    Args:
        models (List[Type[BaseModel]]): List of pydantic models.
    Returns:
        APIRouter: FastAPI router with GraphQL endpoint for the given pydantic models.
    """
    import strawberry
    from strawberry.fastapi import GraphQLRouter
    for model in models:
        model_name = model.__name__


        # TODO: have an empty aas class which gets extended with its submodels, but they have the annotation for strawberry type -> create type at the end
        dict_pydantic_base_aas = base.AAS(id_="", description="", id_short="").dict()
        submodels = get_all_submodels_from_model(models[0])

        for submodel in submodels:
            dict_pydantic_base_sm = base.Submodel(id_="", description="", id_short="", semantic_id="").dict()
            for sme in get_vars(submodel):
                if isinstance(sme, base.SubmodelElementCollection):
                    @strawberry.experimental.pydantic.type(model=sme, all_fields=True)
                    class StarberrySubModelElement:
                        pass
                    class_name = type(sme).__name__ + "Type"
                    strawberry_submodel_element_class = StarberrySubModelElement
                    strawberry_submodel_element_class.__name__ = class_name
                    attribute_name_of_submodel = convert_util.convert_camel_case_to_underscrore_str(type(sme).__name__)
                    dict_pydantic_base_sm.update({
                        attribute_name_of_submodel: strawberry_submodel_element_class
                        })
                elif isinstance(sme, list):
                    pass

            submodel = create_model(submodel.__name__, **dict_pydantic_base_sm, __base__=base.Submodel)

            @strawberry.experimental.pydantic.type(model=submodel, all_fields=True)
            class StarberrySubModel:
                pass
            class_name = submodel.__name__ + "Type"
            strawberry_submodel_class = StarberrySubModel
            strawberry_submodel_class.__name__ = class_name
            strawberry_submodel_class.__qualname__ = class_name
            attribute_name_of_submodel = convert_util.convert_camel_case_to_underscrore_str(submodel.__name__)
            dict_pydantic_base_aas.update({
                attribute_name_of_submodel: strawberry_submodel_class
                })

        print("dict_pydantic_base_aas", dict_pydantic_base_aas)
        # TODO: fix that the strawberry type are also used when initiating the model
        model_type = create_model(model_name + "Type", **dict_pydantic_base_aas, __base__=base.AAS)
        print(model_type, model_type.__fields__)

        @strawberry.experimental.pydantic.type(model=model_type, all_fields=True)
        class StarberryModel:
            pass

        strawberry_aas_class = StarberryModel
        strawberry_aas_class.__name__ = model_name + "Type"
        strawberry_aas_class.__qualname__ = model_name + "Type"


        @strawberry.type
        class Query:
            @strawberry.field(name="get_" + model_name)
            async def get_model(self, id: str) -> strawberry_aas_class:
                aas = await get_aas_from_server(id)
                return strawberry_aas_class.from_pydantic(aas)
            
            @strawberry.field(name="get_all_" + model_name)
            async def get_all_models(self) -> List[strawberry_aas_class]:
                aas_list = await get_all_aas_from_server()
                return [strawberry_aas_class.from_pydantic(aas) for aas in aas_list]

    schema = strawberry.Schema(query=Query)
    return GraphQLRouter(schema, "/graphql")