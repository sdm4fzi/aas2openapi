from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.get_all_submodel_references_aas_repository_limit import GetAllSubmodelReferencesAasRepositoryLimit
from ...models.result import Result
from ...types import UNSET, Response, Unset


def _get_kwargs(
    aas_identifier: str,
    *,
    client: Client,
    limit: Union[Unset, None, GetAllSubmodelReferencesAasRepositoryLimit] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/shells/{aasIdentifier}/submodel-refs".format(client.base_url, aasIdentifier=aas_identifier)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_limit: Union[Unset, None, str] = UNSET
    if not isinstance(limit, Unset):
        json_limit = limit.value if limit else None

    params["limit"] = json_limit

    params["cursor"] = cursor

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[List[str], Result]]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = Result.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = Result.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = Result.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(List[str], response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = Result.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = Result.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[List[str], Result]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    aas_identifier: str,
    *,
    client: Client,
    limit: Union[Unset, None, GetAllSubmodelReferencesAasRepositoryLimit] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
) -> Response[Union[List[str], Result]]:
    """Returns all submodel references

    Args:
        aas_identifier (str):
        limit (Union[Unset, None, GetAllSubmodelReferencesAasRepositoryLimit]):
        cursor (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List[str], Result]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
        client=client,
        limit=limit,
        cursor=cursor,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    aas_identifier: str,
    *,
    client: Client,
    limit: Union[Unset, None, GetAllSubmodelReferencesAasRepositoryLimit] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
) -> Optional[Union[List[str], Result]]:
    """Returns all submodel references

    Args:
        aas_identifier (str):
        limit (Union[Unset, None, GetAllSubmodelReferencesAasRepositoryLimit]):
        cursor (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List[str], Result]
    """

    return sync_detailed(
        aas_identifier=aas_identifier,
        client=client,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    aas_identifier: str,
    *,
    client: Client,
    limit: Union[Unset, None, GetAllSubmodelReferencesAasRepositoryLimit] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
) -> Response[Union[List[str], Result]]:
    """Returns all submodel references

    Args:
        aas_identifier (str):
        limit (Union[Unset, None, GetAllSubmodelReferencesAasRepositoryLimit]):
        cursor (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List[str], Result]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
        client=client,
        limit=limit,
        cursor=cursor,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    aas_identifier: str,
    *,
    client: Client,
    limit: Union[Unset, None, GetAllSubmodelReferencesAasRepositoryLimit] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
) -> Optional[Union[List[str], Result]]:
    """Returns all submodel references

    Args:
        aas_identifier (str):
        limit (Union[Unset, None, GetAllSubmodelReferencesAasRepositoryLimit]):
        cursor (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List[str], Result]
    """

    return (
        await asyncio_detailed(
            aas_identifier=aas_identifier,
            client=client,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
