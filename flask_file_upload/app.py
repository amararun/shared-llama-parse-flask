from flask import Flask, render_template, request, send_file, jsonify
import requests
import os
import tempfile
from flask_cors import CORS

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # In production, environment variables should be set in Coolify
    pass

app = Flask(__name__)

# Apply CORS settings to allow only requests from tigzig.com
CORS(app, resources={r"/*": {"origins": ["https://www.tigzig.com", "https://tigzig.com"]}})

# Get the API key from environment variables for security
API_KEY = os.getenv('LLAMA_API_KEY')
if not API_KEY:
    print("Warning: LLAMA_API_KEY environment variable not set")

# Global variables for job ID and status
job_id = None
status = 'pending'
original_file_name = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global job_id, status, original_file_name
    file = request.files['file']
    original_file_name = file.filename  # Save the original file name

    # Use temporary storage for the file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        file_path = temp_file.name
        file.save(file_path)  # Save file to temporary path

    try:
        response = requests.post(
            'https://api.cloud.llamaindex.ai/api/parsing/upload',
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'accept': 'application/json'
            },
            files={'file': (file.filename, open(file_path, 'rb'), 'application/pdf')}
        )

        response.raise_for_status()  # Raises an HTTPError for bad responses

        job_id = response.json().get('id')
        if not job_id:
            return jsonify({'message': 'Error: job_id not found in the response', 'response': response.json()}), 400

        status = response.json().get('status', 'pending')
        return jsonify({'message': 'File uploaded successfully, job started.'})

    except requests.exceptions.HTTPError as err:
        return jsonify({'message': f'Error uploading file: {err}'}), 400
    except Exception as e:
        return jsonify({'message': f'Unexpected error: {str(e)}'}), 500
    finally:
        # Clean up the temporary file after the request
        if os.path.exists(file_path):
            os.remove(file_path)



@app.route('/poll', methods=['GET'])
def poll_status():
    global status
    if job_id is None:
        return jsonify({'status': 'no job'})

    response = requests.get(
        f'https://api.cloud.llamaindex.ai/api/parsing/job/{job_id}',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )

    if response.status_code == 200:
        status = response.json().get('status', 'blank')
    else:
        status = 'error'

    return jsonify({'status': status})

@app.route('/download', methods=['GET'])
def download_file():
    global status, job_id, original_file_name

    if status.lower() != 'success' and status.lower() != 'completed':
        return jsonify({'message': 'Job is not completed yet'}), 400

    # Fetch the result from the API
    response = requests.get(
        f'https://api.cloud.llamaindex.ai/api/parsing/job/{job_id}/result/markdown',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )

    if response.status_code == 200:
        base_name = os.path.splitext(original_file_name)[0]
        file_name = f"{base_name}.txt"
        
        # Use temporary file to store the markdown result
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
            result_path = temp_file.name
            text = response.text.replace('\\n', '\n')  # Ensure newlines are respected
            temp_file.write(text.encode('utf-8'))  # Write the markdown text to the temporary file

        # Send the file as an attachment
        return send_file(result_path, as_attachment=True, download_name=file_name)

    return jsonify({'message': 'Error retrieving the result'}), 400

# The `if __name__ == '__main__':` block is not needed for Vercel

if __name__ == '__main__':
    # Only used for local development
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
