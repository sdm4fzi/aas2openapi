from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.paged_result_paging_metadata import PagedResultPagingMetadata


T = TypeVar("T", bound="PagedResult")


@attr.s(auto_attribs=True)
class PagedResult:
    """
    Attributes:
        paging_metadata (Union[Unset, PagedResultPagingMetadata]):
    """

    paging_metadata: Union[Unset, "PagedResultPagingMetadata"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        paging_metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.paging_metadata, Unset):
            paging_metadata = self.paging_metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if paging_metadata is not UNSET:
            field_dict["paging_metadata"] = paging_metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.paged_result_paging_metadata import PagedResultPagingMetadata

        d = src_dict.copy()
        _paging_metadata = d.pop("paging_metadata", UNSET)
        paging_metadata: Union[Unset, PagedResultPagingMetadata]
        if isinstance(_paging_metadata, Unset):
            paging_metadata = UNSET
        else:
            paging_metadata = PagedResultPagingMetadata.from_dict(_paging_metadata)

        paged_result = cls(
            paging_metadata=paging_metadata,
        )

        paged_result.additional_properties = d
        return paged_result

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
