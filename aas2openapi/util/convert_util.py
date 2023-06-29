import json
import re
from basyx.aas import model

from pydantic import BaseModel
import typing


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
    return new_class_name


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
        if isinstance(data_spec, model.DataSpecificationIEC61360):
            for value in data_spec.preferred_name.values():
                if value == "class_name":
                    return data_spec.value


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
        if isinstance(data_spec, model.DataSpecificationIEC61360):
            for value in data_spec.preferred_name.values():
                if value == "attribute_name":
                    return data_spec.value


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
    str_description = str(dict_description)
    return str_description


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
