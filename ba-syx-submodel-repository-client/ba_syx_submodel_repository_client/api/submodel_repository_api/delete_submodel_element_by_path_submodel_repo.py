from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.result import Result
from ...types import Response


def _get_kwargs(
    submodel_identifier: str,
    id_short_path: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}".format(
        client.base_url, submodelIdentifier=submodel_identifier, idShortPath=id_short_path
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, Result]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = Result.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = Result.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = Result.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.OK:
        response_200 = Result.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = Result.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = Result.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, Result]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    submodel_identifier: str,
    id_short_path: str,
    *,
    client: Client,
) -> Response[Union[Any, Result]]:
    """Deletes a submodel element at a specified path within the submodel elements hierarchy

    Args:
        submodel_identifier (str):
        id_short_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Result]]
    """

    kwargs = _get_kwargs(
        submodel_identifier=submodel_identifier,
        id_short_path=id_short_path,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    submodel_identifier: str,
    id_short_path: str,
    *,
    client: Client,
) -> Optional[Union[Any, Result]]:
    """Deletes a submodel element at a specified path within the submodel elements hierarchy

    Args:
        submodel_identifier (str):
        id_short_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Result]
    """

    return sync_detailed(
        submodel_identifier=submodel_identifier,
        id_short_path=id_short_path,
        client=client,
    ).parsed


async def asyncio_detailed(
    submodel_identifier: str,
    id_short_path: str,
    *,
    client: Client,
) -> Response[Union[Any, Result]]:
    """Deletes a submodel element at a specified path within the submodel elements hierarchy

    Args:
        submodel_identifier (str):
        id_short_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Result]]
    """

    kwargs = _get_kwargs(
        submodel_identifier=submodel_identifier,
        id_short_path=id_short_path,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    submodel_identifier: str,
    id_short_path: str,
    *,
    client: Client,
) -> Optional[Union[Any, Result]]:
    """Deletes a submodel element at a specified path within the submodel elements hierarchy

    Args:
        submodel_identifier (str):
        id_short_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Result]
    """

    return (
        await asyncio_detailed(
            submodel_identifier=submodel_identifier,
            id_short_path=id_short_path,
            client=client,
        )
    ).parsed
