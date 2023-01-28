import requests

api_url = 'http://localhost:8000'

def test_healthcheck():
    response = requests.get(f'{api_url}/__health')
    assert response.status_code == 200

class TestStatus():
    def test_get_empty_status(self):
        response = requests.get(f'{api_url}/v1/orders')
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_create_status(self):
        body = {"status": "New status", "listOrder": "Text"}
        response = requests.post(f'{api_url}/v1/orders', json=body)
        assert response.status_code == 200
        assert response.json().get('status') == 'status'
        assert response.json().get('listOrder') == 'Text'
        assert response.json().get('id') == 0

    def test_get_status_by_id(self):
        response = requests.get(f'{api_url}/v1/orders/0')
        assert response.status_code == 200
        assert response.json().get('status') == 'status'
        assert response.json().get('listOrder') == 'Text'
        assert response.json().get('id') == 0

    def test_get_status(self):
        response = requests.get(f'{api_url}/v1/orders')
        assert response.status_code == 200
        assert len(response.json()) == 1