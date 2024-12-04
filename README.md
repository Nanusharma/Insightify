# AI Note-Taking Web Application: Insightify [ Insightify_Report.pdf contains the detailed report ]

## Project Overview

This web application revolutionizes note-taking by leveraging artificial intelligence to convert multiple input methods into structured, readable notes. Users can create notes through handwriting, image uploads, and audio recordings.

## Key Features

- Multiple input methods:
  - Handwritten notes
  - Image uploads
  - Audio recordings
- AI-powered note generation using Google's Gemini API
- PDF export functionality
- User-friendly web interface

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Integration**: Google Gemini API
- **PDF Generation**: FPDF

## Prerequisites

- Python 3.8+
- Flask
- Google Gemini API credentials
- FPDF library
- Modern web browser

## Installation

1. Clone the repository
```bash
git clone [https://github.com/yourusername/ai-note-taking-app.git](https://github.com/Nanusharma/Insightify.git)
```
2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up Google Gemini API credentials
   - Obtain API key from Google Cloud Console
   - Set environment variable or update configuration file

## Running the Application

```bash
flask run
```

## Usage

1. Navigate to homepage
2. Choose input method:
   - Write notes manually
   - Upload an image
   - Record audio
3. Generate and download PDF

## Project Limitations

- Primary language support: English
- Web-based platform compatibility
- Basic note organization features

## Future Enhancements

- Multi-language support
- Advanced note organization
- Enhanced AI processing capabilities
