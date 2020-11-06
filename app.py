import urllib.request
from os.path import splitext
from urllib.parse import urlparse

import textract
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/extract', methods=['POST'])
def extract():
    supportedExts = ["csv", "doc", "docx", "eml", "epub", "gif", "jpg", "jpeg", "json", "html", "htm", "mp3", "msg", "odt", "ogg", "pdf", "png", "pptx", "ps", "rtf", "tiff", "tif", "txt", "wav", "xlsx", "xls"]

    if not request.is_json:
        return jsonify({"success": False, "error": "Missing JSON in request"}), 400

    url = request.json.get("url", None)
    ext = request.json.get("extension", None)

    if not url:
        return jsonify({"success": False, "error": "URL is required"}), 400
    if not ext:
        path = urlparse(url).path
        ext = splitext(path)[1][1:]
        if ext not in supportedExts:
            return jsonify({"success": False, "error": "Please pass the extension parameter"}), 400

    if ext not in supportedExts:
        return jsonify({"success": False, "error": "Unsupported extension. Supported extensions: " + ', '.join(supportedExts)}), 400

    # add try/catch for loading and parsing
    # add binary file input
    # mp3 parsing doesnt work - try deploying on lambda first..
    # add some max file size validation
    # set up ssl
    # set up that server on boot and test

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