from flask import Flask, request, jsonify
import fitz  # PyMuPDF

app = Flask(__name__)

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        pdf_text = ""
        with fitz.open(stream=file.stream.read(), filetype="pdf") as pdf:
            for page in pdf:
                pdf_text += page.get_text()

        return jsonify({"pdf_text": pdf_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
