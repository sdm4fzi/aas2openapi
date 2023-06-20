from fastapi import FastAPI, Request
from pydantic import BaseModel, parse_obj_as
import json

from typing import List, Union, TypeVar, Generic, Type, get_type_hints, get_args

app = FastAPI()

T = TypeVar('T')

class Test(Generic[T]):
    pass

class Item1(BaseModel):
    id_: str
    price: float
    is_offer: bool = None

class Item2(BaseModel):
    id_: str
    value: float

all_types = Union[Item1, Item2]

def create_pydantic_model(model_name, model_definition):
    return parse_obj_as(all_types, model_definition)


def generate_endpoints(model_name, models: List[BaseModel]):
    items = []

    @app.get(f"/{model_name}/", tags=[model_name], response_model=List[type(models[0])])
    async def get_items():
        return models

    @app.get(f"/{model_name}/{{item_id}}", tags=[model_name], response_model=type(models[0]))
    async def get_item(item_id: int):
        return [model for model in models if model.id_ == item_id]

    @app.delete(f"/{model_name}/{{item_id}}", tags=[model_name])
    async def delete_item(item_id: int):
        models = [model for model in models if model.id_ != item_id]
        return {"message": "Item deleted"}        
    
    @app.put(f"/{model_name}/{{item_id}}", tags=[model_name])
    async def put_item(item_id: int, item: all_types) -> dict:
        data = item.form()
        models.append(item)
        return {"message": "Item updated"}

    return items


def generate_fastapi_app(json_file):
    with open(json_file) as file:
        models = json.load(file)

    for model_name, model_definitions in models.items():
        models = []
        for model_definition in model_definitions:
            model = create_pydantic_model(model_name, model_definition)
            models.append(model)
        generate_endpoints(model_name, models)


# Example usage
generate_fastapi_app("models.json")





# i1 = Item1(name="Foo", price=50.4, is_offer=True)
# i2 = Item2(name="Bar", value=42.0)

# class Container(BaseModel):
#     items1: List[Item1]
#     items2: List[Item2]

# c = Container(items1=[i1], items2=[i2])

# with open("models.json", "w", encoding="utf-8") as json_file:
#     data = c.dict()
#     json.dump(data, json_file, ensure_ascii=False, indent=4)
