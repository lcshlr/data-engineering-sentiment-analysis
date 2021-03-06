from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

def get_sentiment(score):
    """Get sentiment based on score
    Args:
        score: the sentiment analysis score
    Returns:
        positive/neutral/negative related to the score
    """
    if score >= 0.05:
        return 'positive'
    elif score <= -0.05:
        return 'negative'
    return 'neutral'

@app.route('/', methods=['POST'])
def sentiment_analysis():
    """Get sentiment based on score
    Args:
        sentence: the sentence we want to predict the sentiment
    Returns:
        positive/neutral/negative related to the sentence
    Raises:
        Error: if no sentence in parameters
    """
    data = request.json
    
    if not data or not 'sentence' in data.keys():
        return Response('Sentence required', status=400)
    sentence = data['sentence']

    sid_obj = SentimentIntensityAnalyzer()
    sentiment_score = sid_obj.polarity_scores(sentence)['compound']
    return jsonify({'sentiment': get_sentiment(sentiment_score)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')