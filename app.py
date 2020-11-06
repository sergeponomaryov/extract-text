import urllib.request
from os.path import splitext
from urllib.parse import urlparse

import textract
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/extract', methods=['GET'])
def extract():
    supportedExts = ["csv", "doc", "docx", "eml", "epub", "gif", "jpg", "jpeg", "json", "html", "htm", "mp3", "msg", "odt", "ogg", "pdf", "png", "pptx", "ps", "rtf", "tiff", "tif", "txt", "wav", "xlsx", "xls"]
    url = None

    url = request.args.get('url', type=str)
    ext = request.args.get('extension', type=str)

    if url == None:
        return 'URL is required', 400
    if ext == None:
        path = urlparse(url).path
        ext = splitext(path)[1][1:]
        if ext not in supportedExts:
            return "Please pass the extension parameter", 400

    if ext not in supportedExts:
        return "Unsupported extension. Supported extensions: " + ', '.join(supportedExts), 400

    # jsonify errors, and add try/catch for parsing
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