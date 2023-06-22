from pydantic import BaseModel, create_model
from typing import Type, Optional, Set, Iterable, Dict

class Submodel(BaseModel):
    id_: str
    code: int

class Item1(BaseModel):
    id_: str
    price: float
    is_offer: bool = None
    # sm: Submodel



# item_1 = Item1(id_="1", price=1.0, is_offer=True, sm=Submodel(id_="1", code=1))


# a = create_model(type(item_1).__name__, **vars(item_1))

# print(a)

# b = a(**item_1.dict())


# print(type(b))
# print(b)
# print(b.dict())

# print(a.__fields__)

def check_if_submodel_exists(model: Type[BaseModel]):
    for field in model.__fields__.values():
        if field.type_ == Submodel:
            return True
    return False

# print(Item1.schema())
print(check_if_submodel_exists(Item1))
