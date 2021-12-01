from flask import Flask

app = Flask(__name__)

@app.route('/')
def sentiment_analysis():
    return 'hello world'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')