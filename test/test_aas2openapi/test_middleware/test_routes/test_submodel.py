import json
import pytest

@pytest.mark.order(200)
def test_create_submodel(client, example_aas_instance):
    process_model = example_aas_instance.process_model
    process_model.id = "PMP2"
    data = example_aas_instance.dict()
    del data["process_model"]
    data = json.dumps(data)
    class_name = example_aas_instance.__class__.__name__
    response = client.post(url=f"/{class_name}/", content=data)
    assert response.status_code == 200
    data = process_model.json()
    sm_class_name = process_model.__class__.__name__
    response = client.post(url=f"/{class_name}/{example_aas_instance.id}/{sm_class_name}", content=data)
    assert response.status_code == 200
    response = client.post(url=f"/{class_name}/{example_aas_instance.id}/{sm_class_name}", content=data)
    assert response.status_code == 413
    response = client.get(url=f"/{class_name}/{example_aas_instance.id}/")
    assert response.status_code == 200
    assert response.json()["process_model"] == process_model.dict()


@pytest.mark.order(201)
def test_get_submodel(client, example_aas_instance, example_submodel_instance):
    class_name = example_aas_instance.__class__.__name__
    response = client.get(url=f"/{class_name}/{example_aas_instance.id}/BillOfMaterial")
    assert response.status_code == 200
    assert response.json() == example_submodel_instance.dict()

@pytest.mark.order(202)
def test_update_submodel(client, example_aas_instance):
    class_name = example_aas_instance.__class__.__name__
    new_process_model = example_aas_instance.process_model
    new_process_model.processes = ["new_process"]
    data = new_process_model.json()
    response = client.put(url=f"/{class_name}/{example_aas_instance.id}/ProcessModel", content=data)
    assert response.status_code == 200
    updated_aas = client.get(url=f"/{class_name}/{example_aas_instance.id}/")
    assert updated_aas.json()["process_model"]["processes"] == ["new_process"]
    new_process_model.id = "new_id"
    response = client.put(url=f"/{class_name}/{example_aas_instance.id}/ProcessModel", content=data)
    assert response.status_code == 200

@pytest.mark.order(203)
def test_delete_submodel(client, example_aas_instance):
    class_name = example_aas_instance.__class__.__name__
    response = client.delete(url=f"/{class_name}/{example_aas_instance.id}/ProcessModel")
    assert response.status_code == 200
    response = client.get(url=f"/{class_name}/{example_aas_instance.id}/ProcessModel")
    assert response.status_code == 411
    response = client.get(url=f"/{class_name}/{example_aas_instance.id}/")
    assert response.status_code == 200
    assert response.json()["process_model"] == None