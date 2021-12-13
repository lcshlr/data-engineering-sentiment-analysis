from api import app


def test_score_over_plus_o_five_returns_positive():
    assert app.get_sentiment(0.051) == "positive"


def test_score_under_minus_o_five_returns_negative():
    assert app.get_sentiment(-0.051) == "negative"


def test_score_between_minus_o_five_and_plus_o_five_returns_neutral():
    assert app.get_sentiment(0) == "neutral"
