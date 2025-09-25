# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator, LANGUAGES

# Initialize Flask app
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing
CORS(app) 
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate_text():
    """API endpoint to translate text."""
    try:
        data = request.get_json()

        if not data or 'text' not in data or 'target_lang' not in data:
            return jsonify({'error': 'Invalid request. "text" and "target_lang" are required.'}), 400

        original_text = data.get('text')
        target_language = data.get('target_lang')
        
        if not original_text:
            return jsonify({'error': 'Text to translate cannot be empty.'}), 400

        if target_language not in LANGUAGES:
            return jsonify({'error': f'Invalid target language code: {target_language}'}), 400

        # Perform the translation
        translation_result = translator.translate(original_text, dest=target_language)
        
        # Prepare the successful response
        response = {
            'translated_text': translation_result.text,
            'detected_source_language': LANGUAGES.get(translation_result.src, translation_result.src).capitalize()
        }
        
        return jsonify(response), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An unexpected error occurred during translation.'}), 500

# The app.run() part is only for local development and will be ignored by Render's server.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
