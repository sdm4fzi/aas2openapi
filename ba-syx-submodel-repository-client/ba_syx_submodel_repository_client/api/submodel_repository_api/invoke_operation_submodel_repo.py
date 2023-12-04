from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.operation_request import OperationRequest
from ...models.result import Result
from ...types import UNSET, Response, Unset


def _get_kwargs(
    submodel_identifier: str,
    id_short_path: str,
    *,
    client: Client,
    json_body: OperationRequest,
    async_: Union[Unset, None, str] = "false",
) -> Dict[str, Any]:
    url = "{}/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/invoke".format(
        client.base_url, submodelIdentifier=submodel_identifier, idShortPath=id_short_path
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["async"] = async_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Result]:
    if response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
        response_405 = Result.from_dict(response.json())

        return response_405
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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Result]:
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
    json_body: OperationRequest,
    async_: Union[Unset, None, str] = "false",
) -> Response[Result]:
    """Synchronously or asynchronously invokes an Operation at a specified path

    Args:
        submodel_identifier (str):
        id_short_path (str):
        async_ (Union[Unset, None, str]):  Default: 'false'.
        json_body (OperationRequest): Operation request object

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Result]
    """

    kwargs = _get_kwargs(
        submodel_identifier=submodel_identifier,
        id_short_path=id_short_path,
        client=client,
        json_body=json_body,
        async_=async_,
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
    json_body: OperationRequest,
    async_: Union[Unset, None, str] = "false",
) -> Optional[Result]:
    """Synchronously or asynchronously invokes an Operation at a specified path

    Args:
        submodel_identifier (str):
        id_short_path (str):
        async_ (Union[Unset, None, str]):  Default: 'false'.
        json_body (OperationRequest): Operation request object

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Result
    """

    return sync_detailed(
        submodel_identifier=submodel_identifier,
        id_short_path=id_short_path,
        client=client,
        json_body=json_body,
        async_=async_,
    ).parsed


async def asyncio_detailed(
    submodel_identifier: str,
    id_short_path: str,
    *,
    client: Client,
    json_body: OperationRequest,
    async_: Union[Unset, None, str] = "false",
) -> Response[Result]:
    """Synchronously or asynchronously invokes an Operation at a specified path

    Args:
        submodel_identifier (str):
        id_short_path (str):
        async_ (Union[Unset, None, str]):  Default: 'false'.
        json_body (OperationRequest): Operation request object

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Result]
    """

    kwargs = _get_kwargs(
        submodel_identifier=submodel_identifier,
        id_short_path=id_short_path,
        client=client,
        json_body=json_body,
        async_=async_,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    submodel_identifier: str,
    id_short_path: str,
    *,
    client: Client,
    json_body: OperationRequest,
    async_: Union[Unset, None, str] = "false",
) -> Optional[Result]:
    """Synchronously or asynchronously invokes an Operation at a specified path

    Args:
        submodel_identifier (str):
        id_short_path (str):
        async_ (Union[Unset, None, str]):  Default: 'false'.
        json_body (OperationRequest): Operation request object

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Result
    """

    return (
        await asyncio_detailed(
            submodel_identifier=submodel_identifier,
            id_short_path=id_short_path,
            client=client,
            json_body=json_body,
            async_=async_,
        )
    ).parsed
