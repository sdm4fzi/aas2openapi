from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.qualifier_kind import QualifierKind
from ..models.qualifier_value_type import QualifierValueType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reference import Reference


T = TypeVar("T", bound="Qualifier")


@attr.s(auto_attribs=True)
class Qualifier:
    """
    Attributes:
        type (Union[Unset, str]):
        value_type (Union[Unset, QualifierValueType]):
        kind (Union[Unset, QualifierKind]):
        value_id (Union[Unset, Reference]):
        value (Union[Unset, str]):
        semantic_id (Union[Unset, Reference]):
        supplemental_semantic_ids (Union[Unset, List['Reference']]):
    """

    type: Union[Unset, str] = UNSET
    value_type: Union[Unset, QualifierValueType] = UNSET
    kind: Union[Unset, QualifierKind] = UNSET
    value_id: Union[Unset, "Reference"] = UNSET
    value: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, "Reference"] = UNSET
    supplemental_semantic_ids: Union[Unset, List["Reference"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        value_type: Union[Unset, str] = UNSET
        if not isinstance(self.value_type, Unset):
            value_type = self.value_type.value

        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        value_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.value_id, Unset):
            value_id = self.value_id.to_dict()

        value = self.value
        semantic_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.semantic_id, Unset):
            semantic_id = self.semantic_id.to_dict()

        supplemental_semantic_ids: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.supplemental_semantic_ids, Unset):
            supplemental_semantic_ids = []
            for supplemental_semantic_ids_item_data in self.supplemental_semantic_ids:
                supplemental_semantic_ids_item = supplemental_semantic_ids_item_data.to_dict()

                supplemental_semantic_ids.append(supplemental_semantic_ids_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if value_type is not UNSET:
            field_dict["valueType"] = value_type
        if kind is not UNSET:
            field_dict["kind"] = kind
        if value_id is not UNSET:
            field_dict["valueID"] = value_id
        if value is not UNSET:
            field_dict["value"] = value
        if semantic_id is not UNSET:
            field_dict["semanticID"] = semantic_id
        if supplemental_semantic_ids is not UNSET:
            field_dict["supplementalSemanticIds"] = supplemental_semantic_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.reference import Reference

        d = src_dict.copy()
        type = d.pop("type", UNSET)

        _value_type = d.pop("valueType", UNSET)
        value_type: Union[Unset, QualifierValueType]
        if isinstance(_value_type, Unset):
            value_type = UNSET
        else:
            value_type = QualifierValueType(_value_type)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, QualifierKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = QualifierKind(_kind)

        _value_id = d.pop("valueID", UNSET)
        value_id: Union[Unset, Reference]
        if isinstance(_value_id, Unset):
            value_id = UNSET
        else:
            value_id = Reference.from_dict(_value_id)

        value = d.pop("value", UNSET)

        _semantic_id = d.pop("semanticID", UNSET)
        semantic_id: Union[Unset, Reference]
        if isinstance(_semantic_id, Unset):
            semantic_id = UNSET
        else:
            semantic_id = Reference.from_dict(_semantic_id)

        supplemental_semantic_ids = []
        _supplemental_semantic_ids = d.pop("supplementalSemanticIds", UNSET)
        for supplemental_semantic_ids_item_data in _supplemental_semantic_ids or []:
            supplemental_semantic_ids_item = Reference.from_dict(supplemental_semantic_ids_item_data)

            supplemental_semantic_ids.append(supplemental_semantic_ids_item)

        qualifier = cls(
            type=type,
            value_type=value_type,
            kind=kind,
            value_id=value_id,
            value=value,
            semantic_id=semantic_id,
            supplemental_semantic_ids=supplemental_semantic_ids,
        )

        qualifier.additional_properties = d
        return qualifier

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
