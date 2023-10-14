from __future__ import annotations

import json
from urllib import parse
from uuid import uuid1

from basyx.aas import model

from typing import Union, Optional, Any
from pydantic import BaseModel, Field
from aas2openapi.util import convert_util

from aas2openapi.models import base
from aas2openapi.util.convert_util import get_vars


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
        id_short=get_id_short(pydantic_aas),
        id_=model.Identifier(pydantic_aas.id_),
        description=convert_util.get_basyx_description_from_pydantic_model(pydantic_aas),
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


def get_id_short(element: Union[base.AAS, base.Submodel, base.SubmodelElementCollection]) -> str:
    if element.id_short:
        return element.id_short
    else:
        return element.id_

def get_semantic_id(pydantic_model: base.Submodel | base.SubmodelElementCollection) -> str | None:
    if pydantic_model.semantic_id:
        semantic_id = model.GlobalReference(
            key=(model.Key(model.KeyTypes.GLOBAL_REFERENCE, pydantic_model.semantic_id), )
        )
    else:
        semantic_id = None
    return semantic_id

def convert_pydantic_model_to_submodel(
    pydantic_submodel: base.Submodel,
) -> model.Submodel:
    basyx_submodel = model.Submodel(
        id_short=get_id_short(pydantic_submodel),
        id_=model.Identifier(pydantic_submodel.id_),
        description=convert_util.get_basyx_description_from_pydantic_model(pydantic_submodel),
        embedded_data_specifications=[
            convert_util.get_data_specification_for_pydantic_model(pydantic_submodel)
        ],
        semantic_id=get_semantic_id(pydantic_submodel),
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
    extend_attribute_name_for_id: bool = False,
) -> model.SubmodelElement:
    """
    Create a basyx SubmodelElement from a pydantic SubmodelElementCollection or a primitive type

    Args:
        attribute_name (str): Name of the attribute that is used for ID and id_short
        attribute_value (Union[ base.SubmodelElementCollection, str, float, int, bool, tuple, list, set ]): Value of the attribute


    Returns:
        model.SubmodelElement: basyx SubmodelElement
    """
    if isinstance(attribute_value, base.SubmodelElementCollection):
        smc = create_submodel_element_collection(attribute_value, attribute_name, extend_attribute_name_for_id)
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
            id_short=get_attribute_id(attribute_name, attribute_value, extend_attribute_name_for_id),
            value=reference,
            embedded_data_specifications=[
                convert_util.get_data_specification_for_attribute_name(attribute_name)
            ],
        )
        return reference_element
    else:
        property = create_property(attribute_name, attribute_value, extend_attribute_name_for_id)

        return property


def get_value_type_of_attribute(
    attribute: Union[str, int, float, bool]
) -> model.datatypes:
    if isinstance(attribute, bool):
        return model.datatypes.Boolean
    elif isinstance(attribute, int):
        return model.datatypes.Integer
    elif isinstance(attribute, float):
        return model.datatypes.Double
    else:
        return model.datatypes.String

def get_attribute_id(attribute_name: str, attribute_value: Any, extend_attribute_name_for_id: bool = False) -> str:
    if extend_attribute_name_for_id:
        id_short = attribute_name + "_" + str(id(attribute_value))
    else:
        id_short = attribute_name
    return id_short

def create_property(
    attribute_name: str, attribute_value: Union[str, int, float, bool],
    extend_attribute_name_for_id: bool = False
) -> model.Property:
    property = model.Property(
        id_short=get_attribute_id(attribute_name, attribute_value, extend_attribute_name_for_id),
        value_type=get_value_type_of_attribute(attribute_value),
        value=attribute_value,
        embedded_data_specifications=[
            convert_util.get_data_specification_for_attribute_name(attribute_name)
        ],
    )
    return property


def create_submodel_element_collection(
    pydantic_submodel_element_collection: base.SubmodelElementCollection, name: str, 
    extend_attribute_name_for_id: bool = False
) -> model.SubmodelElementCollection:
    value = []
    smc_attributes = get_vars(pydantic_submodel_element_collection)

    for attribute_name, attribute_value in smc_attributes.items():
        sme = create_submodel_element(attribute_name, attribute_value)
        value.append(sme)

    id_short = get_id_short(pydantic_submodel_element_collection)
    if extend_attribute_name_for_id:
        id_short = get_attribute_id(id_short, value, extend_attribute_name_for_id)

    smc = model.SubmodelElementCollection(
        id_short=id_short,
        value=value,
        description=convert_util.get_basyx_description_from_pydantic_model(pydantic_submodel_element_collection),
        embedded_data_specifications=[
            convert_util.get_data_specification_for_attribute_name(name)
        ],
        semantic_id=get_semantic_id(pydantic_submodel_element_collection),
    )
    return smc


def create_submodel_element_list(
    name: str, value: list, ordered=True
) -> model.SubmodelElementList:
    submodel_elements = []
    for el in value:
        submodel_element = create_submodel_element(name, el, True)
        submodel_elements.append(submodel_element)

    if isinstance(submodel_elements[0], model.Property):
        value_type_list_element =type(value[0])
    else:
        value_type_list_element = None

    sml = model.SubmodelElementList(
        id_short=name,
        type_value_list_element=type(submodel_elements[0]),
        value_type_list_element=value_type_list_element,
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
        data = rename_data_specifications_for_aas_repository(data)
        data = rename_semantic_id_for_aas_repository(data)
                
        return data
    

def rename_assetKind(data: dict) -> dict:
    if not data["assetInformation"]["assetKind"]:
        raise ValueError("No assetKind found in item:", data)
    if data["assetInformation"]["assetKind"] == "Instance":
        data["assetInformation"]["assetKind"] = AssetInformationAssetKind.INSTANCE
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

def rename_semantic_id_for_aas_repository(dictionary: dict):
    for key, value in dictionary.items():
        if key == "semanticId":
            if value["type"] == "GlobalReference":
                value["type"] = "ExternalReference"
        elif isinstance(value, dict):
            rename_semantic_id_for_aas_repository(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    rename_semantic_id_for_aas_repository(item)
    return dictionary

def rename_data_specifications_for_basyx(dictionary: dict) -> None:
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


def rename_semantic_id_for_basyx(dictionary: dict):
    for key, value in dictionary.items():
        if key == "semanticId":
            if value["type"] == "ExternalReference":
                value["type"] = "GlobalReference"
        elif isinstance(value, dict):
            rename_semantic_id_for_basyx(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    rename_semantic_id_for_basyx(item)
    


def remove_empty_lists(dictionary: dict) -> None:
    keys_to_remove = []
    for key, value in dictionary.items():
        if isinstance(value, dict):
            # Recursively process nested dictionaries
            remove_empty_lists(value)
            # if not value:
            #     keys_to_remove.append(key)
        elif isinstance(value, list) and value:
            # Recursively process nested lists
            for item in value:
                if isinstance(item, dict):
                    remove_empty_lists(item)
        elif isinstance(value, list) and not value:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del dictionary[key]