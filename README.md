# aas2openapi - Middleware for Asset Administration Shell and openAPI 3.0

![Build-sucess](https://img.shields.io/badge/build-success-green)
![Version](https://img.shields.io/badge/version-0.1.7-green)
![PyPI - Python Version](https://img.shields.io/badge/python-3.10|3.11|3.12-blue)
[![DOI](https://zenodo.org/badge/672818560.svg)](https://zenodo.org/badge/latestdoi/672818560)

aas2openapi is a middleware for Asset Administration Shell (AAS) and openAPI 3.0. It can be used to transform AAS to openAPI 3.0 objects and vice versa. Moreover, it can be used to generate a CRUD server that allows to access the AAS data via RESTful API with openAPI Specifications.

## Installation

You can install the package using by running the following command in the terminal:

```bash
pip install git+https://github.com/sdm4fzi/aas2openapi.git@main
```

You can also install the package within a [potry](https://python-poetry.org/) project by adding the following line to the pyproject.toml file:

```bash
aas2openapi = { git = "ssh://git@github.com/sdm4fzi/aas2openapi.git", tag = "0.1.7" }
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
    id_="Product1",
    process_model=ProcessModel(
        id_="PMP1",
        processes=["join", "screw"],
        semantic_id="hunder",
    ),
    bill_of_material=BillOfMaterial(
        id_="BOMP1", components=["stator", "rotor", "coil", "bearing"],
        semantic_id="hund",
        bill_of_material_info=BillOfMaterialInfo(
            id_short="BOMInfoP1",
            semantic_id="hahaah",
            manufacterer="Siemens", typi="1234", 
        )
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

The aas2openapi middleware is build with fastAPI and generates therefore automatically a openAPI Specification for provided models. To use the middleware, we can simply input our predefined data models and connect it with running basyx servers. Here, we use instances of the data models that we have defined before and create a CRUD RESTful API for them:

```python
from aas2openapi.middleware import Middleware
middleware = Middleware()
middleware.load_pydantic_model_instances([example_product])
middleware.generate_rest_api()

app = middleware.app

import uvicorn

uvicorn.run(app)
```

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
docker-compose -f basyx-compose.yaml up
```

We can now run the middleware script with python and access it at `http://localhost:8000/`. Documentation of the generated Rest API is at `http://localhost:8000/docs` and the openAPI Specification is available at `http://localhost:8000/openapi.json`. 

If you want to change the adresses and ports of the AAS and Submodel-server, you can do so by adding a `.env` file to the root directory of the package. The file should contain speicifications similar to that in the `.env.example` file of the package.

Lastly, we can build a docker image of the middleware and run it in a docker-compose as a container. To do so, just adjust the provided Dockerfile and docker-compose.yaml of this package to fit your needs based on the provided example in the file docker_app.py. To build the docker image, run the following command in the terminal:

```bash
docker compose build
```

lastly, we can run the docker-compose file with the following command and start aas2openapi, AAS server and submodel server at the same time:
    
```bash
docker compose up
```

## Contributing

`aas2openapi` is a new project and has therefore much room for improvement. Therefore, it would be a pleasure to get feedback or support! If you want to contribute to the package, either create issues on [aas2openapis github page](https://github.com/sdm4fzi/aas2openapi) for discussing new features or contact me directly via [github](https://github.com/SebBehrendt) or [email](mailto:sebastian.behrendt@kit.edu).

## License

The package is licensed under the [MIT license](LICENSE).

## Acknowledgements

We extend our sincere thanks to the German Federal Ministry for Economic Affairs and Climate Action
(BMWK) for supporting this research project 13IK001ZF “Software-Defined Manufacturing for the
automotive and supplying industry [https://www.sdm4fzi.de/](https://www.sdm4fzi.de/).
