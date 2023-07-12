import typing
from pydantic import BaseModel, parse_obj_as, create_model, Field
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import aas2openapi
import json

from basyx.aas import model
from aas2openapi.middleware.graphql_routers import generate_graphql_endpoint
from aas2openapi.middleware.rest_routers import generate_endpoints_from_model, get_pydantic_model_from_imstances
import aas2openapi


class Middleware:

    def __init__(self):
        self.models: typing.List[typing.Type[BaseModel]] = []
        self._app: typing.Optional[FastAPI] = None


    @property
    def app(self):
        if not self._app:
            description = """
             The aas2openapi middleware allows to convert aas models to pydantic models and generate a REST or GraphQL API from them.
                """

            app = FastAPI(
                title="aas2openapi",
                description=description,
                version=aas2openapi.VERSION,
                contact={
                    "name": "Sebastian Behrendt",
                    "email": "sebastian.behrendt@kit.edu",
                },
                license_info={
                    "name": "MIT License",
                    "url": "https://mit-license.org/",
                },
            )

            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=["*"],
                allow_methods=["*"],
                allow_headers=["*"],
            )
            self._app = app
            @app.get("/", response_model=str)
            async def root():
                return "Welcome to aas2openapi Middleware!"
        return self._app

    def load_pydantic_model_instances(self, instances: typing.List[BaseModel]):
        """
        Functions that loads pydantic models into the middleware that can be used for synchronization.

        Args:
            instances (typing.List[BaseModel]): List of pydantic model instances.
        """
        self.models = get_pydantic_model_from_imstances(instances)

    def load_pydantic_models(self, models: typing.List[typing.Type[BaseModel]]):
        """
        Functions that loads pydantic models into the middleware that can be used for synchronization.

        Args:
            models (typing.List[typing.Type[BaseModel]]): List of pydantic models.
        """
        self.models = models

    def load_aas_from_objectstore(self, models: model.DictObjectStore):
        """
        Functions that loads multiple aas and their submodels into the middleware that can be used for synchronization.

        Args:
            models (typing.List[model.DictObjectStore]): Object store of aas' and submodels
        """
        instances = aas2openapi.convert_object_store_to_pydantic_models(models)
        self.models = get_pydantic_model_from_imstances(instances)
            
    def generate_rest_api(self):
        """
        Generates a REST API with CRUD operations for aas' and submodels from the loaded models.
        """
        for model in self.models:
            routers = generate_endpoints_from_model(model)
            for router in routers:
                self.app.include_router(router)

    def generate_graphql_api(self):
        """
        Generates a GraphQL API with query operations for aas' and submodels from the loaded models.
        """
        router = generate_graphql_endpoint(self.models)
        self.app.include_router(router)