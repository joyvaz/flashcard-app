import json
import os
from datetime import datetime

from gtts import gTTS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
NOUNS_DB = os.path.join(DATA_DIR, 'nouns.json')
VERBS_DB = os.path.join(DATA_DIR, 'verbs.json')
PREPOSITIONS_DB = os.path.join(DATA_DIR, 'prepositions.json')
PHRASES_DB = os.path.join(DATA_DIR, 'phrases.json')
CONNECTOR_DB = os.path.join(DATA_DIR, 'connector.json')
MODALVERBS_DB = os.path.join(DATA_DIR, 'modalverbs.json')
WFRAGEN_DB = os.path.join(DATA_DIR, 'wfragen.json')
AUDIO_DIR = os.path.join(BASE_DIR, 'static', 'audio')
PROGRESS_DIR = os.path.join(BASE_DIR, 'progress')
PROGRESS_FILE = os.path.join(PROGRESS_DIR, 'progress.json')


def load_flashcards(category='verbs'):
    """Load flashcards from JSON file based on category."""
    db_path = VERBS_DB if category == 'verbs' else NOUNS_DB if category == 'nouns' else PREPOSITIONS_DB if category == 'prepositions' else PHRASES_DB if category == 'phrases' else CONNECTOR_DB if category == 'connector' else MODALVERBS_DB if category == 'modalverbs' else WFRAGEN_DB

    if not os.path.exists(db_path):
        save_flashcards([], category)
        return []

    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('flashcards', [])
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_flashcards(flashcards, category='verbs'):
    """Save flashcards to JSON file based on category."""
    db_path = VERBS_DB if category == 'verbs' else NOUNS_DB if category == 'nouns' else PREPOSITIONS_DB if category == 'prepositions' else PHRASES_DB if category == 'phrases' else CONNECTOR_DB if category == 'connector' else MODALVERBS_DB if category == 'modalverbs' else WFRAGEN_DB

    os.makedirs(DATA_DIR, exist_ok=True)

    data = {'flashcards': flashcards}
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_next_id(flashcards):
    """Get the next available ID."""
    if not flashcards:
        return 1
    return max(card['id'] for card in flashcards) + 1


def load_progress():
    """Load user progress from JSON file."""
    if not os.path.exists(PROGRESS_FILE):
        return {}

    try:
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_progress(progress):
    """Save user progress to JSON file."""
    os.makedirs(PROGRESS_DIR, exist_ok=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)


def get_user_progress(category):
    """Get the current card index for a category."""
    progress = load_progress()
    return progress.get(category, 0)


def set_user_progress(category, index):
    """Save the current card index for a category."""
    progress = load_progress()
    progress[category] = index
    save_progress(progress)


def generate_audio(text, card_id, category):
    """Generate German audio for a flashcard and save it."""
    try:
        os.makedirs(AUDIO_DIR, exist_ok=True)

        audio_filename = f"{category}_{card_id}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)

        tts = gTTS(text=text, lang='de', slow=False)
        tts.save(audio_path)

        return audio_filename
    except Exception as exc:
        print(f"Error generating audio: {exc}")
        return None


def get_or_generate_audio(text, card_id, category):
    """Get audio file or generate it if it doesn't exist."""
    try:
        os.makedirs(AUDIO_DIR, exist_ok=True)

        audio_filename = f"{category}_{card_id}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)

        if not os.path.exists(audio_path):
            tts = gTTS(text=text, lang='de', slow=False)
            tts.save(audio_path)

        return audio_path
    except Exception as exc:
        print(f"Error generating audio: {exc}")
        return None


def delete_audio(card_id, category):
    """Delete audio file for a flashcard."""
    try:
        audio_filename = f"{category}_{card_id}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)

        if os.path.exists(audio_path):
            os.remove(audio_path)
    except Exception as exc:
        print(f"Error deleting audio: {exc}")


def build_card_payload(english, deutsch, sample, category, card_id):
    """Create a new flashcard payload."""
    return {
        'id': card_id,
        'english': english,
        'deutsch': deutsch,
        'sample': sample,
        'audio': f"{category}_{card_id}.mp3",
        'created_at': datetime.now().isoformat()
    }
