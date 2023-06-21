from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.embedded_data_specification import EmbeddedDataSpecification
    from ..models.extension import Extension
    from ..models.lang_string_name_type import LangStringNameType
    from ..models.lang_string_text_type import LangStringTextType
    from ..models.qualifier import Qualifier
    from ..models.reference import Reference


T = TypeVar("T", bound="SubmodelElement")


@attr.s(auto_attribs=True)
class SubmodelElement:
    """
    Attributes:
        embedded_data_specifications (Union[Unset, List['EmbeddedDataSpecification']]):
        semantic_id (Union[Unset, Reference]):
        supplemental_semantic_ids (Union[Unset, List['Reference']]):
        display_name (Union[Unset, List['LangStringNameType']]):
        description (Union[Unset, List['LangStringTextType']]):
        id_short (Union[Unset, str]):
        category (Union[Unset, str]):
        extensions (Union[Unset, List['Extension']]):
        qualifiers (Union[Unset, List['Qualifier']]):
    """

    embedded_data_specifications: Union[Unset, List["EmbeddedDataSpecification"]] = UNSET
    semantic_id: Union[Unset, "Reference"] = UNSET
    supplemental_semantic_ids: Union[Unset, List["Reference"]] = UNSET
    display_name: Union[Unset, List["LangStringNameType"]] = UNSET
    description: Union[Unset, List["LangStringTextType"]] = UNSET
    id_short: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    extensions: Union[Unset, List["Extension"]] = UNSET
    qualifiers: Union[Unset, List["Qualifier"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        embedded_data_specifications: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.embedded_data_specifications, Unset):
            embedded_data_specifications = []
            for embedded_data_specifications_item_data in self.embedded_data_specifications:
                embedded_data_specifications_item = embedded_data_specifications_item_data.to_dict()

                embedded_data_specifications.append(embedded_data_specifications_item)

        semantic_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.semantic_id, Unset):
            semantic_id = self.semantic_id.to_dict()

        supplemental_semantic_ids: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.supplemental_semantic_ids, Unset):
            supplemental_semantic_ids = []
            for supplemental_semantic_ids_item_data in self.supplemental_semantic_ids:
                supplemental_semantic_ids_item = supplemental_semantic_ids_item_data.to_dict()

                supplemental_semantic_ids.append(supplemental_semantic_ids_item)

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

        id_short = self.id_short
        category = self.category
        extensions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.extensions, Unset):
            extensions = []
            for extensions_item_data in self.extensions:
                extensions_item = extensions_item_data.to_dict()

                extensions.append(extensions_item)

        qualifiers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.qualifiers, Unset):
            qualifiers = []
            for qualifiers_item_data in self.qualifiers:
                qualifiers_item = qualifiers_item_data.to_dict()

                qualifiers.append(qualifiers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if embedded_data_specifications is not UNSET:
            field_dict["embeddedDataSpecifications"] = embedded_data_specifications
        if semantic_id is not UNSET:
            field_dict["semanticID"] = semantic_id
        if supplemental_semantic_ids is not UNSET:
            field_dict["supplementalSemanticIds"] = supplemental_semantic_ids
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if id_short is not UNSET:
            field_dict["idShort"] = id_short
        if category is not UNSET:
            field_dict["category"] = category
        if extensions is not UNSET:
            field_dict["extensions"] = extensions
        if qualifiers is not UNSET:
            field_dict["qualifiers"] = qualifiers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.embedded_data_specification import EmbeddedDataSpecification
        from ..models.extension import Extension
        from ..models.lang_string_name_type import LangStringNameType
        from ..models.lang_string_text_type import LangStringTextType
        from ..models.qualifier import Qualifier
        from ..models.reference import Reference

        d = src_dict.copy()
        embedded_data_specifications = []
        _embedded_data_specifications = d.pop("embeddedDataSpecifications", UNSET)
        for embedded_data_specifications_item_data in _embedded_data_specifications or []:
            embedded_data_specifications_item = EmbeddedDataSpecification.from_dict(
                embedded_data_specifications_item_data
            )

            embedded_data_specifications.append(embedded_data_specifications_item)

        _semantic_id = d.pop("semanticID", UNSET)
        semantic_id: Union[Unset, Reference]
        if isinstance(_semantic_id, Unset):
            semantic_id = UNSET
        else:
            semantic_id = Reference.from_dict(_semantic_id)

        supplemental_semantic_ids = []
        _supplemental_semantic_ids = d.pop("supplementalSemanticIds", UNSET)
        for supplemental_semantic_ids_item_data in _supplemental_semantic_ids or []:
            supplemental_semantic_ids_item = Reference.from_dict(supplemental_semantic_ids_item_data)

            supplemental_semantic_ids.append(supplemental_semantic_ids_item)

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

        id_short = d.pop("idShort", UNSET)

        category = d.pop("category", UNSET)

        extensions = []
        _extensions = d.pop("extensions", UNSET)
        for extensions_item_data in _extensions or []:
            extensions_item = Extension.from_dict(extensions_item_data)

            extensions.append(extensions_item)

        qualifiers = []
        _qualifiers = d.pop("qualifiers", UNSET)
        for qualifiers_item_data in _qualifiers or []:
            qualifiers_item = Qualifier.from_dict(qualifiers_item_data)

            qualifiers.append(qualifiers_item)

        submodel_element = cls(
            embedded_data_specifications=embedded_data_specifications,
            semantic_id=semantic_id,
            supplemental_semantic_ids=supplemental_semantic_ids,
            display_name=display_name,
            description=description,
            id_short=id_short,
            category=category,
            extensions=extensions,
            qualifiers=qualifiers,
        )

        submodel_element.additional_properties = d
        return submodel_element

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
