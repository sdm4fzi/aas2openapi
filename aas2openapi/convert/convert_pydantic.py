from __future__ import annotations

import json
from urllib import parse

from basyx.aas import model

from typing import List, Union

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
    aas: base.AAS,
) -> model.DictObjectStore[model.Identifiable]:
    """
    Convert a pydantic model to an AssetAdministrationShell and return it as a DictObjectStore with all Submodels

    Args:
        pydantic_aas (base.AAS): pydantic model to convert

    Returns:
        model.DictObjectStore[model.Identifiable]: DictObjectStore with all Submodels
    """
    print(aas)
    aas_attributes = get_vars(aas)
    aas_submodels = []  # placeholder for submodels created
    print(aas_attributes)
    for attribute_name, attribute_value in aas_attributes.items():
        if isinstance(attribute_value, base.Submodel):
            print("Create submodel")
            tempsubmodel = create_submodel(
                attribute_name=attribute_name, attribute_value=attribute_value
            )
            aas_submodels.append(tempsubmodel)

    aas = model.AssetAdministrationShell(
        asset_information="lol",
        id_short=aas.id_,
        id_=aas.id_,
        submodel={
            model.ModelReference.from_referable(submodel) for submodel in aas_submodels
        },
    )
    obj_store: model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
    obj_store.add(aas)
    for sm in aas_submodels:
        obj_store.add(sm)
    return obj_store


def get_id_short(
    element: Union[
        base.Submodel, base.SubmodelElementCollection, base.SubmodelElementList
    ]
) -> str:
    if element.id_short:
        return element.id_short
    else:
        return element.id_


def create_submodel(
    attribute_name: str, attribute_value: base.Submodel
) -> model.Submodel:
    submodel = model.Submodel(
        id_short=get_id_short(attribute_value),
        id_=attribute_value.id_,
        description=model.LangStringSet({"en": attribute_value.description})
    )

    submodel_attributes = get_vars(attribute_value)
    print(
        attribute_name,
        "is a submodel with the following attribues:",
        submodel_attributes,
    )

    for sm_attribute_name, sm_attribute_value in submodel_attributes.items():
        submodel_element = create_submodel_element(
            sm_attribute_name, sm_attribute_value, submodel
        )
        submodel.submodel_element.add(submodel_element)
    return submodel


def create_submodel_element(
    attribute_name: str,
    attribute_value: Union[
        base.SubmodelElementCollection, base.SubmodelElementList, str, float, int, bool
    ], submodel: model.Submodel = None,
) -> model.SubmodelElement:
    if isinstance(attribute_value, base.SubmodelElementCollection):
        smc = create_submodel_element_collection(attribute_value, attribute_name)
        print("SMC created", attribute_name)
        return smc
    elif isinstance(attribute_value, list):
        sml = create_submodel_element_list(attribute_name, attribute_value, submodel)
        print("SML created", attribute_name)
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
        )
        print("Reference", attribute_name)
        return reference_element
    else:
        property = create_property(attribute_name, attribute_value)

        print("Property", attribute_name)
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
    print(attribute_name)
    property = model.Property(
        id_short=attribute_name,
        value_type=get_value_type_of_attribute(attribute_value),
        value=attribute_value,
    )
    return property


def create_submodel_element_collection(
    pydantic_submodel_element_collection: base.SubmodelElementCollection, name: str
) -> model.SubmodelElementCollection:
    value = []
    smc_attributes = get_vars(pydantic_submodel_element_collection)
    print(smc_attributes)

    for attribute_name, attribute_value in smc_attributes.items():
        sme = create_submodel_element(attribute_name, attribute_value)
        value.append(sme)

    smc = model.SubmodelElementCollection(
        id_short=name,
        value=value,
    )
    return smc


def create_submodel_element_list(name: str, value: list, submodel: model.Submodel) -> model.SubmodelElementList:
    print(name)
    submodel_elements = []
    for el in value:
        submodel_element = create_submodel_element(name, el, submodel)
        # print(submodel_element)
        # submodel_element.parent = submodel.id_short
        submodel_elements.append(submodel_element)

    sml = model.SubmodelElementList(
        id_short=name,
        type_value_list_element=type(submodel_elements[0]),
        value=submodel_elements,
    )
    return sml
