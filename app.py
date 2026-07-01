from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import json
import os
from datetime import datetime
from gtts import gTTS
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-for-sessions'

# Path to JSON database
DATA_DIR = 'data'
NOUNS_DB = os.path.join(DATA_DIR, 'nouns.json')
VERBS_DB = os.path.join(DATA_DIR, 'verbs.json')
AUDIO_DIR = 'static/audio'
PROGRESS_DIR = 'progress'
PROGRESS_FILE = os.path.join(PROGRESS_DIR, 'progress.json')

def load_flashcards(category='verbs'):
    """Load flashcards from JSON file based on category"""
    db_path = VERBS_DB if category == 'verbs' else NOUNS_DB
    
    if not os.path.exists(db_path):
        # Create empty database if it doesn't exist
        save_flashcards([], category)
        return []
    
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('flashcards', [])
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_flashcards(flashcards, category='verbs'):
    """Save flashcards to JSON file based on category"""
    db_path = VERBS_DB if category == 'verbs' else NOUNS_DB
    
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    data = {'flashcards': flashcards}
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_next_id(flashcards):
    """Get the next available ID"""
    if not flashcards:
        return 1
    return max(card['id'] for card in flashcards) + 1

def load_progress():
    """Load user progress from JSON file"""
    if not os.path.exists(PROGRESS_FILE):
        return {}
    
    try:
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_progress(progress):
    """Save user progress to JSON file"""
    os.makedirs(PROGRESS_DIR, exist_ok=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)

def get_user_progress(category):
    """Get the current card index for a category"""
    progress = load_progress()
    return progress.get(category, 0)

def set_user_progress(category, index):
    """Save the current card index for a category"""
    progress = load_progress()
    progress[category] = index
    save_progress(progress)

def generate_audio(text, card_id, category):
    """Generate German audio for a flashcard and save it"""
    try:
        # Ensure audio directory exists
        os.makedirs(AUDIO_DIR, exist_ok=True)
        
        # Create filename: category_cardid.mp3
        audio_filename = f"{category}_{card_id}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)
        
        # Generate audio using gTTS
        tts = gTTS(text=text, lang='de', slow=False)
        tts.save(audio_path)
        
        return audio_filename
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

def get_or_generate_audio(text, card_id, category):
    """Get audio file or generate it if it doesn't exist"""
    try:
        # Ensure audio directory exists
        os.makedirs(AUDIO_DIR, exist_ok=True)
        
        audio_filename = f"{category}_{card_id}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)
        
        # If audio file doesn't exist, generate it
        if not os.path.exists(audio_path):
            tts = gTTS(text=text, lang='de', slow=False)
            tts.save(audio_path)
        
        return audio_path
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

def delete_audio(card_id, category):
    """Delete audio file for a flashcard"""
    try:
        audio_filename = f"{category}_{card_id}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
    except Exception as e:
        print(f"Error deleting audio: {e}")

@app.route('/')
def index():
    """Main page - display flashcards"""
    category = request.args.get('category', 'verbs')
    flashcards = load_flashcards(category)
    
    # Get saved progress for this category
    current_index = get_user_progress(category)
    
    # Ensure current_index is valid
    if current_index < 0:
        current_index = 0
    elif current_index >= len(flashcards) and flashcards:
        current_index = len(flashcards) - 1
    
    current_card = flashcards[current_index] if flashcards else None
    total_cards = len(flashcards)
    
    return render_template('index.html', 
                         card=current_card, 
                         index=current_index, 
                         total=total_cards,
                         category=category)

@app.route('/set-progress', methods=['POST'])
def set_progress():
    """Set user progress (called via AJAX)"""
    try:
        data = request.json
        category = data.get('category', 'verbs')
        index = data.get('index', 0)
        
        set_user_progress(category, index)
        
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error setting progress: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/audio/<category>/<int:card_id>')
def get_audio(category, card_id):
    """Get or generate audio for a flashcard"""
    try:
        # Get the flashcard
        flashcards = load_flashcards(category)
        card = next((c for c in flashcards if c['id'] == card_id), None)
        
        if not card:
            return "Card not found", 404
        
        # Get or generate audio
        audio_path = get_or_generate_audio(card['deutsch'], card_id, category)
        
        if not audio_path or not os.path.exists(audio_path):
            return "Could not generate audio", 500
        
        return send_file(audio_path, mimetype='audio/mpeg')
    except Exception as e:
        print(f"Error serving audio: {e}")
        return f"Error: {str(e)}", 500

@app.route('/add', methods=['GET', 'POST'])
def add_card():
    """Add a new flashcard"""
    category = request.args.get('category', 'verbs')
    
    if request.method == 'POST':
        english = request.form.get('english', '').strip()
        deutsch = request.form.get('deutsch', '').strip()
        sample = request.form.get('sample', '').strip()
        category = request.form.get('category', 'verbs')
        
        # Validation
        if not english or not deutsch:
            return render_template('add_card.html', error='English and German fields are required!', category=category)
        
        flashcards = load_flashcards(category)
        card_id = get_next_id(flashcards)
        
        new_card = {
            'id': card_id,
            'english': english,
            'deutsch': deutsch,
            'sample': sample,
            'audio': f"{category}_{card_id}.mp3",
            'created_at': datetime.now().isoformat()
        }
        
        flashcards.append(new_card)
        save_flashcards(flashcards, category)
        
        # Generate audio in background (will be created when user clicks play)
        # Or we can generate it now
        try:
            generate_audio(deutsch, card_id, category)
        except Exception as e:
            print(f"Warning: Could not pre-generate audio: {e}")
        
        return redirect(url_for('index', category=category))
    
    return render_template('add_card.html', category=category)

@app.route('/edit/<int:card_id>', methods=['GET', 'POST'])
def edit_card(card_id):
    """Edit an existing flashcard"""
    category = request.args.get('category', 'verbs')
    flashcards = load_flashcards(category)
    card = next((c for c in flashcards if c['id'] == card_id), None)
    
    if not card:
        return redirect(url_for('index', category=category))
    
    if request.method == 'POST':
        english = request.form.get('english', '').strip()
        deutsch = request.form.get('deutsch', '').strip()
        sample = request.form.get('sample', '').strip()
        category = request.form.get('category', 'verbs')
        
        # Validation
        if not english or not deutsch:
            return render_template('edit_card.html', card=card, error='English and German fields are required!', category=category)
        
        # If German word changed, delete old audio so new one will be generated
        if deutsch != card['deutsch']:
            delete_audio(card_id, category)
            card['audio'] = f"{category}_{card_id}.mp3"
            # Try to generate new audio
            try:
                generate_audio(deutsch, card_id, category)
            except Exception as e:
                print(f"Warning: Could not generate audio: {e}")
        
        # Update card
        card['english'] = english
        card['deutsch'] = deutsch
        card['sample'] = sample
        
        save_flashcards(flashcards, category)
        return redirect(url_for('index', category=category))
    
    return render_template('edit_card.html', card=card, category=category)

@app.route('/delete/<int:card_id>')
def delete_card(card_id):
    """Delete a flashcard"""
    category = request.args.get('category', 'verbs')
    flashcards = load_flashcards(category)
    
    # Delete audio file if it exists
    delete_audio(card_id, category)
    
    flashcards = [c for c in flashcards if c['id'] != card_id]
    save_flashcards(flashcards, category)
    
    return redirect(url_for('index', category=category))

@app.route('/api/cards')
def get_cards_api():
    """API endpoint to get all flashcards"""
    category = request.args.get('category', 'verbs')
    flashcards = load_flashcards(category)
    return jsonify({'flashcards': flashcards})

if __name__ == '__main__':
    app.run(debug=True, port=5000)