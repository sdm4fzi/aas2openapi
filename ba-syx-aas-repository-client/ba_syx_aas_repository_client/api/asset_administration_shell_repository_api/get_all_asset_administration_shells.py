from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.base_64_url_encoded_cursor import Base64UrlEncodedCursor
from ...models.get_all_asset_administration_shells_limit import GetAllAssetAdministrationShellsLimit
from ...models.paged_result import PagedResult
from ...models.result import Result
from ...models.specific_asset_id import SpecificAssetId
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    asset_ids: Union[Unset, None, List["SpecificAssetId"]] = UNSET,
    id_short: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, GetAllAssetAdministrationShellsLimit] = UNSET,
    cursor: Union[Unset, None, "Base64UrlEncodedCursor"] = UNSET,
) -> Dict[str, Any]:
    url = "{}/shells".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_asset_ids: Union[Unset, None, List[Dict[str, Any]]] = UNSET
    if not isinstance(asset_ids, Unset):
        if asset_ids is None:
            json_asset_ids = None
        else:
            json_asset_ids = []
            for asset_ids_item_data in asset_ids:
                asset_ids_item = asset_ids_item_data.to_dict()

                json_asset_ids.append(asset_ids_item)

    params["assetIds"] = json_asset_ids

    params["idShort"] = id_short

    json_limit: Union[Unset, None, str] = UNSET
    if not isinstance(limit, Unset):
        json_limit = limit.value if limit else None

    params["limit"] = json_limit

    json_cursor: Union[Unset, None, Dict[str, Any]] = UNSET
    if not isinstance(cursor, Unset):
        json_cursor = cursor.to_dict() if cursor else None

    if not isinstance(json_cursor, Unset) and json_cursor is not None:
        params.update(json_cursor)

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[PagedResult, Result]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PagedResult.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = Result.from_dict(response.json())

        return response_500
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = Result.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = Result.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = Result.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[PagedResult, Result]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    asset_ids: Union[Unset, None, List["SpecificAssetId"]] = UNSET,
    id_short: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, GetAllAssetAdministrationShellsLimit] = UNSET,
    cursor: Union[Unset, None, "Base64UrlEncodedCursor"] = UNSET,
) -> Response[Union[PagedResult, Result]]:
    """Returns all Asset Administration Shells

    Args:
        asset_ids (Union[Unset, None, List['SpecificAssetId']]):
        id_short (Union[Unset, None, str]):
        limit (Union[Unset, None, GetAllAssetAdministrationShellsLimit]):
        cursor (Union[Unset, None, Base64UrlEncodedCursor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PagedResult, Result]]
    """

    kwargs = _get_kwargs(
        client=client,
        asset_ids=asset_ids,
        id_short=id_short,
        limit=limit,
        cursor=cursor,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    asset_ids: Union[Unset, None, List["SpecificAssetId"]] = UNSET,
    id_short: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, GetAllAssetAdministrationShellsLimit] = UNSET,
    cursor: Union[Unset, None, "Base64UrlEncodedCursor"] = UNSET,
) -> Optional[Union[PagedResult, Result]]:
    """Returns all Asset Administration Shells

    Args:
        asset_ids (Union[Unset, None, List['SpecificAssetId']]):
        id_short (Union[Unset, None, str]):
        limit (Union[Unset, None, GetAllAssetAdministrationShellsLimit]):
        cursor (Union[Unset, None, Base64UrlEncodedCursor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PagedResult, Result]
    """

    return sync_detailed(
        client=client,
        asset_ids=asset_ids,
        id_short=id_short,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    asset_ids: Union[Unset, None, List["SpecificAssetId"]] = UNSET,
    id_short: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, GetAllAssetAdministrationShellsLimit] = UNSET,
    cursor: Union[Unset, None, "Base64UrlEncodedCursor"] = UNSET,
) -> Response[Union[PagedResult, Result]]:
    """Returns all Asset Administration Shells

    Args:
        asset_ids (Union[Unset, None, List['SpecificAssetId']]):
        id_short (Union[Unset, None, str]):
        limit (Union[Unset, None, GetAllAssetAdministrationShellsLimit]):
        cursor (Union[Unset, None, Base64UrlEncodedCursor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PagedResult, Result]]
    """

    kwargs = _get_kwargs(
        client=client,
        asset_ids=asset_ids,
        id_short=id_short,
        limit=limit,
        cursor=cursor,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    asset_ids: Union[Unset, None, List["SpecificAssetId"]] = UNSET,
    id_short: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, GetAllAssetAdministrationShellsLimit] = UNSET,
    cursor: Union[Unset, None, "Base64UrlEncodedCursor"] = UNSET,
) -> Optional[Union[PagedResult, Result]]:
    """Returns all Asset Administration Shells

    Args:
        asset_ids (Union[Unset, None, List['SpecificAssetId']]):
        id_short (Union[Unset, None, str]):
        limit (Union[Unset, None, GetAllAssetAdministrationShellsLimit]):
        cursor (Union[Unset, None, Base64UrlEncodedCursor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PagedResult, Result]
    """

    return (
        await asyncio_detailed(
            client=client,
            asset_ids=asset_ids,
            id_short=id_short,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
