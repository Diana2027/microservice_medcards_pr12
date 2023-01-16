import requests

api_url = 'http://localhost:8001'

def test_healthcheck():
    response = requests.get(f'{api_url}/__health')
    assert response.status_code == 200

class TestMedcards():
    def test_get_empty_cards(self):
        response = requests.get(f'{api_url}/v1/cards')
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_create_card(self):
        body = { "title": "New medcard", "fio": "FIO" }
        response = requests.post(f'{api_url}/v1/cards', json = body)
        assert response.status_code == 200
        assert response.json().get('title') == 'New medcard'
        assert response.json().get('fio') == 'FIO'
        assert response.json().get('id') == 0

    def test_get_card_by_id(self):
        response = requests.get(f'{api_url}/v1/cards/0')
        assert response.status_code == 200
        assert response.json().get('title') == 'New medcard'
        assert response.json().get('fio') == 'FIO'
        assert response.json().get('id') == 0

    def test_get_not_empty_cards():
        response = requests.get(f'{api_url}/v1/cards')
        assert response.status_code == 200
        assert len(response.json()) == 1