from basyx.aas import model
from  basyx.aas.adapter.json import write_aas_json_file
import json

from aas2openapi import convert_object_store_to_pydantic_models

submodel_elements = []

# TODO: rework data specification to IEC be as content and not specification itself

property_1_data_specification_content = model.DataSpecificationIEC61360(
    preferred_name=model.LangStringSet({"en": "attribute_name"}),
    value="property_1_attribute_name",
)

property_1_data_specification = model.EmbeddedDataSpecification(
    data_specification=model.GlobalReference(
        key=(
            model.Key(
                type_=model.KeyTypes.GLOBAL_REFERENCE,
                value="http://example.com/property1semantics",
            ),
        ),
    ),
    data_specification_content=property_1_data_specification_content,
)


submodel_elements.append(
    model.Property(
        id_short="property1",
        value_type=model.datatypes.String,
        value="value1",
        embedded_data_specifications=[property_1_data_specification]

    )
)

property_2_data_specification = model.DataSpecificationIEC61360(
    preferred_name=model.LangStringSet({"en": "attribute_name"}),
    value="property_2_attribute_name",
)

submodel_elements.append(
    model.Property(
        id_short="property2",
        value_type=model.datatypes.Int,
        value=2,
        embedded_data_specifications=[property_2_data_specification]      
    )   
)

sec_data_specification = model.DataSpecificationIEC61360(
    preferred_name=model.LangStringSet({"en": "class_name"}),
    value="SmeClassName",
)

property_3_data_specification = model.DataSpecificationIEC61360(
    preferred_name=model.LangStringSet({"en": "attribute_name"}),
    value="property_3_attribute_name",
)

property_4_data_specification = model.DataSpecificationIEC61360(
    preferred_name=model.LangStringSet({"en": "attribute_name"}),
    value="property_4_attribute_name",
)


submodel_elements.append(
    model.SubmodelElementCollection(
        id_short="submodel_element_collection1",
        value=[
            model.Property(
                id_short="property3",
                value_type=model.datatypes.String,
                value="value3",
                embedded_data_specifications=[property_3_data_specification]
            ),
            model.Property(
                id_short="property4",
                value_type=model.datatypes.Int,
                value=4,
                embedded_data_specifications=[property_4_data_specification]
            ),
        ],
        embedded_data_specifications=[sec_data_specification]
    )
)

sm_data_specification = model.DataSpecificationIEC61360(
    preferred_name=model.LangStringSet({"en": "class_name"}),
    value="SmClassName",
)


submodel = model.Submodel(
    id_=model.Identifier("http://example.com/submodel1"),
    id_short="submodel1",
    semantic_id=model.GlobalReference(
        key=[model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value="http://example.com/submodel1semantics"
        )]),
    description=model.LangStringSet({"en": "This is a submodel"}),
    submodel_element=submodel_elements,
    embedded_data_specifications=[sm_data_specification]
)

property_5_data_specification = model.DataSpecificationIEC61360(
    preferred_name=model.LangStringSet({"en": "attribute_name"}),
    value="property_5_attribute_name",
)

property_6_data_specification = model.DataSpecificationIEC61360(
    preferred_name=model.LangStringSet({"en": "attribute_name"}),
    value="property_6_attribute_name",
)

submodel_elements_list_data_specification = model.DataSpecificationIEC61360(
    preferred_name=model.LangStringSet({"en": "attribute_name"}),
    value="SubmodelElementListClassName",
)

submodel_elements2 = []
submodel_elements2.append(
    model.SubmodelElementList(
        id_short="submodel_element_list1",
        type_value_list_element=model.Property,
        value_type_list_element=model.datatypes.String,
        value=[
            model.Property(
                id_short="property5",
                value_type=model.datatypes.String,
                value="value5",
                embedded_data_specifications=[property_5_data_specification]
            ),
            model.Property(
                id_short="property6",
                value_type=model.datatypes.String,
                value="value7",
                embedded_data_specifications=[property_6_data_specification]
            ),
        ],
        order_relevant=True,
        embedded_data_specifications=[submodel_elements_list_data_specification]  
    )
)

embedded_data_specification = model.DataSpecificationIEC61360(
    preferred_name=model.LangStringSet({"en": "attribute_name"}),
    value="reference_element1_attribute_name",
)

submodel_elements2.append(
    model.ReferenceElement(
        id_short="reference_element1",
        value=model.ModelReference.from_referable(submodel),
        embedded_data_specifications=[embedded_data_specification]
    )
)

sm2_data_specification_content = model.DataSpecificationIEC61360(
    preferred_name=model.LangStringSet({"en": "class_name"}),
    value="Sm2ClassName",
)

sm2_data_specification = model.EmbeddedDataSpecification(
    data_specification=model.GlobalReference(
        key=(
            model.Key(
                type_=model.KeyTypes.GLOBAL_REFERENCE,
                value="http://example.com/sm2semantics",
            ),
        ),
    ),
    data_specification_content=sm2_data_specification_content,
)

submodel2 = model.Submodel(
    id_=model.Identifier("http://example.com/submodel2"),
    id_short="submodel2",
    description=model.LangStringSet({"en": "This is a submodel"}),
    submodel_element=submodel_elements2,
    embedded_data_specifications=[sm2_data_specification]
)

aas_data_specification_content = model.DataSpecificationIEC61360(
    preferred_name=model.LangStringSet({"en": "class_name"}),
    value="AasClassName",
)

aas_data_specification = model.EmbeddedDataSpecification(
    data_specification=model.GlobalReference(
        key=(
            model.Key(
                type_=model.KeyTypes.GLOBAL_REFERENCE,
                value="http://example.com/aassemantics",
            ),
        ),
    ),
    data_specification_content=aas_data_specification_content,
)

aas = model.AssetAdministrationShell(
    asset_information=model.AssetInformation(),
    id_=model.Identifier("http://example.com/asset1"),
    id_short="asset1",
    submodel={
        model.ModelReference.from_referable(submodel),
        model.ModelReference.from_referable(submodel2)
    },
    embedded_data_specifications=[aas_data_specification]
)

obj_store: model.DictObjectStore[model.Identifiable] = model.DictObjectStore(
    [
        aas, submodel, submodel2
    ]
)

aas_list = convert_object_store_to_pydantic_models(obj_store)
with open("examples/created_model_data_from_aas.json", "w", encoding="utf-8") as json_file:
    json.dump({"aas_list": [aas.dict() for aas in aas_list]}, json_file, indent=4)

from aas2openapi.util.convert_util import save_model_list_with_schema

save_model_list_with_schema(aas_list, "examples/created_model_data_and_schema_from_aas.json")
