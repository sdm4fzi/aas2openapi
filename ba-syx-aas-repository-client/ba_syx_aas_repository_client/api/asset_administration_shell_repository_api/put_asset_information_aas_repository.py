from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.asset_information import AssetInformation
from ...models.result import Result
from ...types import Response


def _get_kwargs(
    aas_identifier: str,
    *,
    client: Client,
    json_body: AssetInformation,
) -> Dict[str, Any]:
    url = "{}/shells/{aasIdentifier}/asset-information".format(client.base_url, aasIdentifier=aas_identifier)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, Result]]:
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = Result.from_dict(response.json())

        return response_500
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = Result.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = Result.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = Result.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.OK:
        response_200 = Result.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = Result.from_dict(response.json())

        return response_400
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
    aas_identifier: str,
    *,
    client: Client,
    json_body: AssetInformation,
) -> Response[Union[Any, Result]]:
    """Updates the Asset Information

    Args:
        aas_identifier (str):
        json_body (AssetInformation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Result]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
        client=client,
        json_body=json_body,
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
    json_body: AssetInformation,
) -> Optional[Union[Any, Result]]:
    """Updates the Asset Information

    Args:
        aas_identifier (str):
        json_body (AssetInformation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Result]
    """

    return sync_detailed(
        aas_identifier=aas_identifier,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    aas_identifier: str,
    *,
    client: Client,
    json_body: AssetInformation,
) -> Response[Union[Any, Result]]:
    """Updates the Asset Information

    Args:
        aas_identifier (str):
        json_body (AssetInformation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Result]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    aas_identifier: str,
    *,
    client: Client,
    json_body: AssetInformation,
) -> Optional[Union[Any, Result]]:
    """Updates the Asset Information

    Args:
        aas_identifier (str):
        json_body (AssetInformation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Result]
    """

    return (
        await asyncio_detailed(
            aas_identifier=aas_identifier,
            client=client,
            json_body=json_body,
        )
    ).parsed
