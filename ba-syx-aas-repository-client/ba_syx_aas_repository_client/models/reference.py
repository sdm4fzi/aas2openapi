from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.reference_type import ReferenceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.key import Key


T = TypeVar("T", bound="Reference")


@attr.s(auto_attribs=True)
class Reference:
    """
    Attributes:
        keys (Union[Unset, List['Key']]):
        type (Union[Unset, ReferenceType]):
        referred_semantic_id (Union[Unset, Reference]):
    """

    keys: Union[Unset, List["Key"]] = UNSET
    type: Union[Unset, ReferenceType] = UNSET
    referred_semantic_id: Union[Unset, "Reference"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        keys: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.keys, Unset):
            keys = []
            for keys_item_data in self.keys:
                keys_item = keys_item_data.to_dict()

                keys.append(keys_item)

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        referred_semantic_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.referred_semantic_id, Unset):
            referred_semantic_id = self.referred_semantic_id.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if keys is not UNSET:
            field_dict["keys"] = keys
        if type is not UNSET:
            field_dict["type"] = type
        if referred_semantic_id is not UNSET:
            field_dict["referredSemanticID"] = referred_semantic_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.key import Key

        d = src_dict.copy()
        keys = []
        _keys = d.pop("keys", UNSET)
        for keys_item_data in _keys or []:
            keys_item = Key.from_dict(keys_item_data)

            keys.append(keys_item)

        _type = d.pop("type", UNSET)
        type: Union[Unset, ReferenceType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ReferenceType(_type)

        _referred_semantic_id = d.pop("referredSemanticID", UNSET)
        referred_semantic_id: Union[Unset, Reference]
        if isinstance(_referred_semantic_id, Unset):
            referred_semantic_id = UNSET
        else:
            referred_semantic_id = Reference.from_dict(_referred_semantic_id)

        reference = cls(
            keys=keys,
            type=type,
            referred_semantic_id=referred_semantic_id,
        )

        reference.additional_properties = d
        return reference

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
