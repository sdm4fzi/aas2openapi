from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.operation_variable import OperationVariable


T = TypeVar("T", bound="OperationRequest")


@attr.s(auto_attribs=True)
class OperationRequest:
    """Operation request object

    Attributes:
        inoutput_arguments (Union[Unset, List['OperationVariable']]):
        input_arguments (Union[Unset, List['OperationVariable']]):
        client_timeout_duration (Union[Unset, str]):
    """

    inoutput_arguments: Union[Unset, List["OperationVariable"]] = UNSET
    input_arguments: Union[Unset, List["OperationVariable"]] = UNSET
    client_timeout_duration: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        inoutput_arguments: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.inoutput_arguments, Unset):
            inoutput_arguments = []
            for inoutput_arguments_item_data in self.inoutput_arguments:
                inoutput_arguments_item = inoutput_arguments_item_data.to_dict()

                inoutput_arguments.append(inoutput_arguments_item)

        input_arguments: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.input_arguments, Unset):
            input_arguments = []
            for input_arguments_item_data in self.input_arguments:
                input_arguments_item = input_arguments_item_data.to_dict()

                input_arguments.append(input_arguments_item)

        client_timeout_duration = self.client_timeout_duration

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if inoutput_arguments is not UNSET:
            field_dict["inoutputArguments"] = inoutput_arguments
        if input_arguments is not UNSET:
            field_dict["inputArguments"] = input_arguments
        if client_timeout_duration is not UNSET:
            field_dict["clientTimeoutDuration"] = client_timeout_duration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.operation_variable import OperationVariable

        d = src_dict.copy()
        inoutput_arguments = []
        _inoutput_arguments = d.pop("inoutputArguments", UNSET)
        for inoutput_arguments_item_data in _inoutput_arguments or []:
            inoutput_arguments_item = OperationVariable.from_dict(inoutput_arguments_item_data)

            inoutput_arguments.append(inoutput_arguments_item)

        input_arguments = []
        _input_arguments = d.pop("inputArguments", UNSET)
        for input_arguments_item_data in _input_arguments or []:
            input_arguments_item = OperationVariable.from_dict(input_arguments_item_data)

            input_arguments.append(input_arguments_item)

        client_timeout_duration = d.pop("clientTimeoutDuration", UNSET)

        operation_request = cls(
            inoutput_arguments=inoutput_arguments,
            input_arguments=input_arguments,
            client_timeout_duration=client_timeout_duration,
        )

        operation_request.additional_properties = d
        return operation_request

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
