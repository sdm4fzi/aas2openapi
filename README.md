# aas2openapi - Middleware for Asset Administration Shell and openAPI 3.0

![Build-sucess](https://img.shields.io/badge/build-success-green)
![Version](https://img.shields.io/badge/version-0.1.1-green)
![PyPI - Python Version](https://img.shields.io/badge/python-3.10|3.11|3.12-blue)

aas2openapi is a middleware for Asset Administration Shell (AAS) and openAPI 3.0. It can be used to transform AAS to openAPI 3.0 objects and vice versa. Moreover, it can be used to generate a CRUD server that allows to access the AAS data via RESTful API with openAPI Specifications.

## Installation

You can install the package using [poetry](https://python-poetry.org/) by running the following commands in the terminal:

```bash
poetry shell
poetry install
```

Alternatively, you can install the package with pip by considering the wheel file in the [dist](dist/) folder:

```bash
pip install dist/aas2openapi-0.1.1-py3-none-any.whl
```

Please note that the package is only compatible with Python 3.10 or higher.

## Getting started

In the following, we will consider a minimal example to demonstrate the usage of the package. The example is also available in the [examples](examples/) and consists of defining a simple model of an AAS with two submodels, transforming this model and integrating it with the aas2openapi middleware.

### Defining a simple AAS

At first, we create a simple data model with the basic building blocks (AAS and Submodel) of aas2openapi:

```python
from aas2openapi import models

class BillOfMaterial(models.Submodel):
    components: typing.List[str]

class ProcessModel(models.Submodel):
    processes: typing.List[str]

class Product(models.AAS):
    bill_of_material: BillOfMaterial
    process_model: typing.Optional[ProcessModel]
```

The data model consists of a product that has a process model and a bill of material. The process model and the bill of material are submodels that contain a list of processes and components, respectively. To be able to instantiate an AAS, we also create an instance of this data model:

```python
example_product = Product(
    id_="bc2119e48d0",
    process_model=ProcessModel(
        id_="a8cd10ed",
        processes=["join", "screw"],
    ),
    bill_of_material=BillOfMaterial(
        id_="a7cba3bcd", components=["stator", "rotor", "coil", "bearing"]
    ),
)
```

### Transforming the AAS to openAPI

Now, we can use the `aas2openapi` package to transform the object to an AAS and serialize it with basyx to JSON:

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

The aas2openapi middleware is build with fastAPI and generates therefore automatically a openAPI Specification for provided models. To use the middleware, we can simply input our predefined data models and connect it with running basyx servers. Here, we use instances of the data models that we have defined before and create a CRUD RESTful API and a GraphQL API for them:

```python
from aas2openapi.middleware import Middleware
middleware = Middleware()
middleware.load_pydantic_model_instances([example_product])
middleware.generate_rest_api()
middleware.generate_graphql_api()

app = middleware.app

import uvicorn

uvicorn.run(app)
```

Besides loading the data models from instances,  we can also generate it from types or AAS. To do so, simply replace the `load_pydantic_model_instances` method with `load_pydantic_model_types` or `load_aas`:

```python
middleware.load_pydantic_model_types([Product])
middleware.load_aas_from_objectstore(obj_store)
```

However, no examples can be provided when loading from types and the graphQL API is not available when loading from AAS.

We can either run the middleware now directly with python or make a docker build. In both scenarios, an AAS and Submodel-server need to be running that the middleware can connect to. Each request to the middleware is then translated and forwarded to the AAS and Submodel-server.

The repository already comes with a docker-compose file that can be used to start the AAS and Submodel-server. To start the docker-compose file, run the following command in the terminal:

```bash
docker-compose -f docker-compose.yaml up
```

We can now run the middleware script with python and access it at `http://localhost:8000/`. Documentation of the generated Rest API is at `http://localhost:8000/docs` and the openAPI Specification is available at `http://localhost:8000/openapi.json`. The GraphQL API is at `http://localhost:8000/graphql` and comes also with a graphical viewer.

Lastly, we can build a docker image of the middleware and run it in a docker-compose as a container. To do so, just adjust the provided Dockerfile and docker-compose.yaml of this package to fit your needs based on the provided example in the file docker_app.py.

## Contributing

`aas2openapi` is a new project and has therefore much room for improvement. Therefore, it would be a pleasure to get feedback or support! If you want to contribute to the package, either create issues on [aas2openapis github page](https://github.com/sdm4fzi/aas2openapi) for discussing new features or contact me directly via [github](https://github.com/SebBehrendt) or [email](mailto:sebastian.behrendt@kit.edu).

## License

The package is licensed under the [MIT license](LICENSE).

## Acknowledgements

We extend our sincere thanks to the German Federal Ministry for Economic Affairs and Climate Action
(BMWK) for supporting this research project 13IK001ZF “Software-Defined Manufacturing for the
automotive and supplying industry [https://www.sdm4fzi.de/](https://www.sdm4fzi.de/).
