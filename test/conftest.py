import typing
import os
import time
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from aas2openapi import models
from aas2openapi.middleware import Middleware
from requests import get

response_aas = get("http://localhost:8081/shells")
response_sm = get("http://localhost:8082/submodels")
if (response_aas.status_code == 200 and response_aas.json()["result"] != []) or (response_sm.status_code == 200 and response_sm.json()["result"] != []):
    os.system("docker-compose -f docker-compose-dev.yaml restart")
else:
    os.system("docker-compose -f docker-compose-dev.yaml up -d")
time.sleep(1)
start = time.time()
while True:
    try:
        response_aas = get("http://localhost:8081/shells")
        response_sm = get("http://localhost:8082/submodels")
        if response_aas.status_code == 200 and response_sm.status_code == 200:
            break
    except:
        pass
    if time.time() - start > 20:
        raise Exception("Timeout: Could not connect to the docker container.")
    time.sleep(1)

class BillOfMaterialInfo(models.SubmodelElementCollection):
    manufacterer: str
    product_type: str

class BillOfMaterial(models.Submodel):
    components: typing.List[str]
    bill_of_material_info: BillOfMaterialInfo

class ProcessModel(models.Submodel):
    processes: typing.List[str]

class Product(models.AAS):
    bill_of_material: BillOfMaterial
    process_model: typing.Optional[ProcessModel]

@pytest.fixture(scope="class")
def example_smc() -> typing.Type[models.SubmodelElementCollection]:    
    yield BillOfMaterialInfo


@pytest.fixture(scope="function")
def example_sm() -> typing.Type[models.Submodel]:   
    yield BillOfMaterial


@pytest.fixture(scope="function")
def example_aas() -> typing.Type[models.AAS]:
    return Product


@pytest.fixture(scope="function")
def example_submodel_instance() -> models.Submodel:
    """
    Returns an example instance of Submodel.

    Yields:
        Iterator[typing.Generator[Submodel, typing.Any, None]]: the example instance of Submodel.
    """
    return BillOfMaterial(
        id="BOMP1",
        components=["stator", "rotor", "coil", "bearing"],
        semantic_id="BOMP1_semantic_id",
        bill_of_material_info=BillOfMaterialInfo(
            id_short="BOMInfoP1",
            semantic_id="BOMInfoP1_semantic_id",
            manufacterer="Bosch", 
            product_type="A542", 
        )
    )

@pytest.fixture(scope="function")
def example_aas_instance() -> models.AAS:
    """
    Returns an example instance of Product.

    Yields:
        Iterator[typing.Generator[Product, typing.Any, None]]: the example instance of Product.
    """
    return Product(
    id="Product1",
    process_model=ProcessModel(
        id="PMP1",
        processes=["join", "screw"],
        semantic_id="PMP1_semantic_id",
    ),
    bill_of_material=BillOfMaterial(
        id="BOMP1", 
        components=["stator", "rotor", "coil", "bearing"],
        semantic_id="BOMP1_semantic_id",
        bill_of_material_info=BillOfMaterialInfo(
            id_short="BOMInfoP1",
            semantic_id="BOMInfoP1_semantic_id",
            manufacterer="Bosch", 
            product_type="A542", 
        )
    ),
)


@pytest.fixture(scope="function")
def empty_middleware() -> Middleware:
    """
    Returns an example instance of Middleware.

    Yields:
        Iterator[typing.Generator[Middleware, typing.Any, None]]: the example instance of Middleware.
    """
    middleware = Middleware()
    middleware.generate_model_registry_api()
    return middleware


@pytest.fixture(scope="function")
def loaded_middleware(example_aas_instance: Product) -> Middleware:
    """
    Returns an example instance of Middleware with loaded models.

    Yields:
        Iterator[typing.Generator[Middleware, typing.Any, None]]: the example instance of Middleware with loaded models.
    """
    middleware = Middleware()
    middleware.load_pydantic_model_instances([example_aas_instance])
    middleware.generate_model_registry_api()
    middleware.generate_rest_api()
    middleware.generate_graphql_api()

    return middleware


@pytest.fixture(scope="function")
def app(loaded_middleware: Middleware) -> FastAPI:
    """
    Returns an example instance of FastAPI.

    Yields:
        Iterator[typing.Generator[FastAPI, typing.Any, None]]: the example instance of FastAPI.
    """
    return loaded_middleware.app


@pytest.fixture(scope="function")
def client(
    app: FastAPI
) -> TestClient:
    """
    Create a new FastAPI TestClient based on the current app.
    """
    with TestClient(app) as client:
        return client