import base64

from aas2openapi.convert.convert_pydantic import remove_empty_lists, rename_data_specifications_for_basyx, rename_semantic_id_for_basyx

import basyx.aas.adapter.json
from basyx.aas import model
import json
from typing import Union
import socket


def get_base64_from_string(string: str) -> str:
    b = base64.b64encode(bytes(string, "utf-8"))  # bytes
    base64_str = b.decode("utf-8")  # convert bytes to string
    return base64_str


def transform_client_to_basyx_model(client_model: dict) -> Union[model.AssetAdministrationShell, model.Submodel]:
    """
    Function to transform a client model to a basyx model
    Args:
        response_model (dict): dictionary from server client that needs to be transformed
    Returns:
        Union[model.AssetAdministrationShell, model.Submodel]: basyx model from the given client model
    """
    rename_data_specifications_for_basyx(client_model)
    rename_semantic_id_for_basyx(client_model)
    remove_empty_lists(client_model)
    json_model = json.dumps(client_model, indent=4)
    basyx_model = json.loads(json_model, cls=basyx.aas.adapter.json.AASFromJsonDecoder)
    return basyx_model

def is_server_online(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 2 seconds
        sock.connect((host, port))
        sock.close()
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False