from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.embedded_data_specification import EmbeddedDataSpecification
    from ..models.extension import Extension
    from ..models.lang_string_name_type import LangStringNameType
    from ..models.lang_string_text_type import LangStringTextType
    from ..models.operation_variable import OperationVariable
    from ..models.qualifier import Qualifier
    from ..models.reference import Reference


T = TypeVar("T", bound="Operation")


@attr.s(auto_attribs=True)
class Operation:
    """
    Attributes:
        supplemental_semantic_ids (Union[Unset, List['Reference']]):
        qualifiers (Union[Unset, List['Qualifier']]):
        category (Union[Unset, str]):
        id_short (Union[Unset, str]):
        extensions (Union[Unset, List['Extension']]):
        embedded_data_specifications (Union[Unset, List['EmbeddedDataSpecification']]):
        semantic_id (Union[Unset, Reference]):
        display_name (Union[Unset, List['LangStringNameType']]):
        description (Union[Unset, List['LangStringTextType']]):
        input_variables (Union[Unset, List['OperationVariable']]):
        output_variables (Union[Unset, List['OperationVariable']]):
        inoutput_variables (Union[Unset, List['OperationVariable']]):
    """

    supplemental_semantic_ids: Union[Unset, List["Reference"]] = UNSET
    qualifiers: Union[Unset, List["Qualifier"]] = UNSET
    category: Union[Unset, str] = UNSET
    id_short: Union[Unset, str] = UNSET
    extensions: Union[Unset, List["Extension"]] = UNSET
    embedded_data_specifications: Union[Unset, List["EmbeddedDataSpecification"]] = UNSET
    semantic_id: Union[Unset, "Reference"] = UNSET
    display_name: Union[Unset, List["LangStringNameType"]] = UNSET
    description: Union[Unset, List["LangStringTextType"]] = UNSET
    input_variables: Union[Unset, List["OperationVariable"]] = UNSET
    output_variables: Union[Unset, List["OperationVariable"]] = UNSET
    inoutput_variables: Union[Unset, List["OperationVariable"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        supplemental_semantic_ids: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.supplemental_semantic_ids, Unset):
            supplemental_semantic_ids = []
            for supplemental_semantic_ids_item_data in self.supplemental_semantic_ids:
                supplemental_semantic_ids_item = supplemental_semantic_ids_item_data.to_dict()

                supplemental_semantic_ids.append(supplemental_semantic_ids_item)

        qualifiers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.qualifiers, Unset):
            qualifiers = []
            for qualifiers_item_data in self.qualifiers:
                qualifiers_item = qualifiers_item_data.to_dict()

                qualifiers.append(qualifiers_item)

        category = self.category
        id_short = self.id_short
        extensions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.extensions, Unset):
            extensions = []
            for extensions_item_data in self.extensions:
                extensions_item = extensions_item_data.to_dict()

                extensions.append(extensions_item)

        embedded_data_specifications: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.embedded_data_specifications, Unset):
            embedded_data_specifications = []
            for embedded_data_specifications_item_data in self.embedded_data_specifications:
                embedded_data_specifications_item = embedded_data_specifications_item_data.to_dict()

                embedded_data_specifications.append(embedded_data_specifications_item)

        semantic_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.semantic_id, Unset):
            semantic_id = self.semantic_id.to_dict()

        display_name: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.display_name, Unset):
            display_name = []
            for display_name_item_data in self.display_name:
                display_name_item = display_name_item_data.to_dict()

                display_name.append(display_name_item)

        description: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.description, Unset):
            description = []
            for description_item_data in self.description:
                description_item = description_item_data.to_dict()

                description.append(description_item)

        input_variables: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.input_variables, Unset):
            input_variables = []
            for input_variables_item_data in self.input_variables:
                input_variables_item = input_variables_item_data.to_dict()

                input_variables.append(input_variables_item)

        output_variables: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.output_variables, Unset):
            output_variables = []
            for output_variables_item_data in self.output_variables:
                output_variables_item = output_variables_item_data.to_dict()

                output_variables.append(output_variables_item)

        inoutput_variables: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.inoutput_variables, Unset):
            inoutput_variables = []
            for inoutput_variables_item_data in self.inoutput_variables:
                inoutput_variables_item = inoutput_variables_item_data.to_dict()

                inoutput_variables.append(inoutput_variables_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if supplemental_semantic_ids is not UNSET:
            field_dict["supplementalSemanticIds"] = supplemental_semantic_ids
        if qualifiers is not UNSET:
            field_dict["qualifiers"] = qualifiers
        if category is not UNSET:
            field_dict["category"] = category
        if id_short is not UNSET:
            field_dict["idShort"] = id_short
        if extensions is not UNSET:
            field_dict["extensions"] = extensions
        if embedded_data_specifications is not UNSET:
            field_dict["embeddedDataSpecifications"] = embedded_data_specifications
        if semantic_id is not UNSET:
            field_dict["semanticId"] = semantic_id
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if input_variables is not UNSET:
            field_dict["inputVariables"] = input_variables
        if output_variables is not UNSET:
            field_dict["outputVariables"] = output_variables
        if inoutput_variables is not UNSET:
            field_dict["inoutputVariables"] = inoutput_variables

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.embedded_data_specification import EmbeddedDataSpecification
        from ..models.extension import Extension
        from ..models.lang_string_name_type import LangStringNameType
        from ..models.lang_string_text_type import LangStringTextType
        from ..models.operation_variable import OperationVariable
        from ..models.qualifier import Qualifier
        from ..models.reference import Reference

        d = src_dict.copy()
        supplemental_semantic_ids = []
        _supplemental_semantic_ids = d.pop("supplementalSemanticIds", UNSET)
        for supplemental_semantic_ids_item_data in _supplemental_semantic_ids or []:
            supplemental_semantic_ids_item = Reference.from_dict(supplemental_semantic_ids_item_data)

            supplemental_semantic_ids.append(supplemental_semantic_ids_item)

        qualifiers = []
        _qualifiers = d.pop("qualifiers", UNSET)
        for qualifiers_item_data in _qualifiers or []:
            qualifiers_item = Qualifier.from_dict(qualifiers_item_data)

            qualifiers.append(qualifiers_item)

        category = d.pop("category", UNSET)

        id_short = d.pop("idShort", UNSET)

        extensions = []
        _extensions = d.pop("extensions", UNSET)
        for extensions_item_data in _extensions or []:
            extensions_item = Extension.from_dict(extensions_item_data)

            extensions.append(extensions_item)

        embedded_data_specifications = []
        _embedded_data_specifications = d.pop("embeddedDataSpecifications", UNSET)
        for embedded_data_specifications_item_data in _embedded_data_specifications or []:
            embedded_data_specifications_item = EmbeddedDataSpecification.from_dict(
                embedded_data_specifications_item_data
            )

            embedded_data_specifications.append(embedded_data_specifications_item)

        _semantic_id = d.pop("semanticId", UNSET)
        semantic_id: Union[Unset, Reference]
        if isinstance(_semantic_id, Unset):
            semantic_id = UNSET
        else:
            semantic_id = Reference.from_dict(_semantic_id)

        display_name = []
        _display_name = d.pop("displayName", UNSET)
        for display_name_item_data in _display_name or []:
            display_name_item = LangStringNameType.from_dict(display_name_item_data)

            display_name.append(display_name_item)

        description = []
        _description = d.pop("description", UNSET)
        for description_item_data in _description or []:
            description_item = LangStringTextType.from_dict(description_item_data)

            description.append(description_item)

        input_variables = []
        _input_variables = d.pop("inputVariables", UNSET)
        for input_variables_item_data in _input_variables or []:
            input_variables_item = OperationVariable.from_dict(input_variables_item_data)

            input_variables.append(input_variables_item)

        output_variables = []
        _output_variables = d.pop("outputVariables", UNSET)
        for output_variables_item_data in _output_variables or []:
            output_variables_item = OperationVariable.from_dict(output_variables_item_data)

            output_variables.append(output_variables_item)

        inoutput_variables = []
        _inoutput_variables = d.pop("inoutputVariables", UNSET)
        for inoutput_variables_item_data in _inoutput_variables or []:
            inoutput_variables_item = OperationVariable.from_dict(inoutput_variables_item_data)

            inoutput_variables.append(inoutput_variables_item)

        operation = cls(
            supplemental_semantic_ids=supplemental_semantic_ids,
            qualifiers=qualifiers,
            category=category,
            id_short=id_short,
            extensions=extensions,
            embedded_data_specifications=embedded_data_specifications,
            semantic_id=semantic_id,
            display_name=display_name,
            description=description,
            input_variables=input_variables,
            output_variables=output_variables,
            inoutput_variables=inoutput_variables,
        )

        operation.additional_properties = d
        return operation

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
