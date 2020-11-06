import urllib.request
from os.path import splitext
from urllib.parse import urlparse
import tempfile

import textract
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/extract', methods=['POST'])
def extract():
    supportedExts = ["csv", "doc", "docx", "eml", "epub", "gif", "jpg", "jpeg", "json", "html", "htm", "mp3", "msg", "odt", "ogg", "pdf", "png", "pptx", "ps", "rtf", "tiff", "tif", "txt", "wav", "xlsx", "xls"]

    # parse/validate request
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
    # add some max file size validation. 100M?
    # uwsgi - make sure it works when you close terminal, and on boot. Errors can be seen from worker, log them somewhere. supervisor
    # restart server on changes
    # add firewall of request ips..
    # virtual env uwsgi just so that nothing breaks when you add more projects.

    # create temp file
    temp = tempfile.NamedTemporaryFile(suffix='.'+ext)

    # set user agent as to not get 403s
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36')]
    urllib.request.install_opener(opener)

    # load url into temp file
    urllib.request.urlretrieve(url, temp.name)

    # process it
    text = textract.process(temp.name, extension=ext, encoding = 'unicode_escape')

    # close temp file
    temp.close()

    # respond
    resp = {}
    resp['success'] = True
    resp['text'] = text.decode("utf-8")

    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')