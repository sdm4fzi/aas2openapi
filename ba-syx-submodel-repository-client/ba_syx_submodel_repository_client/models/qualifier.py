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
        value (Union[Unset, str]):
        kind (Union[Unset, QualifierKind]):
        value_type (Union[Unset, QualifierValueType]):
        supplemental_semantic_ids (Union[Unset, List['Reference']]):
        value_id (Union[Unset, Reference]):
        semantic_id (Union[Unset, Reference]):
    """

    type: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    kind: Union[Unset, QualifierKind] = UNSET
    value_type: Union[Unset, QualifierValueType] = UNSET
    supplemental_semantic_ids: Union[Unset, List["Reference"]] = UNSET
    value_id: Union[Unset, "Reference"] = UNSET
    semantic_id: Union[Unset, "Reference"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        value = self.value
        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        value_type: Union[Unset, str] = UNSET
        if not isinstance(self.value_type, Unset):
            value_type = self.value_type.value

        supplemental_semantic_ids: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.supplemental_semantic_ids, Unset):
            supplemental_semantic_ids = []
            for supplemental_semantic_ids_item_data in self.supplemental_semantic_ids:
                supplemental_semantic_ids_item = supplemental_semantic_ids_item_data.to_dict()

                supplemental_semantic_ids.append(supplemental_semantic_ids_item)

        value_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.value_id, Unset):
            value_id = self.value_id.to_dict()

        semantic_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.semantic_id, Unset):
            semantic_id = self.semantic_id.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if value is not UNSET:
            field_dict["value"] = value
        if kind is not UNSET:
            field_dict["kind"] = kind
        if value_type is not UNSET:
            field_dict["valueType"] = value_type
        if supplemental_semantic_ids is not UNSET:
            field_dict["supplementalSemanticIds"] = supplemental_semantic_ids
        if value_id is not UNSET:
            field_dict["valueId"] = value_id
        if semantic_id is not UNSET:
            field_dict["semanticId"] = semantic_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.reference import Reference

        d = src_dict.copy()
        type = d.pop("type", UNSET)

        value = d.pop("value", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, QualifierKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = QualifierKind(_kind)

        _value_type = d.pop("valueType", UNSET)
        value_type: Union[Unset, QualifierValueType]
        if isinstance(_value_type, Unset):
            value_type = UNSET
        else:
            value_type = QualifierValueType(_value_type)

        supplemental_semantic_ids = []
        _supplemental_semantic_ids = d.pop("supplementalSemanticIds", UNSET)
        for supplemental_semantic_ids_item_data in _supplemental_semantic_ids or []:
            supplemental_semantic_ids_item = Reference.from_dict(supplemental_semantic_ids_item_data)

            supplemental_semantic_ids.append(supplemental_semantic_ids_item)

        _value_id = d.pop("valueId", UNSET)
        value_id: Union[Unset, Reference]
        if isinstance(_value_id, Unset):
            value_id = UNSET
        else:
            value_id = Reference.from_dict(_value_id)

        _semantic_id = d.pop("semanticId", UNSET)
        semantic_id: Union[Unset, Reference]
        if isinstance(_semantic_id, Unset):
            semantic_id = UNSET
        else:
            semantic_id = Reference.from_dict(_semantic_id)

        qualifier = cls(
            type=type,
            value=value,
            kind=kind,
            value_type=value_type,
            supplemental_semantic_ids=supplemental_semantic_ids,
            value_id=value_id,
            semantic_id=semantic_id,
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
