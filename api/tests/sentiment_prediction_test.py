import requests


def test_positive_sentence_is_positive():
    url = 'http://localhost:5000/'
    response = requests.post(url, json={'sentence': 'I like Data engineering'})
    assert response.json()['sentiment'] == 'positive'


def test_negative_sentence_is_negative():
    url = 'http://localhost:5000/'
    response = requests.post(url, json={"sentence": "I don't really like Data engineering"})
    assert response.json()['sentiment'] == 'negative'


def test_neutral_sentence_is_neutral():
    url = 'http://localhost:5000/'
    response = requests.post(url, json={"sentence": "Test"})
    assert response.json()['sentiment'] == 'neutral'


def test_positive_smileys_are_recognized():
    url = 'http://localhost:5000/'
    response = requests.post(url, json={'sentence': ':)'})
    assert response.json()['sentiment'] == 'positive'


def test_negative_smileys_are_recognized():
    url = 'http://localhost:5000/'
    response = requests.post(url, json={'sentence': ':('})
    assert response.json()['sentiment'] == 'negative'
