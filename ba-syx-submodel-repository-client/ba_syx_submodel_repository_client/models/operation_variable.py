from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.submodel_element import SubmodelElement


T = TypeVar("T", bound="OperationVariable")


@attr.s(auto_attribs=True)
class OperationVariable:
    """
    Attributes:
        value (Union[Unset, SubmodelElement]):
    """

    value: Union[Unset, "SubmodelElement"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.submodel_element import SubmodelElement

        d = src_dict.copy()
        _value = d.pop("value", UNSET)
        value: Union[Unset, SubmodelElement]
        if isinstance(_value, Unset):
            value = UNSET
        else:
            value = SubmodelElement.from_dict(_value)

        operation_variable = cls(
            value=value,
        )

        operation_variable.additional_properties = d
        return operation_variable

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
