from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_specification_content import DataSpecificationContent
    from ..models.reference import Reference


T = TypeVar("T", bound="EmbeddedDataSpecification")


@attr.s(auto_attribs=True)
class EmbeddedDataSpecification:
    """
    Attributes:
        data_specification (Union[Unset, Reference]):
        data_specification_content (Union[Unset, DataSpecificationContent]):
    """

    data_specification: Union[Unset, "Reference"] = UNSET
    data_specification_content: Union[Unset, "DataSpecificationContent"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_specification: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data_specification, Unset):
            data_specification = self.data_specification.to_dict()

        data_specification_content: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data_specification_content, Unset):
            data_specification_content = self.data_specification_content.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data_specification is not UNSET:
            field_dict["dataSpecification"] = data_specification
        if data_specification_content is not UNSET:
            field_dict["dataSpecificationContent"] = data_specification_content

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_specification_content import DataSpecificationContent
        from ..models.reference import Reference

        d = src_dict.copy()
        _data_specification = d.pop("dataSpecification", UNSET)
        data_specification: Union[Unset, Reference]
        if isinstance(_data_specification, Unset):
            data_specification = UNSET
        else:
            data_specification = Reference.from_dict(_data_specification)

        _data_specification_content = d.pop("dataSpecificationContent", UNSET)
        data_specification_content: Union[Unset, DataSpecificationContent]
        if isinstance(_data_specification_content, Unset):
            data_specification_content = UNSET
        else:
            data_specification_content = DataSpecificationContent.from_dict(_data_specification_content)

        embedded_data_specification = cls(
            data_specification=data_specification,
            data_specification_content=data_specification_content,
        )

        embedded_data_specification.additional_properties = d
        return embedded_data_specification

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
