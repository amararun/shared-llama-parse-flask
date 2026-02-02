# PDF to Markdown Converter with LlamaIndex API

A Flask application that converts PDF documents to well-formatted Markdown/Text using the LlamaIndex Parse API. Handles complex documents like annual reports, 10-K filings, research papers, and tables.

## Application Structure

```
flask_file_upload/
├── app.py              # Main Flask application
├── requirements.txt    # Project dependencies
├── static/
│   └── styles.css     # Application styling
└── templates/
    └── index.html     # Main UI template
```

## Deployment on Coolify

1. Configure Coolify deployment with:
   ```
   Base Directory: /flask_file_upload
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app --bind 0.0.0.0:5000
   ```

2. Set environment variables in Coolify:
   ```
   LLAMA_API_KEY=your_api_key_here
   ```

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/amararun/llama-parse-flask.git
   cd llama-parse-flask
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   cd flask_file_upload
   pip install -r requirements.txt
   ```

4. Create `.env` file with your LlamaIndex API key:
   ```
   LLAMA_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```bash
   python app.py
   ```

## How It Works

1. User uploads a PDF file through the web interface
2. File is temporarily stored and sent to LlamaIndex Parse API
3. Application polls the API for job status
4. Once processing is complete, user can download the converted markdown/text

## API Endpoints

### `GET /`
- Returns the main application interface
- Response: HTML page with upload form

### `POST /upload`
- Accepts PDF file upload
- Request: Multipart form data with 'file' field
- Response: JSON
  ```json
  {
    "message": "File uploaded successfully, job started."
  }
  ```

### `GET /poll`
- Checks the status of the current parsing job
- Response: JSON
  ```json
  {
    "status": "PENDING|SUCCESS|ERROR"
  }
  ```

### `GET /download`
- Downloads the converted markdown/text file
- Response: Text file attachment
- Only available after successful parsing

## Features

- Clean, modern UI with responsive design
- Real-time job status updates
- Handles complex PDF documents
- Converts tables and formatted text
- CORS enabled for specific domains
- Production-ready with Gunicorn WSGI server

## Error Handling

- Validates file types (PDF only)
- Handles API connection errors
- Provides clear status messages
- Graceful error recovery

## Security

- API key stored in environment variables
- CORS protection enabled
- Temporary file cleanup
- No permanent storage of uploaded files

## Author

Built by [Amar Harolikar](https://www.linkedin.com/in/amarharolikar/)

Explore 30+ open source AI tools for analytics, databases & automation at [tigzig.com](https://tigzig.com)
