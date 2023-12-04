from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PagedResultPagingMetadata")


@attr.s(auto_attribs=True)
class PagedResultPagingMetadata:
    """
    Attributes:
        cursor (Union[Unset, str]):  Example: wJlCDLIl6KTWypN7T6vc6nWEmEYe99Hjf1XY1xmqV-M=#.
    """

    cursor: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cursor = self.cursor

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cursor is not UNSET:
            field_dict["cursor"] = cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cursor = d.pop("cursor", UNSET)

        paged_result_paging_metadata = cls(
            cursor=cursor,
        )

        paged_result_paging_metadata.additional_properties = d
        return paged_result_paging_metadata

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
