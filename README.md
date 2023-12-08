# aas2openapi - Middleware for Asset Administration Shell and openAPI 3.0

![Build-sucess](https://img.shields.io/badge/build-success-green)
![PyPI](https://img.shields.io/pypi/v/aas2openapi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aas2openapi)
[![DOI](https://zenodo.org/badge/672818560.svg)](https://zenodo.org/badge/latestdoi/672818560)

aas2openapi is a middleware for Asset Administration Shell (AAS) and openAPI 3.0. It can be used to transform AAS to openAPI 3.0 objects and vice versa. Moreover, it can be used to generate a CRUD server that allows to access the AAS data via RESTful API with openAPI Specifications.

## Installation

You can install the package using by running the following command in the terminal:

```bash
pip install aas2openapi
```


Alternatively, you can install the package with [poetry](https://python-poetry.org/) for development:

```bash
poetry shell
poetry install
```

Please note that the package is only compatible with Python 3.10 or higher.

## Getting started

In the following, we will consider a minimal example to demonstrate the usage of the package. The example is also available in the [examples](examples/) and consists of defining a simple model of an AAS with two submodels, transforming this model and integrating it with the aas2openapi middleware.

### Defining a simple AAS

At first, we create a simple data model with the basic building blocks (AAS and Submodel) of aas2openapi:

```python
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
```

The data model consists of a product that has a process model and a bill of material. The process model and the bill of material are submodels that contain a list of processes and components, respectively. To be able to instantiate an AAS, we also create an instance of this data model:

```python
example_product = Product(
    id="Product1",
    process_model=ProcessModel(
        id="PMP1",
        processes=["join", "screw"],
        semantic_id="PMP1_semantic_id",
    ),
    bill_of_material=BillOfMaterial(
        id="BOMP1", components=["stator", "rotor", "coil", "bearing"],
        semantic_id="BOMP1_semantic_id",
        bill_of_material_info=BillOfMaterialInfo(
            id_short="BOMInfoP1",
            semantic_id="BOMInfoP1_semantic_id",
            manufacterer="Bosch", product_type="A542", 
        )
    ),
)
```

### Transforming the AAS to openAPI

Now, we can use `aas2openapi` to transform the object to an AAS and serialize it with basyx to JSON:

```python
import aas2openapi
obj_store = aas2openapi.convert_pydantic_model_to_aas(example_product)
import basyx.aas.adapter.json.json_serialization

with open("examples/simple_aas_and_submodels.json", "w", encoding="utf-8") as json_file:
    basyx.aas.adapter.json.write_aas_json_file(json_file, obj_store)
```

Of course, we can also transform AAS to python objects, which can be easily transformed to openAPI objects with the middleware:

```python
data_model = aas2openapi.convert_object_store_to_pydantic_models(obj_store)
print(data_model)
```

### Using the aasopenapi middleware

The aas2openapi middleware is build with fastAPI and generates therefore automatically a openAPI Specification for provided models. To use the middleware, we can simply input our predefined data models and connect it with running basyx servers. Here, we use instances of the data models that we have defined before and create a CRUD RESTful API for them:

```python
from aas2openapi.middleware import Middleware
middleware = Middleware()
middleware.load_pydantic_model_instances([example_product])
middleware.generate_rest_api()
middleware.generate_graphql_api()
middleware.generate_model_registry_api()

app = middleware.app
```

We can run this app either from the command line with uvicorn:

```bash
  uvicorn app:app --reload
```

Here, it is assumed, that the file you saved is called app.py. If it has a different name, rename the first app. Alternatively, you can also run the app directly with python, by extending the script at the bottom with:

```python
  if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)

```

You can access now the documentation of the REST API with swagger at `http://localhost:8000/docs` and the graphql endpoint at  `http://localhost:8000/graphql`. 

Besides loading the data models from instances,  we can also generate it directly from its python type, from a JSON-object or from an AAS. To do so, simply replace the `load_pydantic_model_instances` method with `load_pydantic_models` to load from types or `load_aas_objectstore` to load from an AAS object store or `load_json_models` to load from serialized JSON-objects:

```python
middleware.load_pydantic_model_types([Product])
middleware.load_aas_from_objectstore(obj_store)
middleware.load_json_models(file_path="examples/example_json_model.json")

```

However, no examples can be provided when loading from types.

We can either run the middleware now directly with python or make a docker build. In both scenarios, an AAS and Submodel-server need to be running that the middleware can connect to. Each request to the middleware is then translated and forwarded to the AAS and Submodel-server.

The repository already comes with a docker-compose file that can be used to start the AAS and Submodel-server. To start the docker-compose file, run the following command in the terminal:

```bash
docker-compose -f docker-compose-dev.yaml up
```

We can now run the middleware script with python and access it at `http://localhost:8000/`. Documentation of the generated Rest API is at `http://localhost:8000/docs` available by a swaggerUI and the openAPI Specification is available at `http://localhost:8000/openapi.json`. You can use the swaggerUI to post some AAS or this exemplary command (with bash console):
    
```bash
  curl -X 'POST' \
  'http://127.0.0.1:8000/Product/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id_short": "Product1",
  "description": "string",
  "id": "Product1",
  "bill_of_material": {
    "id_short": "BOMP1",
    "description": "",
    "id": "BOMP1",
    "semantic_id": "BOMP1_semantic_id",
    "components": [
      "stator",
      "rotor",
      "coil",
      "bearing"
    ],
    "bill_of_material_info": {
      "id_short": "BOMInfoP1",
      "description": "",
      "semantic_id": "BOMInfoP1_semantic_id",
      "manufacterer": "Bosch",
      "product_type": "A542"
    }
  },
  "process_model": {
    "id_short": "PMP1",
    "description": "",
    "id": "PMP1",
    "semantic_id": "PMP1_semantic_id",
    "processes": [
      "join",
      "screw"
    ]
  }
}'
```

If you want to change the adresses and ports of the AAS and Submodel-server, you can do so by adding a `.env` file to the root directory of the package. The file should contain speicifications similar to that in the `.env.example` file of the package.

Lastly, we can build a docker image of the middleware and run it in a docker-compose as a container. To do so, just adjust the provided Dockerfile and docker-compose.yaml of this package to fit your needs based on the provided example in the file docker_app.py. To build the docker image, run the following command in the terminal:

```bash
docker compose build
```

lastly, we can run the docker-compose file with the following command and start aas2openapi, AAS server and submodel server at the same time:
    
```bash
docker compose up
```

If you want to start the middleware also with a user interface for the AAS and a mongo db backend for AAS, you can use the following command:

```bash
docker compose -f docker-compose-ui.yaml up -d
```

The user interface is then available at `http://localhost:3000/`. After posting some AAS with the middleware (see above), you can add the AAS to the user interface by clicking on the "+" button and entering the AAS id (base64 encoded). The AAS is then available in the user interface.

## Contributing

`aas2openapi` is a new project and has therefore much room for improvement. Therefore, it would be a pleasure to get feedback or support! If you want to contribute to the package, either create issues on [aas2openapis github page](https://github.com/sdm4fzi/aas2openapi) for discussing new features or contact me directly via [github](https://github.com/SebBehrendt) or [email](mailto:sebastian.behrendt@kit.edu).

## License

The package is licensed under the [MIT license](LICENSE).

## Acknowledgements

We extend our sincere thanks to the German Federal Ministry for Economic Affairs and Climate Action
(BMWK) for supporting this research project 13IK001ZF “Software-Defined Manufacturing for the
automotive and supplying industry [https://www.sdm4fzi.de/](https://www.sdm4fzi.de/).
