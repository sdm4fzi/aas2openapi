from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.service_description_profiles_item import ServiceDescriptionProfilesItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="ServiceDescription")


@attr.s(auto_attribs=True)
class ServiceDescription:
    """The Description object enables servers to present their capabilities to the clients, in particular which profiles
    they implement. At least one defined profile is required. Additional, proprietary attributes might be included.
    Nevertheless, the server must not expect that a regular client understands them.

        Attributes:
            profiles (Union[Unset, List[ServiceDescriptionProfilesItem]]):
    """

    profiles: Union[Unset, List[ServiceDescriptionProfilesItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profiles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.profiles, Unset):
            profiles = []
            for profiles_item_data in self.profiles:
                profiles_item = profiles_item_data.value

                profiles.append(profiles_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if profiles is not UNSET:
            field_dict["profiles"] = profiles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        profiles = []
        _profiles = d.pop("profiles", UNSET)
        for profiles_item_data in _profiles or []:
            profiles_item = ServiceDescriptionProfilesItem(profiles_item_data)

            profiles.append(profiles_item)

        service_description = cls(
            profiles=profiles,
        )

        service_description.additional_properties = d
        return service_description

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
