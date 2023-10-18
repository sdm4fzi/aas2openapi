import pytest


@pytest.mark.order(100)
def test_create_aas(client, example_aas_instance):
    data = example_aas_instance.json()
    class_name = example_aas_instance.__class__.__name__
    response = client.post(url=f"/{class_name}/", content=data)
    assert response.status_code == 200 
    response = client.post(url=f"/{class_name}/", content=data)
    assert response.status_code == 400

@pytest.mark.order(101)
def test_get_all_aas(client, example_aas_instance):
    class_name = example_aas_instance.__class__.__name__
    response = client.get(url=f"/{class_name}/")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == [example_aas_instance.dict()]

@pytest.mark.order(102)
def test_get_aas(client, example_aas_instance):
    class_name = example_aas_instance.__class__.__name__
    response = client.get(url=f"/{class_name}/{example_aas_instance.id_}/")
    assert response.status_code == 200
    assert response.json() == example_aas_instance.dict()

@pytest.mark.order(103)
def test_update_aas(client, example_aas_instance):
    class_name = example_aas_instance.__class__.__name__
    example_aas_instance.id_short = "new_id_short"
    example_aas_instance.process_model.processes = ["new_process"]
    response = client.put(url=f"/{class_name}/{example_aas_instance.id_}/", content=example_aas_instance.json())
    assert response.status_code == 200
    updated_aas = client.get(url=f"/{class_name}/{example_aas_instance.id_}/")
    assert updated_aas.json()["id_short"] == "new_id_short"
    assert updated_aas.json()["process_model"]["processes"] == ["new_process"]
    example_aas_instance.process_model.id_ = "new_id"
    response = client.put(url=f"/{class_name}/{example_aas_instance.id_}/", content=example_aas_instance.json())
    assert response.status_code == 400

@pytest.mark.order(104)
def test_delete_aas(client, example_aas_instance):
    class_name = example_aas_instance.__class__.__name__
    response = client.delete(url=f"/{class_name}/{example_aas_instance.id_}/")
    assert response.status_code == 200
    response = client.get(url=f"/{class_name}/{example_aas_instance.id_}/")
    assert response.status_code == 400