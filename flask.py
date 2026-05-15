from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 1. 파일이 저장될 폴더 설정
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 2. 허용할 파일 확장자 설정 (PDF만 허용)
ALLOWED_EXTENSIONS = {'pdf'}

# 3. uploads 폴더가 없다면 자동으로 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 4. 파일 확장자가 허용된 것(PDF)인지 확인하는 함수
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 5. 파일 업로드 API 엔드포인트 (/upload)
@app.route('/upload', methods=['POST'])
def upload_file():
    # 클라이언트가 보낸 요청 안에 'file'이라는 데이터가 있는지 확인
    if 'file' not in request.files:
        return jsonify({'error': '요청에 파일이 포함되어 있지 않습니다.'}), 400
    
    file = request.files['file']
    
    # 파일은 보냈는데 이름이 비어있는 경우 (파일 선택창에서 취소 등)
    if file.filename == '':
        return jsonify({'error': '선택된 파일이 없습니다.'}), 400
    
    # 파일이 정상적으로 존재하고, 확장자가 PDF일 경우
    if file and allowed_file(file.filename):
        # secure_filename: 한글이나 해킹 위험이 있는 특수문자가 들어간 파일명을 안전하게 변환
        filename = secure_filename(file.filename)
        
        # 저장할 전체 경로 생성 (예: uploads/my_document.pdf)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # 실제 서버에 파일 저장
        file.save(file_path)
        
        return jsonify({
            'message': 'PDF 파일 업로드 성공!',
            'filename': filename,
            'saved_path': file_path
        }), 200
    else:
        return jsonify({'error': 'PDF 파일만 업로드할 수 있습니다.'}), 400

# 6. Flask 서버 실행
if __name__ == '__main__':
    # debug=True: 코드를 수정하면 서버가 자동으로 재시작됨
    app.run(debug=True, port=5000)