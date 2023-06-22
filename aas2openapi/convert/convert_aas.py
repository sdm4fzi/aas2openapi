from __future__ import annotations

from aas2openapi.models import base
from basyx.aas import model

def convert_aas_to_pydantic_model(aas: model.AssetAdministrationShell) -> base.AAS:
    """
    Converts an AAS to a Pydantic model.
    """
    # TODO: implement conversion here!
    pass

def convert_sm_to_pydantic_model(sm: model.Submodel) -> base.Submodel:
    """
    Converts a Submodel to a Pydantic model.
    """
    # TODO: implement conversion here!
    pass