from __future__ import annotations

import json
from urllib import parse

from basyx.aas import model

from typing import Union
from pydantic import BaseModel, Field
from aas2openapi.util import convert_util

from aas2openapi.models import base


def get_vars(obj: object) -> dict:
    vars_dict = vars(obj)
    vars_dict = {key: value for key, value in vars_dict.items() if key[0] != "_"}
    vars_dict = {key: value for key, value in vars_dict.items() if value is not None}
    vars_dict = {key: value for key, value in vars_dict.items() if key != "id_"}
    vars_dict = {key: value for key, value in vars_dict.items() if key != "description"}
    vars_dict = {key: value for key, value in vars_dict.items() if key != "id_short"}
    return vars_dict


def convert_pydantic_model_to_aas(
    pydantic_aas: base.AAS,
) -> model.DictObjectStore[model.Identifiable]:
    """
    Convert a pydantic model to an AssetAdministrationShell and return it as a DictObjectStore with all Submodels

    Args:
        pydantic_aas (base.AAS): pydantic model to convert

    Returns:
        model.DictObjectStore[model.Identifiable]: DictObjectStore with all Submodels
    """
    aas_attributes = get_vars(pydantic_aas)
    aas_submodels = []  # placeholder for submodels created
    for attribute_value in aas_attributes.values():
        if isinstance(attribute_value, base.Submodel):
            tempsubmodel = convert_pydantic_model_to_submodel(
                pydantic_submodel=attribute_value
            )
            aas_submodels.append(tempsubmodel)

    asset_information = model.AssetInformation()

    basyx_aas = model.AssetAdministrationShell(
        asset_information=asset_information,
        id_short=pydantic_aas.id_short,
        id_=model.Identifier(pydantic_aas.id_),
        submodel={
            model.ModelReference.from_referable(submodel) for submodel in aas_submodels
        },
        embedded_data_specifications=[
            convert_util.get_data_specification_for_pydantic_model(pydantic_aas)
        ],
    )
    obj_store: model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
    obj_store.add(basyx_aas)
    for sm in aas_submodels:
        obj_store.add(sm)
    return obj_store


def get_id_short(element: Union[base.Submodel, base.SubmodelElementCollection]) -> str:
    if element.id_short:
        return element.id_short
    else:
        return element.id_


def convert_pydantic_model_to_submodel(
    pydantic_submodel: base.Submodel,
) -> model.Submodel:
    basyx_submodel = model.Submodel(
        id_short=get_id_short(pydantic_submodel),
        id_=model.Identifier(pydantic_submodel.id_),
        description=model.LangStringSet({"en": pydantic_submodel.description}),
        embedded_data_specifications=[
            convert_util.get_data_specification_for_pydantic_model(pydantic_submodel)
        ],
    )

    submodel_attributes = get_vars(pydantic_submodel)

    for sm_attribute_name, sm_attribute_value in submodel_attributes.items():
        submodel_element = create_submodel_element(
            sm_attribute_name, sm_attribute_value
        )
        basyx_submodel.submodel_element.add(submodel_element)
    return basyx_submodel


def create_submodel_element(
    attribute_name: str,
    attribute_value: Union[
        base.SubmodelElementCollection, str, float, int, bool, tuple, list, set
    ],
) -> model.SubmodelElement:
    if isinstance(attribute_value, base.SubmodelElementCollection):
        smc = create_submodel_element_collection(attribute_value, attribute_name)
        return smc
    elif isinstance(attribute_value, list) or isinstance(attribute_value, tuple):
        sml = create_submodel_element_list(attribute_name, attribute_value)
        return sml
    elif isinstance(attribute_value, set):
        sml = create_submodel_element_list(
            attribute_name, attribute_value, ordered=False
        )
        return sml
    elif (isinstance(attribute_value, str)) and (
        (
            parse.urlparse(attribute_value).scheme
            and parse.urlparse(attribute_value).netloc
        )
        or (attribute_value.split("_")[-1] in ["id", "ids"])
    ):
        key = model.Key(
            type_=model.KeyTypes.ASSET_ADMINISTRATION_SHELL,
            value=attribute_value,
        )
        reference = model.ModelReference(key=(key,), type_="")
        reference_element = model.ReferenceElement(
            id_short=attribute_name,
            value=reference,
            embedded_data_specifications=[
                convert_util.get_data_specification_for_attribute_name(attribute_name)
            ],
        )
        return reference_element
    else:
        property = create_property(attribute_name, attribute_value)

        return property


def get_value_type_of_attribute(
    attribute: Union[str, int, float, bool]
) -> model.datatypes:
    if isinstance(attribute, int):
        return model.datatypes.Integer
    elif isinstance(attribute, float):
        return model.datatypes.Double
    elif isinstance(attribute, bool):
        return model.datatypes.Boolean
    else:
        return model.datatypes.String


def create_property(
    attribute_name: str, attribute_value: Union[str, int, float, bool]
) -> model.Property:
    property = model.Property(
        id_short=attribute_name,
        value_type=get_value_type_of_attribute(attribute_value),
        value=attribute_value,
        embedded_data_specifications=[
            convert_util.get_data_specification_for_attribute_name(attribute_name)
        ],
    )
    return property


def create_submodel_element_collection(
    pydantic_submodel_element_collection: base.SubmodelElementCollection, name: str
) -> model.SubmodelElementCollection:
    value = []
    smc_attributes = get_vars(pydantic_submodel_element_collection)

    for attribute_name, attribute_value in smc_attributes.items():
        sme = create_submodel_element(attribute_name, attribute_value)
        value.append(sme)

    smc = model.SubmodelElementCollection(
        id_short=pydantic_submodel_element_collection.id_short,
        value=value,
        embedded_data_specifications=[
            convert_util.get_data_specification_for_attribute_name(name)
        ],
    )
    return smc


def create_submodel_element_list(
    name: str, value: list, ordered=True
) -> model.SubmodelElementList:
    submodel_elements = []
    for el in value:
        submodel_element = create_submodel_element(name, el)
        submodel_elements.append(submodel_element)

    sml = model.SubmodelElementList(
        id_short=name,
        type_value_list_element=type(submodel_elements[0]),
        value=submodel_elements,
        order_relevant=ordered,
        embedded_data_specifications=[
            convert_util.get_data_specification_for_attribute_name(name)
        ],
    )
    return sml


from ba_syx_aas_repository_client.models import (
    AssetInformationAssetKind,
)
import basyx.aas.adapter.json.json_serialization


class ClientModel(BaseModel):
    basyx_object: Union[model.AssetAdministrationShell, model.Submodel]

    class Config:
        arbitrary_types_allowed = True

    def to_dict(self) -> dict:
        basyx_json_string = json.dumps(
            self.basyx_object, cls=basyx.aas.adapter.json.AASToJsonEncoder
        )
        data: dict = json.loads(basyx_json_string)
        # if isinstance(self.basyx_object, model.AssetAdministrationShell):
        #     data = rename_assetKind(data)
        data = rename_data_specifications_for_aas_repository(data)
                
        return data
    

def rename_assetKind(data: dict) -> dict:
    if not data["assetInformation"]["assetKind"]:
        raise ValueError("No assetKind found in item:", data)
    if data["assetInformation"]["assetKind"] == "Instance":
        data["assetInformation"]["assetKind"] = AssetInformationAssetKind.INSTANCE
        print("renamed assetKind to", data["assetInformation"]["assetKind"])
    elif data["assetInformation"]["assetKind"] == "Type":
        data["assetInformation"]["assetKind"] = AssetInformationAssetKind.TYPE
    return data

def rename_data_specifications_for_aas_repository(dictionary: dict):
    for key, value in dictionary.items():
        if key == "embeddedDataSpecifications":
            for data_spec in value:
                if data_spec["dataSpecification"]["type"] == "GlobalReference":
                    data_spec["dataSpecification"]["type"] = "ExternalReference"
                if data_spec["dataSpecificationContent"]["modelType"] == "DataSpecificationIEC61360":
                    data_spec["dataSpecificationContent"]["modelType"] = "DataSpecificationIec61360"
        elif isinstance(value, dict):
            rename_data_specifications_for_aas_repository(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    rename_data_specifications_for_aas_repository(item)
    return dictionary

def rename_data_specifications_for_basyx(dictionary: dict):
    for key, value in dictionary.items():
        if key == "embeddedDataSpecifications":
            for data_spec in value:
                if data_spec["dataSpecification"]["type"] == "ExternalReference":
                    data_spec["dataSpecification"]["type"] = "GlobalReference"
                if data_spec["dataSpecificationContent"]["modelType"] == "DataSpecificationIec61360":
                    data_spec["dataSpecificationContent"]["modelType"] = "DataSpecificationIEC61360"
        elif isinstance(value, dict):
            rename_data_specifications_for_basyx(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    rename_data_specifications_for_basyx(item)
    return dictionary
