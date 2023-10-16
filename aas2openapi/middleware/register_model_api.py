from fastapi import APIRouter, HTTPException, FastAPI
from fastapi.openapi.utils import get_openapi

from aas2openapi.middleware.rest_routers import generate_endpoints_from_model


from typing import Dict

def route_matches(route, name):
    route_api_key = route.path_format.split("/")[1]
    print("____", route_api_key, name)
    return route_api_key == name


def remove_model_routes_from_app(app: FastAPI, model_name: str):
    """
    Function removes routes from app that contain the model_name as first route seperator.

    Args:
        app (FastAPI): FastAPI app to remove routes from
        model_name (str): model_name of model to remove from API of app
    """
    indices_to_delete = []
    for i, r in enumerate(app.routes):
        if route_matches(r, model_name):
            indices_to_delete.append(i)
    for index in sorted(indices_to_delete, reverse=True):
        del app.routes[index]
    update_openapi(app)

def remove_graphql_api(app: FastAPI):
    for i, r in enumerate(app.routes):
        if route_matches(r, "graphql"):
            del app.routes[i]


def update_openapi(app: FastAPI):
    """
    Updates the openAPI schema of a fastAPI app during runtime to register updates.

    Args:
        app (FastAPI): app where the openapi schema should be updated.
    """
    app.openapi_schema = get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                terms_of_service=app.terms_of_service,
                contact=app.contact,
                license_info=app.license_info,
                routes=app.routes,
                tags=app.openapi_tags,
                servers=app.servers,
            )


def generate_model_api(middleware_instance) -> APIRouter:
    """
    Generates endpoints to register und unregister models from the middleware. 

    Returns:
        APIRouter: FastAPI router with endpoints to register and register models.
    """
    # TODO: make sure, that middleware can be imported for type annotation without cycling import. 
    # TODO: maybe add a get and update request for existing models. maybe extend the path with name of the model (or not) 
    # TODO: Also allow to retrieve and post models as JSONSchema -> with required / non-required fields.
    router = APIRouter(
        prefix=f"",
        tags=["Model registry"],
        responses={404: {"description": "Not found"}},
    )

    @router.post(
        "/register_model",
        response_model=dict,
    )
    async def post_model(model_name: str, model: dict) -> Dict[str, str]:
        if any(model_name == model_instance.__name__ for model_instance in middleware_instance.models):
            raise HTTPException(403, f"A model with the name {model_name} exists already!")
        if not "id_" in model.keys():
            raise HTTPException(403, f"Mandatory field id_ is missing for the model <{model_name}>.")
        for key, value in model.items():
            if isinstance(value, dict) and not "id_" in value.keys():
                raise HTTPException(403, f"Mandatory field id_ is missing in submodel <{key}> for model <{model_name}>.")
        middleware_instance.load_json_models(json_models={model_name: model}, all_fields_required=True)
        routers = generate_endpoints_from_model(middleware_instance.models[-1])
        for router in routers:
            middleware_instance.app.include_router(router)
        update_openapi(middleware_instance.app)
        remove_graphql_api(middleware_instance.app)
        middleware_instance.generate_graphql_api()
        return {"message": f"Succesfully created API for model {model_name}."}
    



    @router.delete("/delete_model", response_model=dict)
    async def delete_model(model_name: str):
        new_models = []
        if not any(model.__name__ == model_name for model in middleware_instance.models):
            raise HTTPException(404, f"No model registered in middleware with name <{model_name}>")
        for model in middleware_instance.models:
            if not model.__name__ == model_name:
                new_models.append(model)
        middleware_instance.models = new_models

        remove_model_routes_from_app(middleware_instance.app, model_name)
        remove_graphql_api(middleware_instance.app)
        middleware_instance.generate_graphql_api()

        return {"message": f"Succesfully deleted API for model {model_name}."}

    return router

