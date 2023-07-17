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

def convert_union_to_str(model_cls):
    # Create a new class inheriting from the original model class
    new_model = create_model(__model_name=model_cls.__name__, __base__=model_cls)
    # new_model = create_model(__model_name=model_cls.__name__, **model_cls.__fields__, __base__=model_cls)
    print(new_model.__annotations__)
    # Iterate over the fields of the modified class
    fields_requiring_post_validation = []
    for field_name, field in new_model.__fields__.items():
        if isinstance(field, ModelField) and (field.type_ == typing._UnionGenericAlias or (hasattr(field.type_, "__origin__") and field.type_.__origin__ is Union)):
            # Replace the union type with str type
            field.type_ = str
            field.default = ""
            fields_requiring_post_validation.append(field_name)
            # Add a pre-validator to convert int/float values to str
        print(field_name, field)
    
    def convert_to_str(cls, v):
        return str(v)
    validators = {
    'field_validator': validator(field_name, pre=True, always=True)(convert_to_str)
    }
    newer_model = create_model(__model_name=model_cls.__name__, **new_model.__fields__, __config__=Config, __validators__=validators)
    # for field_name, field in newer_model.__fields__.items():
    #     print(field_name, field)
    #     if field_name in fields_requiring_post_validation:
    #         print("adding validator", field_name, field)

    #         # newer_model.__pre_root_validators__.append(convert_to_str)
    #          # @validator(field_name, always=True)
    #         # def convert_to_str(cls, v):
    #         #     print("convert_to_str", v, type(v))
    #         #     return str(v)

    #         # Assign the pre-validator to the field
    #         if not field.pre_validators:
    #             field.pre_validators = [convert_to_str]
    #         else:
    #             field.pre_validators = [convert_to_str] + field.pre_validators

    return newer_model



new_aas_type = create_model(__model_name="Example_aas", **base.AAS.__annotations__)

# new_submodel_type = create_model(__model_name="example_sm", **base.Submodel.__annotations__)
import typing
class Submodel(BaseModel):
    id_: str
    description: str
    id_short: str
    link: typing.Union[str, typing.List[str]] = ""

new_submodel_type = convert_union_to_str(Submodel)


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

# print(strawberry_sm.to_pydantic())  