import textract
from flask import Flask, request
import urllib.request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/extract', methods=['GET'])
def extract():
    url = None

    url = request.args.get('url', type=str)

    if url == None:
        return 'URL is required', 400
    urllib.request.urlretrieve(url, "tmp.html")

    text = textract.process("tmp.html")
    return text


if __name__ == '__main__':
    app.run()