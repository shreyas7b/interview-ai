from flask import Flask
from flask import Flask, request, jsonify
import boto3
import fitz  # PyMuPDF
from io import BytesIO

app = Flask(__name__)

s3_client = boto3.client('s3', region_name='ap-south-1')
@app.route('/')
def hello_world():
    return 'Hello, World!'

def download_file_from_s3(bucket_name, object_key):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        return response['Body'].read()
    except Exception as e:
        print(f"Error downloading file from S3: {e}")
        raise

def input_pdf_setup(bucket_name, object_key):
    try:
        file_content = download_file_from_s3(bucket_name, object_key)
        
        pdf_text = ""
        with fitz.open(stream=file_content, filetype="pdf") as pdf:
            for page in pdf:
                pdf_text += page.get_text()

        return pdf_text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    data = request.json
    bucket_name = data.get('bucket_name')
    object_key = data.get('object_key')

    if not bucket_name or not object_key:
        return jsonify({"error": "bucket_name and object_key are required"}), 400

    try:
        pdf_text = input_pdf_setup(bucket_name, object_key)
        return jsonify({"pdf_text": pdf_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
