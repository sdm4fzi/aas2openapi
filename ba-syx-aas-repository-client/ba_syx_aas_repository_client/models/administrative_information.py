from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.embedded_data_specification import EmbeddedDataSpecification
    from ..models.reference import Reference


T = TypeVar("T", bound="AdministrativeInformation")


@attr.s(auto_attribs=True)
class AdministrativeInformation:
    """
    Attributes:
        version (Union[Unset, str]):
        revision (Union[Unset, str]):
        creator (Union[Unset, Reference]):
        template_id (Union[Unset, str]):
        embedded_data_specifications (Union[Unset, List['EmbeddedDataSpecification']]):
    """

    version: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    creator: Union[Unset, "Reference"] = UNSET
    template_id: Union[Unset, str] = UNSET
    embedded_data_specifications: Union[Unset, List["EmbeddedDataSpecification"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        version = self.version
        revision = self.revision
        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        template_id = self.template_id
        embedded_data_specifications: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.embedded_data_specifications, Unset):
            embedded_data_specifications = []
            for embedded_data_specifications_item_data in self.embedded_data_specifications:
                embedded_data_specifications_item = embedded_data_specifications_item_data.to_dict()

                embedded_data_specifications.append(embedded_data_specifications_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if version is not UNSET:
            field_dict["version"] = version
        if revision is not UNSET:
            field_dict["revision"] = revision
        if creator is not UNSET:
            field_dict["creator"] = creator
        if template_id is not UNSET:
            field_dict["templateId"] = template_id
        if embedded_data_specifications is not UNSET:
            field_dict["embeddedDataSpecifications"] = embedded_data_specifications

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.embedded_data_specification import EmbeddedDataSpecification
        from ..models.reference import Reference

        d = src_dict.copy()
        version = d.pop("version", UNSET)

        revision = d.pop("revision", UNSET)

        _creator = d.pop("creator", UNSET)
        creator: Union[Unset, Reference]
        if isinstance(_creator, Unset):
            creator = UNSET
        else:
            creator = Reference.from_dict(_creator)

        template_id = d.pop("templateId", UNSET)

        embedded_data_specifications = []
        _embedded_data_specifications = d.pop("embeddedDataSpecifications", UNSET)
        for embedded_data_specifications_item_data in _embedded_data_specifications or []:
            embedded_data_specifications_item = EmbeddedDataSpecification.from_dict(
                embedded_data_specifications_item_data
            )

            embedded_data_specifications.append(embedded_data_specifications_item)

        administrative_information = cls(
            version=version,
            revision=revision,
            creator=creator,
            template_id=template_id,
            embedded_data_specifications=embedded_data_specifications,
        )

        administrative_information.additional_properties = d
        return administrative_information

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
