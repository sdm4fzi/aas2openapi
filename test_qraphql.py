import strawberry
from fastapi import FastAPI
from pydantic import BaseConfig, BaseModel, create_model
from pydantic.fields import ModelField
from strawberry.fastapi import GraphQLRouter

from aas2openapi.models import base
from aas2openapi.middleware.graphql_routers import generate_strawberry_type_for_model, update_type_with_field

class Config:
    arbitrary_types_allowed = True
    # validation = False

    def prepare_field(self):
        pass


app = FastAPI()

print(vars(base.AAS))
print(base.AAS.__fields__)
print(base.AAS.__annotations__)
print("________")


new_aas_type = create_model(__model_name="Example_aas", **base.AAS.__annotations__)

new_submodel_type = create_model(__model_name="example_sm", **base.Submodel.__annotations__)

strawberry_submodel = generate_strawberry_type_for_model(new_submodel_type)
print(strawberry_submodel)
update_type_with_field(new_aas_type, "submodel", strawberry_submodel)
strawberry_aas = generate_strawberry_type_for_model(new_aas_type)


# print(Base.__fields__)
# print(fields)
print(new_aas_type.__fields__)
print(new_aas_type.__config__.__dict__)
# new_model = create_model(__model_name="NewModel", **Base.__fields__, __base__=Base, )
# print(new_model)
strawberry_sm = strawberry_submodel(**{"id_": "1", "description": "2", "id_short": "3"})
a = strawberry_aas(**{"id_": "1", "description": "2", "id_short": "3", "submodel": strawberry_sm})
print(a)
print(a.submodel)
