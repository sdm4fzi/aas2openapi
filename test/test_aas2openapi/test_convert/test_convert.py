import pytest
from aas2openapi.models import base
from aas2openapi.convert import convert_aas, convert_pydantic


def test_convert_simple_submodel(example_submodel_instance: base.Submodel):
    basyx_aas_submodel = convert_pydantic.convert_pydantic_model_to_submodel(example_submodel_instance)
    pydantic_model = convert_aas.convert_submodel_to_pydantic_model(basyx_aas_submodel)
    assert pydantic_model.dict() == example_submodel_instance.dict()

def test_convert_simple_aas(example_aas_instance: base.AAS):
    basyx_aas = convert_pydantic.convert_pydantic_model_to_aas(example_aas_instance)
    pydantic_models = convert_aas.convert_object_store_to_pydantic_models(basyx_aas)
    assert len(pydantic_models) == 1	
    pydantic_model = pydantic_models[0]
    assert pydantic_model.dict() == example_aas_instance.dict()

def test_convert_special_submodel(example_special_sm_instance1: base.Submodel, example_special_sm_instance2: base.Submodel):
    basyx_aas_submodel = convert_pydantic.convert_pydantic_model_to_submodel(example_special_sm_instance1)
    pydantic_model = convert_aas.convert_submodel_to_pydantic_model(basyx_aas_submodel)
    assert pydantic_model.dict() == example_special_sm_instance1.dict()
    basyx_aas_submodel = convert_pydantic.convert_pydantic_model_to_submodel(example_special_sm_instance2)
    pydantic_model = convert_aas.convert_submodel_to_pydantic_model(basyx_aas_submodel)
    assert pydantic_model.dict() == example_special_sm_instance2.dict()

def test_convert_special_aas(example_special_aas_instance: base.AAS):
    basyx_aas = convert_pydantic.convert_pydantic_model_to_aas(example_special_aas_instance)
    pydantic_models = convert_aas.convert_object_store_to_pydantic_models(basyx_aas)
    assert len(pydantic_models) == 1	
    pydantic_model = pydantic_models[0]
    assert pydantic_model.dict() == example_special_aas_instance.dict()