from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.get_all_submodel_elements_extent import GetAllSubmodelElementsExtent
from ...models.get_all_submodel_elements_level import GetAllSubmodelElementsLevel
from ...models.get_all_submodel_elements_limit import GetAllSubmodelElementsLimit
from ...models.result import Result
from ...types import UNSET, Response, Unset


def _get_kwargs(
    submodel_identifier: str,
    *,
    client: Client,
    limit: Union[Unset, None, GetAllSubmodelElementsLimit] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, GetAllSubmodelElementsLevel] = GetAllSubmodelElementsLevel.DEEP,
    extent: Union[Unset, None, GetAllSubmodelElementsExtent] = GetAllSubmodelElementsExtent.WITHOUTBLOBVALUE,
) -> Dict[str, Any]:
    url = "{}/submodels/{submodelIdentifier}/submodel-elements".format(
        client.base_url, submodelIdentifier=submodel_identifier
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_limit: Union[Unset, None, str] = UNSET
    if not isinstance(limit, Unset):
        json_limit = limit.value if limit else None

    params["limit"] = json_limit

    params["cursor"] = cursor

    json_level: Union[Unset, None, str] = UNSET
    if not isinstance(level, Unset):
        json_level = level.value if level else None

    params["level"] = json_level

    json_extent: Union[Unset, None, str] = UNSET
    if not isinstance(extent, Unset):
        json_extent = extent.value if extent else None

    params["extent"] = json_extent

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Result, str]]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = Result.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = Result.from_dict(response.json())

        return response_500
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(str, response.json())
        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = Result.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = Result.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = Result.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Result, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    submodel_identifier: str,
    *,
    client: Client,
    limit: Union[Unset, None, GetAllSubmodelElementsLimit] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, GetAllSubmodelElementsLevel] = GetAllSubmodelElementsLevel.DEEP,
    extent: Union[Unset, None, GetAllSubmodelElementsExtent] = GetAllSubmodelElementsExtent.WITHOUTBLOBVALUE,
) -> Response[Union[Result, str]]:
    """Returns all submodel elements including their hierarchy

    Args:
        submodel_identifier (str):
        limit (Union[Unset, None, GetAllSubmodelElementsLimit]):
        cursor (Union[Unset, None, str]):
        level (Union[Unset, None, GetAllSubmodelElementsLevel]):  Default:
            GetAllSubmodelElementsLevel.DEEP.
        extent (Union[Unset, None, GetAllSubmodelElementsExtent]):  Default:
            GetAllSubmodelElementsExtent.WITHOUTBLOBVALUE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Result, str]]
    """

    kwargs = _get_kwargs(
        submodel_identifier=submodel_identifier,
        client=client,
        limit=limit,
        cursor=cursor,
        level=level,
        extent=extent,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    submodel_identifier: str,
    *,
    client: Client,
    limit: Union[Unset, None, GetAllSubmodelElementsLimit] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, GetAllSubmodelElementsLevel] = GetAllSubmodelElementsLevel.DEEP,
    extent: Union[Unset, None, GetAllSubmodelElementsExtent] = GetAllSubmodelElementsExtent.WITHOUTBLOBVALUE,
) -> Optional[Union[Result, str]]:
    """Returns all submodel elements including their hierarchy

    Args:
        submodel_identifier (str):
        limit (Union[Unset, None, GetAllSubmodelElementsLimit]):
        cursor (Union[Unset, None, str]):
        level (Union[Unset, None, GetAllSubmodelElementsLevel]):  Default:
            GetAllSubmodelElementsLevel.DEEP.
        extent (Union[Unset, None, GetAllSubmodelElementsExtent]):  Default:
            GetAllSubmodelElementsExtent.WITHOUTBLOBVALUE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Result, str]
    """

    return sync_detailed(
        submodel_identifier=submodel_identifier,
        client=client,
        limit=limit,
        cursor=cursor,
        level=level,
        extent=extent,
    ).parsed


async def asyncio_detailed(
    submodel_identifier: str,
    *,
    client: Client,
    limit: Union[Unset, None, GetAllSubmodelElementsLimit] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, GetAllSubmodelElementsLevel] = GetAllSubmodelElementsLevel.DEEP,
    extent: Union[Unset, None, GetAllSubmodelElementsExtent] = GetAllSubmodelElementsExtent.WITHOUTBLOBVALUE,
) -> Response[Union[Result, str]]:
    """Returns all submodel elements including their hierarchy

    Args:
        submodel_identifier (str):
        limit (Union[Unset, None, GetAllSubmodelElementsLimit]):
        cursor (Union[Unset, None, str]):
        level (Union[Unset, None, GetAllSubmodelElementsLevel]):  Default:
            GetAllSubmodelElementsLevel.DEEP.
        extent (Union[Unset, None, GetAllSubmodelElementsExtent]):  Default:
            GetAllSubmodelElementsExtent.WITHOUTBLOBVALUE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Result, str]]
    """

    kwargs = _get_kwargs(
        submodel_identifier=submodel_identifier,
        client=client,
        limit=limit,
        cursor=cursor,
        level=level,
        extent=extent,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    submodel_identifier: str,
    *,
    client: Client,
    limit: Union[Unset, None, GetAllSubmodelElementsLimit] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    level: Union[Unset, None, GetAllSubmodelElementsLevel] = GetAllSubmodelElementsLevel.DEEP,
    extent: Union[Unset, None, GetAllSubmodelElementsExtent] = GetAllSubmodelElementsExtent.WITHOUTBLOBVALUE,
) -> Optional[Union[Result, str]]:
    """Returns all submodel elements including their hierarchy

    Args:
        submodel_identifier (str):
        limit (Union[Unset, None, GetAllSubmodelElementsLimit]):
        cursor (Union[Unset, None, str]):
        level (Union[Unset, None, GetAllSubmodelElementsLevel]):  Default:
            GetAllSubmodelElementsLevel.DEEP.
        extent (Union[Unset, None, GetAllSubmodelElementsExtent]):  Default:
            GetAllSubmodelElementsExtent.WITHOUTBLOBVALUE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Result, str]
    """

    return (
        await asyncio_detailed(
            submodel_identifier=submodel_identifier,
            client=client,
            limit=limit,
            cursor=cursor,
            level=level,
            extent=extent,
        )
    ).parsed
