import typing
from pydantic import BaseModel

class Example(BaseModel):
    name: str
    count: int
    tag: typing.Optional[str] = ""


example_instance = Example(name="test", count=1)

print(example_instance)

from pydantic import create_model
from pydantic.fields import FieldInfo

DynamicModel = create_model("ExampleModel", **vars(example_instance))

example_dict = {}
for field_name, field in Example.__fields__.items():
    print(field_name)
    print(field)
    example_dict[field_name] =  DynamicModel.__fields__[field_name].default
    if field.required:
        DynamicModel.__fields__[field_name].required = True
    if field.default or field.default == "" or field.default == 0 or field.default == 0.0 or field.default == False or field.default == [] or field.default == {}:
        print("set default")
        DynamicModel.__fields__[field_name].default = field.default
        DynamicModel.__fields__[field_name].field_info = FieldInfo(default=field.default)
    else:
        DynamicModel.__fields__[field_name].default = None
        DynamicModel.__fields__[field_name].field_info = FieldInfo(default=None)
    if field.default_factory:
        DynamicModel.__fields__[field_name].default_factory = field.default_factory
    else:
        DynamicModel.__fields__[field_name].default_factory = None
    print(DynamicModel.__fields__[field_name])

print(DynamicModel)

new_example_instance = DynamicModel(name="Peter", count=2)

print(new_example_instance)



DynamicModel.Config.schema_extra = {"json_schema_extra": {"example": example_dict}}

print(DynamicModel.Config)
print(DynamicModel.schema_json(indent=2))