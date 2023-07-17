import strawberry
from fastapi import FastAPI
from pydantic import BaseConfig, BaseModel, create_model, validator
from strawberry.fastapi import GraphQLRouter

from aas2openapi.models import base
from aas2openapi.middleware.graphql_routers import generate_strawberry_type_for_model, update_type_with_field

class Config:
    arbitrary_types_allowed = True
    # validation = False

    def prepare_field(self):
        pass


app = FastAPI()

from pydantic import BaseModel
from pydantic.fields import ModelField
from typing import Union

def convert_union_types_to_str(model_cls):
    new_model = create_model(__model_name=model_cls.__name__, __base__=model_cls)
    fields_requiring_post_validation = []
    new_type_dict = {}
    for field_name, field in new_model.__fields__.items():
        if isinstance(field, ModelField) and (field.type_ == typing._UnionGenericAlias or (hasattr(field.type_, "__origin__") and field.type_.__origin__ is Union)):
            field.type_ = str
            field.default = ""
            fields_requiring_post_validation.append(field_name)
        new_type_dict[field_name] = (field.type_, field.default if field.default else ...)
    def convert_to_str(cls, v):
        return str(v)
    validators = {
    'field_validator': validator(field_name, pre=True, always=True)(convert_to_str)
    }
    newer_model = create_model(__model_name=model_cls.__name__, **new_type_dict, __config__=Config, __validators__=validators)
    return newer_model



new_aas_type = create_model(__model_name="Example_aas", **base.AAS.__annotations__)

# new_submodel_type = create_model(__model_name="example_sm", **base.Submodel.__annotations__)
import typing
class Submodel(BaseModel):
    id_: str
    description: str
    id_short: str
    link: typing.Union[str, typing.List[str]] = ""

new_submodel_type = convert_union_types_to_str(Submodel)
print(new_submodel_type.__fields__) 


strawberry_submodel = generate_strawberry_type_for_model(new_submodel_type)
update_type_with_field(new_aas_type, "submodel", strawberry_submodel)
strawberry_aas = generate_strawberry_type_for_model(new_aas_type)


# print(Base.__fields__)
# print(fields)
print(strawberry_submodel._pydantic_type.__fields__)
# new_model = create_model(__model_name="NewModel", **Base.__fields__, __base__=Base, )
# print(new_model)
strawberry_sm = strawberry_submodel(**{"id_": "1", "description": "2", "id_short": "3", "link": [","]})
a = strawberry_aas(**{"id_": "1", "description": "2", "id_short": "3", "submodel": strawberry_sm})
print(a)
print(a.submodel)

print(strawberry_sm.to_pydantic())  