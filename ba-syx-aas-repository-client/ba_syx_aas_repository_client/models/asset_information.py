from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.asset_information_asset_kind import AssetInformationAssetKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource import Resource
    from ..models.specific_asset_id import SpecificAssetId


T = TypeVar("T", bound="AssetInformation")


@attr.s(auto_attribs=True)
class AssetInformation:
    """
    Attributes:
        asset_kind (Union[Unset, AssetInformationAssetKind]):
        specific_asset_ids (Union[Unset, List['SpecificAssetId']]):
        asset_type (Union[Unset, str]):
        default_thumbnail (Union[Unset, Resource]):
        global_asset_id (Union[Unset, str]):
    """

    asset_kind: Union[Unset, AssetInformationAssetKind] = UNSET
    specific_asset_ids: Union[Unset, List["SpecificAssetId"]] = UNSET
    asset_type: Union[Unset, str] = UNSET
    default_thumbnail: Union[Unset, "Resource"] = UNSET
    global_asset_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        asset_kind: Union[Unset, str] = UNSET
        if not isinstance(self.asset_kind, Unset):
            asset_kind = self.asset_kind.value

        specific_asset_ids: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.specific_asset_ids, Unset):
            specific_asset_ids = []
            for specific_asset_ids_item_data in self.specific_asset_ids:
                specific_asset_ids_item = specific_asset_ids_item_data.to_dict()

                specific_asset_ids.append(specific_asset_ids_item)

        asset_type = self.asset_type
        default_thumbnail: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_thumbnail, Unset):
            default_thumbnail = self.default_thumbnail.to_dict()

        global_asset_id = self.global_asset_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if asset_kind is not UNSET:
            field_dict["assetKind"] = asset_kind
        if specific_asset_ids is not UNSET:
            field_dict["specificAssetIds"] = specific_asset_ids
        if asset_type is not UNSET:
            field_dict["assetType"] = asset_type
        if default_thumbnail is not UNSET:
            field_dict["defaultThumbnail"] = default_thumbnail
        if global_asset_id is not UNSET:
            field_dict["globalAssetId"] = global_asset_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.resource import Resource
        from ..models.specific_asset_id import SpecificAssetId

        d = src_dict.copy()
        _asset_kind = d.pop("assetKind", UNSET)
        asset_kind: Union[Unset, AssetInformationAssetKind]
        if isinstance(_asset_kind, Unset):
            asset_kind = UNSET
        else:
            asset_kind = AssetInformationAssetKind(_asset_kind)

        specific_asset_ids = []
        _specific_asset_ids = d.pop("specificAssetIds", UNSET)
        for specific_asset_ids_item_data in _specific_asset_ids or []:
            specific_asset_ids_item = SpecificAssetId.from_dict(specific_asset_ids_item_data)

            specific_asset_ids.append(specific_asset_ids_item)

        asset_type = d.pop("assetType", UNSET)

        _default_thumbnail = d.pop("defaultThumbnail", UNSET)
        default_thumbnail: Union[Unset, Resource]
        if isinstance(_default_thumbnail, Unset):
            default_thumbnail = UNSET
        else:
            default_thumbnail = Resource.from_dict(_default_thumbnail)

        global_asset_id = d.pop("globalAssetId", UNSET)

        asset_information = cls(
            asset_kind=asset_kind,
            specific_asset_ids=specific_asset_ids,
            asset_type=asset_type,
            default_thumbnail=default_thumbnail,
            global_asset_id=global_asset_id,
        )

        asset_information.additional_properties = d
        return asset_information

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
