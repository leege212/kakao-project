from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return jsonify({"message": "Server is running."})


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "요청에 파일이 포함되어 있지 않습니다."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "선택된 파일이 없습니다."}), 400

    if file and allowed_file(file.filename):
        # 보안을 위해 파일명 이스케이프 처리
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        return jsonify({
            "message": "파일 업로드 성공",
            "filename": filename,
            "saved_path": save_path
        }), 200
    else:
        return jsonify({"error": "PDF 파일만 업로드 가능합니다."}), 400


@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({
        "uploaded_files": files,
        "count": len(files)
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)