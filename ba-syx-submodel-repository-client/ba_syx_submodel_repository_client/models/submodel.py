from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.submodel_kind import SubmodelKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.administrative_information import AdministrativeInformation
    from ..models.embedded_data_specification import EmbeddedDataSpecification
    from ..models.extension import Extension
    from ..models.lang_string_name_type import LangStringNameType
    from ..models.lang_string_text_type import LangStringTextType
    from ..models.qualifier import Qualifier
    from ..models.reference import Reference
    from ..models.submodel_element import SubmodelElement


T = TypeVar("T", bound="Submodel")


@attr.s(auto_attribs=True)
class Submodel:
    """
    Attributes:
        submodel_elements (Union[Unset, List['SubmodelElement']]):
        kind (Union[Unset, SubmodelKind]):
        supplemental_semantic_ids (Union[Unset, List['Reference']]):
        id (Union[Unset, str]):
        administration (Union[Unset, AdministrativeInformation]):
        category (Union[Unset, str]):
        extensions (Union[Unset, List['Extension']]):
        qualifiers (Union[Unset, List['Qualifier']]):
        display_name (Union[Unset, List['LangStringNameType']]):
        description (Union[Unset, List['LangStringTextType']]):
        id_short (Union[Unset, str]):
        embedded_data_specifications (Union[Unset, List['EmbeddedDataSpecification']]):
        semantic_id (Union[Unset, Reference]):
    """

    submodel_elements: Union[Unset, List["SubmodelElement"]] = UNSET
    kind: Union[Unset, SubmodelKind] = UNSET
    supplemental_semantic_ids: Union[Unset, List["Reference"]] = UNSET
    id: Union[Unset, str] = UNSET
    administration: Union[Unset, "AdministrativeInformation"] = UNSET
    category: Union[Unset, str] = UNSET
    extensions: Union[Unset, List["Extension"]] = UNSET
    qualifiers: Union[Unset, List["Qualifier"]] = UNSET
    display_name: Union[Unset, List["LangStringNameType"]] = UNSET
    description: Union[Unset, List["LangStringTextType"]] = UNSET
    id_short: Union[Unset, str] = UNSET
    embedded_data_specifications: Union[Unset, List["EmbeddedDataSpecification"]] = UNSET
    semantic_id: Union[Unset, "Reference"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        submodel_elements: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.submodel_elements, Unset):
            submodel_elements = []
            for submodel_elements_item_data in self.submodel_elements:
                submodel_elements_item = submodel_elements_item_data.to_dict()

                submodel_elements.append(submodel_elements_item)

        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        supplemental_semantic_ids: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.supplemental_semantic_ids, Unset):
            supplemental_semantic_ids = []
            for supplemental_semantic_ids_item_data in self.supplemental_semantic_ids:
                supplemental_semantic_ids_item = supplemental_semantic_ids_item_data.to_dict()

                supplemental_semantic_ids.append(supplemental_semantic_ids_item)

        id = self.id
        administration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.administration, Unset):
            administration = self.administration.to_dict()

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
        embedded_data_specifications: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.embedded_data_specifications, Unset):
            embedded_data_specifications = []
            for embedded_data_specifications_item_data in self.embedded_data_specifications:
                embedded_data_specifications_item = embedded_data_specifications_item_data.to_dict()

                embedded_data_specifications.append(embedded_data_specifications_item)

        semantic_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.semantic_id, Unset):
            semantic_id = self.semantic_id.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if submodel_elements is not UNSET:
            field_dict["submodelElements"] = submodel_elements
        if kind is not UNSET:
            field_dict["kind"] = kind
        if supplemental_semantic_ids is not UNSET:
            field_dict["supplementalSemanticIds"] = supplemental_semantic_ids
        if id is not UNSET:
            field_dict["id"] = id
        if administration is not UNSET:
            field_dict["administration"] = administration
        if category is not UNSET:
            field_dict["category"] = category
        if extensions is not UNSET:
            field_dict["extensions"] = extensions
        if qualifiers is not UNSET:
            field_dict["qualifiers"] = qualifiers
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if id_short is not UNSET:
            field_dict["idShort"] = id_short
        if embedded_data_specifications is not UNSET:
            field_dict["embeddedDataSpecifications"] = embedded_data_specifications
        if semantic_id is not UNSET:
            field_dict["semanticId"] = semantic_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.administrative_information import AdministrativeInformation
        from ..models.embedded_data_specification import EmbeddedDataSpecification
        from ..models.extension import Extension
        from ..models.lang_string_name_type import LangStringNameType
        from ..models.lang_string_text_type import LangStringTextType
        from ..models.qualifier import Qualifier
        from ..models.reference import Reference
        from ..models.submodel_element import SubmodelElement

        d = src_dict.copy()
        submodel_elements = []
        _submodel_elements = d.pop("submodelElements", UNSET)
        for submodel_elements_item_data in _submodel_elements or []:
            submodel_elements_item = SubmodelElement.from_dict(submodel_elements_item_data)

            submodel_elements.append(submodel_elements_item)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, SubmodelKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = SubmodelKind(_kind)

        supplemental_semantic_ids = []
        _supplemental_semantic_ids = d.pop("supplementalSemanticIds", UNSET)
        for supplemental_semantic_ids_item_data in _supplemental_semantic_ids or []:
            supplemental_semantic_ids_item = Reference.from_dict(supplemental_semantic_ids_item_data)

            supplemental_semantic_ids.append(supplemental_semantic_ids_item)

        id = d.pop("id", UNSET)

        _administration = d.pop("administration", UNSET)
        administration: Union[Unset, AdministrativeInformation]
        if isinstance(_administration, Unset):
            administration = UNSET
        else:
            administration = AdministrativeInformation.from_dict(_administration)

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

        submodel = cls(
            submodel_elements=submodel_elements,
            kind=kind,
            supplemental_semantic_ids=supplemental_semantic_ids,
            id=id,
            administration=administration,
            category=category,
            extensions=extensions,
            qualifiers=qualifiers,
            display_name=display_name,
            description=description,
            id_short=id_short,
            embedded_data_specifications=embedded_data_specifications,
            semantic_id=semantic_id,
        )

        submodel.additional_properties = d
        return submodel

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
