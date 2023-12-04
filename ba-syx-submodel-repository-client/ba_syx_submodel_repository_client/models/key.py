from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.key_type import KeyType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Key")


@attr.s(auto_attribs=True)
class Key:
    """
    Attributes:
        value (Union[Unset, str]):
        type (Union[Unset, KeyType]):
    """

    value: Union[Unset, str] = UNSET
    type: Union[Unset, KeyType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, KeyType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = KeyType(_type)

        key = cls(
            value=value,
            type=type,
        )

        key.additional_properties = d
        return key

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
