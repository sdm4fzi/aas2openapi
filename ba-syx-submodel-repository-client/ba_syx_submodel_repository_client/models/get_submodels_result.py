from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.paged_result_paging_metadata import PagedResultPagingMetadata
    from ..models.submodel import Submodel


T = TypeVar("T", bound="GetSubmodelsResult")


@attr.s(auto_attribs=True)
class GetSubmodelsResult:
    """
    Attributes:
        paging_metadata (Union[Unset, PagedResultPagingMetadata]):
        result (Union[Unset, List['Submodel']]):
    """

    paging_metadata: Union[Unset, "PagedResultPagingMetadata"] = UNSET
    result: Union[Unset, List["Submodel"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        paging_metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.paging_metadata, Unset):
            paging_metadata = self.paging_metadata.to_dict()

        result: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.result, Unset):
            result = []
            for result_item_data in self.result:
                result_item = result_item_data.to_dict()

                result.append(result_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if paging_metadata is not UNSET:
            field_dict["paging_metadata"] = paging_metadata
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.paged_result_paging_metadata import PagedResultPagingMetadata
        from ..models.submodel import Submodel

        d = src_dict.copy()
        _paging_metadata = d.pop("paging_metadata", UNSET)
        paging_metadata: Union[Unset, PagedResultPagingMetadata]
        if isinstance(_paging_metadata, Unset):
            paging_metadata = UNSET
        else:
            paging_metadata = PagedResultPagingMetadata.from_dict(_paging_metadata)

        result = []
        _result = d.pop("result", UNSET)
        for result_item_data in _result or []:
            result_item = Submodel.from_dict(result_item_data)

            result.append(result_item)

        get_submodels_result = cls(
            paging_metadata=paging_metadata,
            result=result,
        )

        get_submodels_result.additional_properties = d
        return get_submodels_result

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
