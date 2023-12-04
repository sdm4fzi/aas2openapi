from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.entity import Entity
from ...models.operation import Operation
from ...models.relationship_element import RelationshipElement
from ...models.result import Result
from ...models.submodel_element import SubmodelElement
from ...models.submodel_element_collection import SubmodelElementCollection
from ...models.submodel_element_list import SubmodelElementList
from ...types import Response


def _get_kwargs(
    submodel_identifier: str,
    *,
    client: Client,
    json_body: Union[
        "Entity",
        "Operation",
        "RelationshipElement",
        "SubmodelElement",
        "SubmodelElementCollection",
        "SubmodelElementList",
    ],
) -> Dict[str, Any]:
    url = "{}/submodels/{submodelIdentifier}/submodel-elements".format(
        client.base_url, submodelIdentifier=submodel_identifier
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body: Dict[str, Any]

    if isinstance(json_body, SubmodelElement):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, SubmodelElement):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, Entity):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, SubmodelElement):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, Operation):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RelationshipElement):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, SubmodelElementCollection):
        json_json_body = json_body.to_dict()

    else:
        json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Result, SubmodelElement]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = SubmodelElement.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = Result.from_dict(response.json())

        return response_409
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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Result, SubmodelElement]]:
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
    json_body: Union[
        "Entity",
        "Operation",
        "RelationshipElement",
        "SubmodelElement",
        "SubmodelElementCollection",
        "SubmodelElementList",
    ],
) -> Response[Union[Result, SubmodelElement]]:
    """Creates a new submodel element

    Args:
        submodel_identifier (str):
        json_body (Union['Entity', 'Operation', 'RelationshipElement', 'SubmodelElement',
            'SubmodelElementCollection', 'SubmodelElementList']): Requested submodel element

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Result, SubmodelElement]]
    """

    kwargs = _get_kwargs(
        submodel_identifier=submodel_identifier,
        client=client,
        json_body=json_body,
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
    json_body: Union[
        "Entity",
        "Operation",
        "RelationshipElement",
        "SubmodelElement",
        "SubmodelElementCollection",
        "SubmodelElementList",
    ],
) -> Optional[Union[Result, SubmodelElement]]:
    """Creates a new submodel element

    Args:
        submodel_identifier (str):
        json_body (Union['Entity', 'Operation', 'RelationshipElement', 'SubmodelElement',
            'SubmodelElementCollection', 'SubmodelElementList']): Requested submodel element

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Result, SubmodelElement]
    """

    return sync_detailed(
        submodel_identifier=submodel_identifier,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    submodel_identifier: str,
    *,
    client: Client,
    json_body: Union[
        "Entity",
        "Operation",
        "RelationshipElement",
        "SubmodelElement",
        "SubmodelElementCollection",
        "SubmodelElementList",
    ],
) -> Response[Union[Result, SubmodelElement]]:
    """Creates a new submodel element

    Args:
        submodel_identifier (str):
        json_body (Union['Entity', 'Operation', 'RelationshipElement', 'SubmodelElement',
            'SubmodelElementCollection', 'SubmodelElementList']): Requested submodel element

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Result, SubmodelElement]]
    """

    kwargs = _get_kwargs(
        submodel_identifier=submodel_identifier,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    submodel_identifier: str,
    *,
    client: Client,
    json_body: Union[
        "Entity",
        "Operation",
        "RelationshipElement",
        "SubmodelElement",
        "SubmodelElementCollection",
        "SubmodelElementList",
    ],
) -> Optional[Union[Result, SubmodelElement]]:
    """Creates a new submodel element

    Args:
        submodel_identifier (str):
        json_body (Union['Entity', 'Operation', 'RelationshipElement', 'SubmodelElement',
            'SubmodelElementCollection', 'SubmodelElementList']): Requested submodel element

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Result, SubmodelElement]
    """

    return (
        await asyncio_detailed(
            submodel_identifier=submodel_identifier,
            client=client,
            json_body=json_body,
        )
    ).parsed
