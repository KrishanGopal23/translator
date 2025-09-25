# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator

# Initialize Flask app
app = Flask(__name__)
CORS(app) 

@app.route('/translate', methods=['POST'])
def translate_text():
    """API endpoint to translate text using deep-translator."""
    try:
        data = request.get_json()

        if not data or 'text' not in data or 'target_lang' not in data:
            return jsonify({'error': 'Invalid request. "text" and "target_lang" are required.'}), 400

        original_text = data.get('text')
        target_language = data.get('target_lang')
        
        if not original_text:
            return jsonify({'error': 'Text to translate cannot be empty.'}), 400

        # Perform the translation using deep-translator
        translated_text = GoogleTranslator(source='auto', target=target_language).translate(original_text)
        
        # Prepare the successful response
        response = {
            'translated_text': translated_text
        }
        
        return jsonify(response), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        # The library raises an error for invalid language codes, which this will catch.
        return jsonify({'error': 'An unexpected error occurred. Check if the language code is valid.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
