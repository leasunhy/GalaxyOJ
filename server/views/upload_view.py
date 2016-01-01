from . import upload

from werkzeug.security import safe_join
from werkzeug import secure_filename
from flask import request, jsonify, url_for, current_app, abort, send_from_directory

import hashlib
from datetime import datetime


# for CKEDITOR
@upload.route('/upload_image', methods=['POST'])
def upload_image():
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ['jpg', 'png']

    file = request.files['upload']
    error = ''
    if not file:
        return jsonify(uploaded=0, error={'message': 'Please select a file.'})
    elif not allowed_file(file.filename):
        return jsonify(uploaded=0, error={'message': 'File extension not allowed.'})
    else:
        filename = file.filename
        extension = '.' + filename.rsplit('.', 1)[1]
        filename = hashlib.md5((filename + str(datetime.utcnow())).encode('utf-8')).hexdigest() + extension
        filepath = safe_join(current_app.config['IMAGE_UPLOAD_FOLDER'], filename)
        if not filepath:
            return jsonify(uploaded=0, error={'message': 'Filename illegal.'})
        file.save(filepath)
        callback = request.args.get('CKEditorFuncNum')
        url = url_for('upload.fetch', filename=filename)
        res = """
            <script type="text/javascript">window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s')</script>
        """ % (callback, url, error)
        return res, 200, {"Content-Type": "text/html"}


@upload.route('/fetch_image/<path:filename>')
def fetch(filename):
    filename = secure_filename(filename.strip())
    if not filename:
        abort(404)
    return send_from_directory(current_app.config['IMAGE_UPLOAD_FOLDER'], filename)


