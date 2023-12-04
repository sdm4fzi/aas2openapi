from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.administrative_information import AdministrativeInformation
    from ..models.asset_information import AssetInformation
    from ..models.embedded_data_specification import EmbeddedDataSpecification
    from ..models.extension import Extension
    from ..models.lang_string_name_type import LangStringNameType
    from ..models.lang_string_text_type import LangStringTextType
    from ..models.reference import Reference


T = TypeVar("T", bound="AssetAdministrationShell")


@attr.s(auto_attribs=True)
class AssetAdministrationShell:
    """
    Attributes:
        asset_information (Union[Unset, AssetInformation]):
        derived_from (Union[Unset, Reference]):
        submodels (Union[Unset, List['Reference']]):
        id (Union[Unset, str]):
        administration (Union[Unset, AdministrativeInformation]):
        category (Union[Unset, str]):
        id_short (Union[Unset, str]):
        extensions (Union[Unset, List['Extension']]):
        embedded_data_specifications (Union[Unset, List['EmbeddedDataSpecification']]):
        display_name (Union[Unset, List['LangStringNameType']]):
        description (Union[Unset, List['LangStringTextType']]):
    """

    asset_information: Union[Unset, "AssetInformation"] = UNSET
    derived_from: Union[Unset, "Reference"] = UNSET
    submodels: Union[Unset, List["Reference"]] = UNSET
    id: Union[Unset, str] = UNSET
    administration: Union[Unset, "AdministrativeInformation"] = UNSET
    category: Union[Unset, str] = UNSET
    id_short: Union[Unset, str] = UNSET
    extensions: Union[Unset, List["Extension"]] = UNSET
    embedded_data_specifications: Union[Unset, List["EmbeddedDataSpecification"]] = UNSET
    display_name: Union[Unset, List["LangStringNameType"]] = UNSET
    description: Union[Unset, List["LangStringTextType"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        asset_information: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.asset_information, Unset):
            asset_information = self.asset_information.to_dict()

        derived_from: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.derived_from, Unset):
            derived_from = self.derived_from.to_dict()

        submodels: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.submodels, Unset):
            submodels = []
            for submodels_item_data in self.submodels:
                submodels_item = submodels_item_data.to_dict()

                submodels.append(submodels_item)

        id = self.id
        administration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.administration, Unset):
            administration = self.administration.to_dict()

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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if asset_information is not UNSET:
            field_dict["assetInformation"] = asset_information
        if derived_from is not UNSET:
            field_dict["derivedFrom"] = derived_from
        if submodels is not UNSET:
            field_dict["submodels"] = submodels
        if id is not UNSET:
            field_dict["id"] = id
        if administration is not UNSET:
            field_dict["administration"] = administration
        if category is not UNSET:
            field_dict["category"] = category
        if id_short is not UNSET:
            field_dict["idShort"] = id_short
        if extensions is not UNSET:
            field_dict["extensions"] = extensions
        if embedded_data_specifications is not UNSET:
            field_dict["embeddedDataSpecifications"] = embedded_data_specifications
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.administrative_information import AdministrativeInformation
        from ..models.asset_information import AssetInformation
        from ..models.embedded_data_specification import EmbeddedDataSpecification
        from ..models.extension import Extension
        from ..models.lang_string_name_type import LangStringNameType
        from ..models.lang_string_text_type import LangStringTextType
        from ..models.reference import Reference

        d = src_dict.copy()
        _asset_information = d.pop("assetInformation", UNSET)
        asset_information: Union[Unset, AssetInformation]
        if isinstance(_asset_information, Unset):
            asset_information = UNSET
        else:
            asset_information = AssetInformation.from_dict(_asset_information)

        _derived_from = d.pop("derivedFrom", UNSET)
        derived_from: Union[Unset, Reference]
        if isinstance(_derived_from, Unset):
            derived_from = UNSET
        else:
            derived_from = Reference.from_dict(_derived_from)

        submodels = []
        _submodels = d.pop("submodels", UNSET)
        for submodels_item_data in _submodels or []:
            submodels_item = Reference.from_dict(submodels_item_data)

            submodels.append(submodels_item)

        id = d.pop("id", UNSET)

        _administration = d.pop("administration", UNSET)
        administration: Union[Unset, AdministrativeInformation]
        if isinstance(_administration, Unset):
            administration = UNSET
        else:
            administration = AdministrativeInformation.from_dict(_administration)

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

        asset_administration_shell = cls(
            asset_information=asset_information,
            derived_from=derived_from,
            submodels=submodels,
            id=id,
            administration=administration,
            category=category,
            id_short=id_short,
            extensions=extensions,
            embedded_data_specifications=embedded_data_specifications,
            display_name=display_name,
            description=description,
        )

        asset_administration_shell.additional_properties = d
        return asset_administration_shell

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
