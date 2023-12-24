from flask import Flask, request, jsonify, send_from_directory, Blueprint
from werkzeug.utils import secure_filename
import os
import threading
import subprocess
import logging

app = Flask(__name__)

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

UPLOAD_FOLDER = '/data/uploads'
OUTPUT_FOLDER = '/data/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def convert_file(file_path, output_file, results, conversion_success):
    try:
        cmd = ['/app/caj2pdf/caj2pdf', 'convert', file_path, '-o', output_file]
        subprocess.run(cmd, check=True)
        results.append(output_file)
        conversion_success.append(True)
    except Exception as e:
        logger.error(f"Error converting file {file_path}: {e}")
        conversion_success.append(False)

@api_v1.route('/hello', methods=['GET'])
def hello_world():
    return "Hello World"

@api_v1.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist('file')
    if len(files) > 10:
        return jsonify({"error": "Too many files"}), 400

    threads = []
    results = []
    conversion_success = []

    for file in files:
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if not file.filename.endswith('.caj'):
            return jsonify({"error": "Invalid file type"}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            file.save(file_path)
        except Exception as e:
            logger.error(f"Error saving file {filename}: {e}")
            return jsonify({"error": f"Could not save file {filename}"}), 500

        output_file = os.path.join(OUTPUT_FOLDER, filename.replace('.caj', '.pdf'))
        thread = threading.Thread(target=convert_file, args=(file_path, output_file, results, conversion_success))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if not all(conversion_success):
        return jsonify({"error": "Error occurred during file conversion"}), 500

    server_root = request.url_root.rstrip('/')
    download_links = [{"file_name": os.path.basename(file), "url": f"{server_root}/api/v1/download/{os.path.basename(file)}"} for file in results]
    return jsonify({"message": "Files uploaded and converted", "download_links": download_links}), 200

@api_v1.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

app.register_blueprint(api_v1)

if __name__ == '__main__':
    pass  # app.run(debug=True, host='0.0.0.0', port=5000)
