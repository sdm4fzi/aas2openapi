from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Base64UrlEncodedCursor")


@attr.s(auto_attribs=True)
class Base64UrlEncodedCursor:
    """
    Attributes:
        encoded_cursor (Union[Unset, str]):
        decoded_cursor (Union[Unset, str]):
    """

    encoded_cursor: Union[Unset, str] = UNSET
    decoded_cursor: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        encoded_cursor = self.encoded_cursor
        decoded_cursor = self.decoded_cursor

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if encoded_cursor is not UNSET:
            field_dict["encodedCursor"] = encoded_cursor
        if decoded_cursor is not UNSET:
            field_dict["decodedCursor"] = decoded_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        encoded_cursor = d.pop("encodedCursor", UNSET)

        decoded_cursor = d.pop("decodedCursor", UNSET)

        base_64_url_encoded_cursor = cls(
            encoded_cursor=encoded_cursor,
            decoded_cursor=decoded_cursor,
        )

        base_64_url_encoded_cursor.additional_properties = d
        return base_64_url_encoded_cursor

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
