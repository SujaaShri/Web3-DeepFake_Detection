from flask import Flask, render_template, request
import hashlib
import os

from blockchain import register_hash_on_chain, verify_hash_on_chain

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def generate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()


@app.route('/')
def home():
    return render_template('index.html')


# 🔹 Upload & Register on Blockchain
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    file_hash = generate_hash(file_path)

    # Register hash on blockchain
    try:
        tx_hash = register_hash_on_chain(file_hash)
        status = "Hash registered on blockchain successfully!"
    except Exception as e:
        tx_hash = "Transaction failed"
        status = str(e)

    return f"""
    <h2>File Uploaded Successfully!</h2>
    <p><strong>SHA-256 Hash:</strong> {file_hash}</p>
    <p><strong>Blockchain TX:</strong> {tx_hash}</p>
    <p><strong>Status:</strong> {status}</p>
    <a href="/">Upload Another File</a>
    """


# 🔹 Verify from Blockchain
@app.route('/verify', methods=['POST'])
def verify_file():
    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    file_hash = generate_hash(file_path)

    try:
        verified = verify_hash_on_chain(file_hash)
        status = "AUTHENTIC (On Blockchain)" if verified else "NOT VERIFIED"
    except Exception as e:
        status = str(e)

    return f"""
    <h2>Verification Result</h2>
    <p><strong>SHA-256 Hash:</strong> {file_hash}</p>
    <p><strong>Status:</strong> {status}</p>
    <a href="/">Go Back</a>
    """


if __name__ == '__main__':
    app.run(debug=True)