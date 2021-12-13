import requests


def test_no_sentence_sentence_required():
    url = 'http://localhost:5000/'
    response = requests.post(url)
    assert response.text == 'Sentence required'


def test_no_sentence_returns_code_400():
    url = 'http://localhost:5000/'
    response = requests.post(url)
    assert response.status_code == 400


def test_any_sentence_returns_result():
    url = 'http://localhost:5000/'
    response = requests.post(url, json={'sentence': 'Test sentence'})
    assert response.json()['sentiment'] is not None


def test_any_sentence_returns_code_200():
    url = 'http://localhost:5000/'
    response = requests.post(url, json={'sentence': 'Test sentence'})
    assert response.status_code == 200
