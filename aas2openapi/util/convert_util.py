import json
import re
from typing import List, Type, Dict
from basyx.aas import model
import ast

from pydantic import BaseModel
import typing

from aas2openapi.models import base


def convert_camel_case_to_underscrore_str(came_case_string: str) -> str:
    """
    Convert a camel case string to an underscore seperated string.

    Args:
        class_name (str): The camel case string to convert.

    Returns:
        str: The underscore seperated string.
    """
    came_case_string = came_case_string[0].lower() + came_case_string[1:]
    new_class_name = re.sub(r"(?<!^)(?=[A-Z])", "_", came_case_string).lower()
    if all(len(el) == 1 for el in new_class_name.split('_')):
        new_class_name = new_class_name.replace('_', '')
    return new_class_name

def convert_under_score_to_camel_case_str(underscore_str: str) -> str:
    """
    Convert a underscore seperated string to a camel case string.

    Args:
        class_name (str): The underscore seperated string to convert.

    Returns:
        str: The camel case string.
    """
    words = underscore_str.split('_')
    camel_case_str = ''.join(word.title() for word in words)
    return camel_case_str


def save_model_list_with_schema(model_list: typing.List[BaseModel], path: str):
    """
    Saves a list of pydantic models to a json file.
    Args:
        model_list (typing.List[base.AAS]): List of pydantic models
        path (str): Path to the json file
    """
    save_dict = {
        "models": [model.dict() for model in model_list],
        "schema": [model.schema() for model in model_list],
    }

    with open(path, "w", encoding="utf-8") as json_file:
        json.dump(save_dict, json_file, indent=4)


def get_class_name_from_basyx_model(item: model.HasDataSpecification) -> str:
    """
    Returns the class name of an basyx model from the data specifications.
    Args:
        item (model.HasDataSpecification): Basyx model to get the class name from
    Returns:
        str: Class name of the basyx model
    """
    if not item.embedded_data_specifications:
        raise ValueError("No data specifications found in item:", item)
    for data_spec in item.embedded_data_specifications:
        content = data_spec.data_specification_content
        if isinstance(content, model.DataSpecificationIEC61360):
            for value in content.preferred_name.values():
                if value == "class_name":
                    return content.value
    raise ValueError("No class name found in item:", item, type(item), item.id_short)


def get_attribute_name_of_basyx_model(item: model.HasDataSpecification) -> str:
    """
    Returns the attribute name of an basyx model from the data specifications. The attribute name is used as the name of the attribute in the pydantic model, required for conversion of references, properties and submodel element lists.
    Args:
        item (model.HasDataSpecification): Basyx model to get the attribute name from
    Raises:
        ValueError: If no data specifications are found in the basyx model
    Returns:
        str: Attribute name of the basyx model
    """
    if not item.embedded_data_specifications:
        raise ValueError("No data specifications found in item:", item)
    for data_spec in item.embedded_data_specifications:
        content = data_spec.data_specification_content
        if isinstance(content, model.DataSpecificationIEC61360):
            for value in content.preferred_name.values():
                if value == "attribute_name":
                    return content.value
    raise ValueError("No attribute name found in item:", item)


def get_str_description(langstring_set: model.LangStringSet) -> str:
    """
    Converts a LangStringSet to a string.
    Args:
        langstring_set (model.LangStringSet): LangStringSet to convert
    Returns:
        str: String representation of the LangStringSet
    """
    if not langstring_set:
        return ""
    dict_description = {}
    for langstring in langstring_set:
        dict_description[langstring] = langstring_set[langstring]
    return str(dict_description)


def get_basyx_description_from_pydantic_model(pydantic_model: base.AAS | base.Submodel | base.SubmodelElementCollection) -> model.LangStringSet:
    """
    Crreates a LangStringSet from a pydantic model.
    Args:
        pydantic_model (BaseModel): Pydantic model that contains the description
    Returns:
        model.LangStringSet: LangStringSet description representation of the pydantic model
    Raises:
        ValueError: If the description of the pydantic model is not a dict or a string
    """
    if not pydantic_model.description:
        return None
    try:
        dict_description = json.loads(pydantic_model.description)
        if not isinstance(dict_description, dict):
            raise ValueError
    except ValueError:
        dict_description = {"en": pydantic_model.description}
    return model.LangStringSet(dict_description)



def get_data_specification_for_pydantic_model(
    pydantic_model: BaseModel,
) -> model.EmbeddedDataSpecification:
    return model.EmbeddedDataSpecification(
        data_specification=model.GlobalReference(
            key=(
                model.Key(
                    type_=model.KeyTypes.GLOBAL_REFERENCE,
                    value=pydantic_model.__class__.__name__,
                ),
            ),
        ),
        data_specification_content=model.DataSpecificationIEC61360(
            preferred_name=model.LangStringSet({"en": "class_name"}),
            value=pydantic_model.__class__.__name__,
        ),
    )


def get_data_specification_for_attribute_name(
    attribute_name: str,
) -> model.EmbeddedDataSpecification:
    return model.EmbeddedDataSpecification(
        data_specification=model.GlobalReference(
            key=(
                model.Key(
                    type_=model.KeyTypes.GLOBAL_REFERENCE,
                    value=attribute_name,
                ),
            ),
        ),
        data_specification_content=model.DataSpecificationIEC61360(
            preferred_name=model.LangStringSet({"en": "attribute_name"}),
            value=attribute_name,
        ),
    )


def get_all_submodels_from_model(model: Type[BaseModel]) -> List[Type[base.Submodel]]:
    """
    Function to get all submodels from a pydantic model
    Args:
        model (Type[BaseModel]): The pydantic model to get the submodels from
    Returns:
        List[Type[model.Submodel]]: A list of all submodel types in the pydantic model
    """
    submodels = []
    for field in model.__fields__.values():
        if issubclass(field.type_, base.Submodel):
            submodels.append(field.type_)
    return submodels


def get_all_submodel_elements_from_submodel(model: Type[base.Submodel]) -> Dict[str, Type[base.SubmodelElementCollection | list | str | bool | float | int]]:
    """
    Function to get all submodel elements from a pydantic submodel

    Args:
        model (Type[BaseModel]): The pydantic submodel to get the submodel elements from

    Returns:
        List[base.SubmodelElementCollection | list | str | bool | float | int]: A list of all submodel elements in the pydantic submodel
    """
    submodel_elements = {}
    for field in model.__fields__.values():
        if field.name != "description" and field.name != "id_short" and field.name != "semantic_id" and field.name != "id_":
            submodel_elements[field.name] = field.type_
    return submodel_elements


def get_all_submodels_from_object_store(
    obj_store: model.DictObjectStore,
) -> List[model.Submodel]:
    """
    Function to get all basyx submodels from an object store
    Args:
        obj_store (model.DictObjectStore): Object store to get submodels from
    Returns:
        List[model.Submodel]: List of basyx submodels
    """
    submodels = []
    for item in obj_store:
        if isinstance(item, model.Submodel):
            submodels.append(item)
    return submodels
