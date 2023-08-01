import typing
from pydantic import BaseModel

class Tester(BaseModel):
    name: str
    age: typing.Optional[int] = None






if __name__ == '__main__':
    for field in Tester.__fields__.values():
        print("___", field)
        print(field.type_, type(field.type_))