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

    # add guessing ext from url
    # add binary file input
    # parse all weird characters etc, should be pure text? but also /n's and stuff.

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36')]
    urllib.request.install_opener(opener)
    filename, headers = urllib.request.urlretrieve(url)
    text = textract.process(filename, extension=ext)
    resp = {}
    resp['success'] = True
    resp['text'] = str(text)

    return jsonify(resp)

if __name__ == '__main__':
    app.run()