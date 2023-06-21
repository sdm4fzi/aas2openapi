from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.message_message_type import MessageMessageType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Message")


@attr.s(auto_attribs=True)
class Message:
    """
    Attributes:
        code (Union[Unset, str]):
        correlation_id (Union[Unset, str]):
        message_type (Union[Unset, MessageMessageType]):
        text (Union[Unset, str]):
        timestamp (Union[Unset, str]):
    """

    code: Union[Unset, str] = UNSET
    correlation_id: Union[Unset, str] = UNSET
    message_type: Union[Unset, MessageMessageType] = UNSET
    text: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        correlation_id = self.correlation_id
        message_type: Union[Unset, str] = UNSET
        if not isinstance(self.message_type, Unset):
            message_type = self.message_type.value

        text = self.text
        timestamp = self.timestamp

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if correlation_id is not UNSET:
            field_dict["correlationId"] = correlation_id
        if message_type is not UNSET:
            field_dict["messageType"] = message_type
        if text is not UNSET:
            field_dict["text"] = text
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code", UNSET)

        correlation_id = d.pop("correlationId", UNSET)

        _message_type = d.pop("messageType", UNSET)
        message_type: Union[Unset, MessageMessageType]
        if isinstance(_message_type, Unset):
            message_type = UNSET
        else:
            message_type = MessageMessageType(_message_type)

        text = d.pop("text", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        message = cls(
            code=code,
            correlation_id=correlation_id,
            message_type=message_type,
            text=text,
            timestamp=timestamp,
        )

        message.additional_properties = d
        return message

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
