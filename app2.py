from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from werkzeug.utils import secure_filename
from fpdf import FPDF
import tempfile
from PIL import Image
import io
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse



app = Flask(__name__)

# Set up configuration
UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure Gemini API
genai.configure(api_key="AIzaSyCzst48MNGT3IJBW29xSuPjBEIHy7MiPEQ")
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 10000,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/write')
def write():
    return render_template('indexCanvas.html')

@app.route('/upload-image')
def upload_image():
    return render_template('indexUpload.html')

@app.route('/audio')
def audio():
    return render_template('indexAudio.html')

@app.route('/site')
def site():
    return render_template('indexSite.html')


@app.route('/analyze-website', methods=['POST'])
def analyze_website():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Validate URL
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return jsonify({'error': 'Invalid URL'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid URL'}), 400

        # Extract website content
        content = extract_website_content(url)
        if not content:
            return jsonify({'error': 'Could not extract website content'}), 400

        # Generate summary using Gemini
        prompt = f"Provide a concise 3-sentence summary of the following website content: {content}"
        response = model.generate_content(prompt)
        
        return jsonify({
            'success': True,
            'summary': response.text
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat-message', methods=['POST'])
def chat_message():
    try:
        message = request.json.get('message')
        url = request.json.get('url')
        
        if not message or not url:
            return jsonify({'error': 'Message and URL are required'}), 400

        # Extract website content
        content = extract_website_content(url)
        if not content:
            return jsonify({'error': 'Could not extract website content'}), 400

        # Generate response using Gemini
        prompt = f"""
        Website Content: {content}
        
        User Question: {message}
        
        Please provide a relevant and informative response based on the website content.
        """
        
        response = model.generate_content(prompt)
        
        return jsonify({
            'success': True,
            'response': response.text
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_website_content(url, max_chars=5000):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts, styles, and navigation elements
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        
        content = soup.get_text(separator=' ', strip=True)
        return content[:max_chars]

    except Exception as e:
        print(f"Error extracting website content: {e}")
        return None
    


@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' in request.files:
        audio_file = request.files['audio']
        if audio_file:
            # Save audio temporarily for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
                temp_audio_file.write(audio_file.read())
                temp_audio_path = temp_audio_file.name

            # Generate text description for the audio
            response_text = gemini(temp_audio_path)
            
            # Convert generated text to a PDF
            output_filename = text_to_pdf(response_text)
            
            # Clean up temporary audio file
            os.remove(temp_audio_path)

            return jsonify({'success': True, 'message': 'Audio uploaded successfully', 'pdf_file': output_filename}), 200

    if 'image' in request.files:
        image_file = request.files['image']
        if image_file:
            # Save image temporarily for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image_file:
                temp_image_file.write(image_file.read())
                temp_image_path = temp_image_file.name

            # Generate text description for the image
            response_text = gemini(temp_image_path)
            
            # Convert generated text to a PDF
            output_filename = text_to_pdf(response_text)
            
            # Clean up temporary image file
            os.remove(temp_image_path)

            return jsonify({'success': True, 'message': 'Image uploaded successfully', 'pdf_file': output_filename}), 200

    return jsonify({'success': False, 'error': 'No file uploaded'}), 400

def gemini(file_path):
    """Processes the image or audio file using the Gemini model to generate descriptive content."""
    # Upload the file
    myfile = genai.upload_file(file_path)

    # Generate content based on the file
    result = model.generate_content([myfile, "\n\n", 
                                     "Can you tell me what we are talking about in the file and create in-depth details to study these topics and related topics?"])

    return result.text

def text_to_pdf(text):
    """Converts provided text into a PDF file and saves it."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    
    output_filename = os.path.join(UPLOAD_FOLDER, "output.pdf")
    pdf.output(output_filename)
    return output_filename  # Return filename for reference

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
