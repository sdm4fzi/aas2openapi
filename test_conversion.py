import json
from urllib import parse

from basyx.aas import model
import basyx.aas.adapter.json.json_serialization

from typing import List

from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection
from aas2openapi.models import product

example_smc = product.subProduct(
    id_ = "SMC_example", 
    description = "xyz", 
    subProbductType = "a",
    subProductAAS = "b",
    status = "c",
    quantity = "5",
    subProductAttributes = None
    )

example_material = product.MaterialData(
    id_ = "1",
    description = "y",
    material_type = "A",
    processes = "B",
    transport_process = "C"
    )

example_bom = product.BOM(
    id_ = "Example_Bom_Submodel",
    description = "this is an example",
    assembly = "assembly",
    subProduct = [example_smc],
    subProductCount = "http://193.196.37.23:4001/aasServer/shells/AAS_caesar_id/aas",
    material_data = example_material
    )

example_process_reference = product.ProcessReference(
    id_ = "Example_Process_Reference",
    description = "this is an example",
    semantic_id = "1",
    process_id="2",
    process_type="3",
)


example_product = product.Product(
    id_ = "Example_Product", description = "456", bom = example_bom, process_reference=example_process_reference, 
    )







def create_submodel(attribute_name: str,
                    attribute_value: Submodel):
    submodel = model.Submodel(
                    id_short = attribute_value.id_,
                    id_ = attribute_value.id_,
                    description=attribute_value.id_
                    )
    
    print(attribute_name, "is a submodel")
            
    submodel_attributes = vars(attribute_value)
    print(submodel_attributes)
    
    for sm_attribute_name, sm_attribute_value in submodel_attributes.items():
        if isinstance(sm_attribute_value, SubmodelElementCollection):

            smc = model.SubmodelElementCollection(
                    id_short=sm_attribute_name,
                    id_=sm_attribute_name,
                    value_type=model.datatypes.String,
                    value=sm_attribute_value,
                )
            submodel.submodel_element.add(smc)
            
            print("SMC", sm_attribute_name)

        elif (
            isinstance(sm_attribute_value, str)
            and parse.urlparse(sm_attribute_value).scheme
            and parse.urlparse(sm_attribute_value).netloc
        ) or (sm_attribute_name.split("_")[-1] in ["id","ids"]): 
            
            pass
        
            print(sm_attribute_name)
            print(sm_attribute_value)
            
            
            
            key = model.Key(
                type_=model.KeyTypes.ASSET_ADMINISTRATION_SHELL,
                value="1",
            )
        
            reference = model.Reference(
                key = (key,)
                    )
            
            reference_element = model.ReferenceElement(
                id_short=sm_attribute_name,
                value=reference,
            )
            
            submodel.submodel_element.add(reference_element)  
            print("Reference", sm_attribute_name)

        else:
            property = model.Property(
                    id_short=sm_attribute_name,
                    value_type=model.datatypes.String,
                    value=str(sm_attribute_value),
                    )
            submodel.submodel_element.add(property)

            
            print("Property", sm_attribute_name)
    return submodel




def convert_pydantic_model_to_aas(aas: product.AAS) -> model.AssetAdministrationShell:
    #  transform pydantic model to AAS

    # step 1.1: create an identifier for the Asset
    identifier = model.Identifier(id_=aas.id_, id_type=model.Identifier.CUSTOM)

    # step 1.2: create the Asset object
    asset = model.Asset(
        id_short = aas.id_,
        kind = model.AssetKind.INSTANCE,
        identification = identifier,
    )
    print("Asset created")

    description = aas.description

    #  create submodels
  
    aas_attributes = vars(aas)
    aas_submodels = []  # placeholder for submodels created

    for attribute_name, attribute_value in aas_attributes.items():
        if isinstance(attribute_value, product.Submodel):
            # TODO: create submodel here

            tempsubmodel = create_submodel(
                attribute_name=attribute_name,
                attribute_value=attribute_value        
            )
            aas_submodels.append(tempsubmodel)
            
            
            
            
                    
                    


   
    # TODO: create AAS and add Submodels

    # # ALTERNATIVE: step 2 and 3 can alternatively be done in one step
    # submodel = model.Submodel(
    #     id_short=product.Submodel.id_,
    #     identification=model.Identifier(
    #         product.Submodel.id_, model.IdentifierType.CUSTOM
    #     ),
    # )

    # submodel = model.Submodel(
    #     id_short=product.SubmodelElementCollection.id_,
    #     identification=model.Identifier(
    #         product.SubmodelElementCollection.id_, model.IdentifierType.CUSTOM
    #     ),
    # )

    # aas = model.AssetAdministrationShell(
    #     id_short=aas.id_,
    #     identification=model.Identifier(aas.id_, model.IdentifierType.CUSTOM),
    #     asset=model.AASReference.from_referable(asset),
    #     submodel={model.AASReference.from_referable(submodel)},
    # )

    # # step 4.2: create the simple Property
    # property_ = model.Property(
    #     id_short=product.description,
    #     value_type=model.datatypes.String,
    #     value=string,
    # )

    # # step 4.3: add the Property to the Submodel
    # submodel.submodel_element.add(property_)

    # pass


basyx_aas = convert_pydantic_model_to_aas(example_product)


# aashell_json_string = json.dumps(
#     basyx_aas, cls=basyx.aas.adapter.json.json_serialization.AASToJsonEncoder
# )
# print("\n", aashell_json_string)








    # TODO: transform AAS to pydantic model

