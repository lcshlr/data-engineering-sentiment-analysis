import pandas as pd
from sklearn.metrics import accuracy_score
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_vader_sentence_compound(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    compound = sid_obj.polarity_scores(sentence)['compound']
    if compound > 0.05:
        return 1
    elif (compound >= -0.05) and (compound <= 0.05):
        return None
    else:
        return 0


def test_model_accuracy():
    df = pd.read_csv('api/tests/resources/weather-agg-DFE.csv')

    # columns with all nan values
    df = df.drop("_canary", axis=1)
    df = df.drop("gold_answer", axis=1)

    df['vader'] = df.apply(lambda x: get_vader_sentence_compound(x['tweet_text']), axis=1)

    df['label'] = df['what_emotion_does_the_author_express_specifically_about_the_weather'] \
        .apply(lambda x: 1 if x == 'Positive' else (None if x == 'Neutral / author is just sharing information' or x == 'Tweet not related to weather condition' else 0))

    # Evaluate results
    accuracy = accuracy_score(df.dropna()["label"].values, df.dropna()["vader"].values)
    print(f'Accuracy: {accuracy_score(df.dropna()["label"].values, df.dropna()["vader"].values)}')

    assert accuracy > 0.75
