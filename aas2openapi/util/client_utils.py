import base64
import os
from urllib.parse import urlparse

from fastapi import HTTPException

from aas2openapi.convert.convert_pydantic import (
    remove_empty_lists,
)

import basyx.aas.adapter.json
from basyx.aas import model
import json
from typing import Union, Tuple, Any
import socket
from logging.config import dictConfig
import logging
from aas2openapi.util.logging_util import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("aas2openapi")


def load_aas_and_submodel_repository_adress() -> Tuple[str, str]:
    """
    Function to load the adress of the aas and submodel repository from the .env file. If no environment file is found, the default adress is used.

    Returns:
        Tuple[str, str]: Tuple of aas and submodel repository adress
    """
    try:
        AAS_SERVER_ADRESS = (
            "http://"
            + os.getenv("AAS_SERVER_HOST")
            + ":"
            + os.getenv("AAS_SERVER_PORT")
        )
        SUBMODEL_SERVER_ADRESS = (
            "http://"
            + os.getenv("SUBMODEL_SERVER_HOST")
            + ":"
            + os.getenv("SUBMODEL_SERVER_PORT")
        )
    except:
        logger.warning(
            "No environment variables for AAS and Submodel Repository addresses and ports found. Using default values on localhost:8081 and localhost:8082."
        )
        os.environ["AAS_SERVER_HOST"] = "localhost"
        os.environ["AAS_SERVER_PORT"] = "8081"
        os.environ["SUBMODEL_SERVER_HOST"] = "localhost"
        os.environ["SUBMODEL_SERVER_PORT"] = "8082"
        AAS_SERVER_ADRESS = (
            "http://"
            + os.getenv("AAS_SERVER_HOST")
            + ":"
            + os.getenv("AAS_SERVER_PORT")
        )
        SUBMODEL_SERVER_ADRESS = (
            "http://"
            + os.getenv("SUBMODEL_SERVER_HOST")
            + ":"
            + os.getenv("SUBMODEL_SERVER_PORT")
        )
    return AAS_SERVER_ADRESS, SUBMODEL_SERVER_ADRESS


def get_base64_from_string(string: str) -> str:
    b = base64.b64encode(bytes(string, "utf-8"))  # bytes
    base64_str = b.decode("utf-8")  # convert bytes to string
    return base64_str


def transform_client_to_basyx_model(
    client_model: dict | Any,
) -> Union[model.AssetAdministrationShell, model.Submodel]:
    """
    Function to transform a client model to a basyx model
    Args:
        response_model (dict): dictionary from server client that needs to be transformed
    Returns:
        Union[model.AssetAdministrationShell, model.Submodel]: basyx model from the given client model
    """
    if not isinstance(client_model, dict):
        client_model = client_model.to_dict()
    remove_empty_lists(client_model)
    json_model = json.dumps(client_model, indent=4)
    basyx_model = json.loads(json_model, cls=basyx.aas.adapter.json.AASFromJsonDecoder)
    return basyx_model




def is_server_online(adress: str):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        parsed_url = urlparse(adress)
        host = parsed_url.hostname
        port = parsed_url.port
        sock.settimeout(2)  # 2 seconds
        sock.connect((host, port))
        sock.close()
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False


async def check_aas_and_sm_server_online():
    AAS_SERVER, SUBMODEL_SERVER = load_aas_and_submodel_repository_adress()
    if not is_server_online(AAS_SERVER):
        raise HTTPException(status_code=503, detail=f"Eror 503: AAS Server cannot be reached at adress {AAS_SERVER}")
    if not is_server_online(SUBMODEL_SERVER):
        raise HTTPException(status_code=503, detail=f"Eror 503: Submodel Server cannot be reached at adress {SUBMODEL_SERVER}")
