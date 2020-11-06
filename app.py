import urllib.request

import textract
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/extract', methods=['GET'])
def extract():
    url = None

    url = request.args.get('url', type=str)
    ext = request.args.get('ext', type=str)

    if url == None:
        return 'URL is required', 400
    if ext == None:
        return 'Ext is required', 400

    filename, headers = urllib.request.urlretrieve(url)
    text = textract.process(filename, extension=ext)
    resp = {}
    resp['success'] = True
    resp['text'] = str(text)

    return jsonify(resp)

if __name__ == '__main__':
    app.run()