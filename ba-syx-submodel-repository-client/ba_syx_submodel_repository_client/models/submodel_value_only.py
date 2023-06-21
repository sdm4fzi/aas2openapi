from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.submodel_value_only_values_only_map import SubmodelValueOnlyValuesOnlyMap


T = TypeVar("T", bound="SubmodelValueOnly")


@attr.s(auto_attribs=True)
class SubmodelValueOnly:
    """
    Attributes:
        id_short (Union[Unset, str]):
        values_only_map (Union[Unset, SubmodelValueOnlyValuesOnlyMap]):
    """

    id_short: Union[Unset, str] = UNSET
    values_only_map: Union[Unset, "SubmodelValueOnlyValuesOnlyMap"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        values_only_map: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.values_only_map, Unset):
            values_only_map = self.values_only_map.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id_short is not UNSET:
            field_dict["idShort"] = id_short
        if values_only_map is not UNSET:
            field_dict["valuesOnlyMap"] = values_only_map

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.submodel_value_only_values_only_map import SubmodelValueOnlyValuesOnlyMap

        d = src_dict.copy()
        id_short = d.pop("idShort", UNSET)

        _values_only_map = d.pop("valuesOnlyMap", UNSET)
        values_only_map: Union[Unset, SubmodelValueOnlyValuesOnlyMap]
        if isinstance(_values_only_map, Unset):
            values_only_map = UNSET
        else:
            values_only_map = SubmodelValueOnlyValuesOnlyMap.from_dict(_values_only_map)

        submodel_value_only = cls(
            id_short=id_short,
            values_only_map=values_only_map,
        )

        submodel_value_only.additional_properties = d
        return submodel_value_only

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
