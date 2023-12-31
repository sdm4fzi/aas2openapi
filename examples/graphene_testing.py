import typing as T
import json
import uuid
import datetime
import decimal
from enum import Enum
import pydantic
import graphene
from aas2openapi import models


from graphene_pydantic import PydanticInputObjectType, PydanticObjectType


def add_class_method(model: T.Type):
    def is_type_of(cls, root, info):
        return isinstance(root, (cls, model))
    class_method = classmethod(is_type_of)
    model.is_type_of = class_method

class BillOfMaterialInfoModel(models.SubmodelElementCollection):
    manufacterer: str
    product_type: str

class BillOfMaterialModel(models.Submodel):
    components: T.List[str]
    bill_of_material_info: BillOfMaterialInfoModel

class ProcessModelModel(models.Submodel):
    processes: T.List[str]

class ProductStateEnum(str, Enum):
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    DEFECT = "defect"

class SpecialBillOfMaterialInfoModel(models.SubmodelElementCollection):
    manufacterer: str
    product_type: str
    product_version: str
    product_state: ProductStateEnum

class SpecialBillOfMaterialModel(models.Submodel):
    components: T.List[str]
    bill_of_material_info: T.Union[SpecialBillOfMaterialInfoModel, BillOfMaterialInfoModel]

class ProductModel(models.AAS):
    bill_of_material: BillOfMaterialModel
    process_model: T.Optional[ProcessModelModel]

class SpecialProductModel(models.AAS):
    special_bill_of_material: SpecialBillOfMaterialModel
    process_model: T.Optional[ProcessModelModel]


# Graphene mappings to the above models...


# class BillOfMaterialInfo(PydanticObjectType):
#     class Meta:
#         model = BillOfMaterialInfoModel

# add_class_method(BillOfMaterialInfo)

# class BillOfMaterial(PydanticObjectType):
#     class Meta:
#         model = BillOfMaterialModel

# add_class_method(BillOfMaterial)

# class ProcessModel(PydanticObjectType):
#     class Meta:
#         model = ProcessModelModel

# add_class_method(ProcessModel)

# class Product(PydanticObjectType):
#     class Meta:
#         model = ProductModel

# # add_class_method(Product)

# class SpecialBillOfMaterialInfo(PydanticObjectType):
#     class Meta:
#         model = SpecialBillOfMaterialInfoModel

# add_class_method(SpecialBillOfMaterialInfo)

# class SpecialBillOfMaterial(PydanticObjectType):
#     class Meta:
#         model = SpecialBillOfMaterialModel

# add_class_method(SpecialBillOfMaterial)

# class SpecialProduct(PydanticObjectType):
#     class Meta:
#         model = SpecialProductModel

# add_class_method(SpecialProduct)


# class Query(graphene.ObjectType):
#     list_special_products = graphene.List(SpecialProduct)
#     list_products = graphene.List(Product)

#     def resolve_list_special_products(self, info):
#         """Dummy resolver that creates a tree of Pydantic objects"""
#         return [
#             SpecialProductModel(
#                 id="example_product",
#                 id_short="id_short",
#                 special_bill_of_material=SpecialBillOfMaterialModel(
#                     id="id",
#                     components=["components"],
#                     bill_of_material_info=SpecialBillOfMaterialInfoModel(
#                         id_short="id_short",
#                         manufacterer="manufacterer",
#                         product_type="product_type",
#                         product_version="product_version",
#                         product_state=ProductStateEnum.IN_PROGRESS,
#                     ),
#                 ),
#                 process_model=ProcessModelModel(
#                     id="id_short2",
#                     processes=["processes"],
#                 ),
#             ),
#         ]
    
#     def resolve_list_products(self, info):
#         """Dummy resolver that creates a tree of Pydantic objects"""
#         return [
#             ProductModel(
#                 id="example_product",
#                 id_short="id_short",
#                 bill_of_material=BillOfMaterialModel(
#                     id="id",
#                     components=["components"],
#                     bill_of_material_info=BillOfMaterialInfoModel(
#                         id_short="id_short",
#                         manufacterer="manufacterer",
#                         product_type="product_type",
#                     ),
#                 ),
#                 process_model=ProcessModelModel(
#                     id="id_short2",
#                     processes=["processes"],
#                 ),
#             ),
#         ]

# class BillOfMaterialInput(PydanticInputObjectType):
#     class Meta:
#         model = BillOfMaterialModel



# class CreateBillOfMaterial(graphene.Mutation):
#     class Arguments:
#         person = BillOfMaterialInput(required=True)

#     Output = BillOfMaterial

#     def mutate(self, info, person: BillOfMaterialInput):
#         person_model = BillOfMaterial(**person)
#         ## save person_model here
#         return person
    
# class Mutation(graphene.ObjectType):
#     create_bill_of_material = CreateBillOfMaterial.Field()


# schema = graphene.Schema(query=Query)
# # schema = graphene.Schema(query=Query, mutation=Mutation)

# from fastapi import FastAPI
# from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
# app = FastAPI()
# app.mount("/igraphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
# app.mount("/graphql", GraphQLApp(schema=schema, playground=True, on_get=make_playground_handler()))


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app)

example_product = ProductModel(
    id="Product1",
    process_model=ProcessModelModel(
        id="PMP1",
        processes=["join", "screw"],
        semantic_id="PMP1_semantic_id",
    ),
    bill_of_material=BillOfMaterialModel(
        id="BOMP1", 
        components=["stator", "rotor", "coil", "bearing"],
        semantic_id="BOMP1_semantic_id",
        bill_of_material_info=BillOfMaterialInfoModel(
            id_short="BOMInfoP1",
            semantic_id="BOMInfoP1_semantic_id",
            manufacterer="Bosch", 
            product_type="A542", 
        )
    ),
)

example_special_product = SpecialProductModel(
    id="Product1",
    process_model=ProcessModelModel(
        id="PMP1",
        processes=["join", "screw"],
        semantic_id="PMP1_semantic_id",
    ),
    special_bill_of_material=SpecialBillOfMaterialModel(
        id="BOMP1", 
        components=["stator", "rotor", "coil", "bearing"],
        semantic_id="BOMP1_semantic_id",
        bill_of_material_info=SpecialBillOfMaterialInfoModel(
            id_short="BOMInfoP1",
            semantic_id="BOMInfoP1_semantic_id",
            manufacterer="Bosch", 
            product_type="A542", 
            product_version="1.0.0",
            product_state=ProductStateEnum.IN_PROGRESS
        )
    ),
)

from aas2openapi.middleware import Middleware

class Process(models.AAS):
    process_model: ProcessModelModel

example_process = Process(
    id="PMP1",
    process_model=ProcessModelModel(
        id="PMP1",
        processes=["join", "screw"],
        semantic_id="PMP1_semantic_id",
    ),
)

middleware = Middleware()
middleware.load_pydantic_models([SpecialProductModel, ProductModel])
# middleware.load_pydantic_model_instances([example_special_product, example_product])
# middleware.load_pydantic_model_instances([example_process, example_special_product])
middleware.generate_rest_api()
middleware.generate_graphql_api()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(middleware.app)