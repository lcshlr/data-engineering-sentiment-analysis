import requests

def test_no_sentence_sentence_required():
    url = 'http://localhost:5000/'
    response = requests.post(url)
    assert response.text == 'Sentence required'

def test_positive_sentence_is_positive():
    url = 'http://localhost:5000/'
    response = requests.post(url, json={'sentence': 'I like Data engineering'})
    assert response.json()['sentiment'] == 'positive'

def test_negative_sentence_is_negative():
    url = 'http://localhost:5000/'
    response = requests.post(url, json={"sentence": "I don't really like Data engineering"})
    assert response.json()['sentiment'] == 'negative'