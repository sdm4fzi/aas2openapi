from typing import  Union, List, Tuple


from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection



class GeneralInformation(Submodel):
   order_ids: str
   priority: int
   time_model_id: str
   customer_information: str
   
class ProductInstance(Submodel):
    product_type: str 
   
class Order(AAS):
    productInstance = ProductInstance
    generalInformation: GeneralInformation

    
