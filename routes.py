from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for
import os

from services import (
    build_card_payload,
    delete_audio,
    generate_audio,
    get_next_id,
    get_or_generate_audio,
    get_user_progress,
    load_flashcards,
    save_flashcards,
    set_user_progress,
)

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Main page - display flashcards."""
    category = request.args.get('category', 'verbs')
    flashcards = load_flashcards(category)

    current_index = get_user_progress(category)

    if current_index < 0:
        current_index = 0
    elif current_index >= len(flashcards) and flashcards:
        current_index = len(flashcards) - 1

    current_card = flashcards[current_index] if flashcards else None
    total_cards = len(flashcards)

    return render_template(
        'index.html',
        card=current_card,
        index=current_index,
        total=total_cards,
        category=category,
    )


@bp.route('/set-progress', methods=['POST'])
def set_progress():
    """Set user progress (called via AJAX)."""
    try:
        data = request.json
        category = data.get('category', 'verbs')
        index = data.get('index', 0)

        set_user_progress(category, index)

        return jsonify({'status': 'success'})
    except Exception as exc:
        print(f"Error setting progress: {exc}")
        return jsonify({'status': 'error', 'message': str(exc)}), 500


@bp.route('/audio/<category>/<int:card_id>')
def get_audio(category, card_id):
    """Get or generate audio for a flashcard."""
    try:
        flashcards = load_flashcards(category)
        card = next((c for c in flashcards if c['id'] == card_id), None)

        if not card:
            return 'Card not found', 404

        audio_path = get_or_generate_audio(card['deutsch'], card_id, category)

        if not audio_path or not os.path.exists(audio_path):
            return 'Could not generate audio', 500

        return send_file(audio_path, mimetype='audio/mpeg')
    except Exception as exc:
        print(f"Error serving audio: {exc}")
        return f'Error: {str(exc)}', 500


@bp.route('/add', methods=['GET', 'POST'])
def add_card():
    """Add a new flashcard."""
    category = request.args.get('category', 'verbs')

    if request.method == 'POST':
        english = request.form.get('english', '').strip()
        deutsch = request.form.get('deutsch', '').strip()
        sample = request.form.get('sample', '').strip()
        category = request.form.get('category', 'verbs')

        if not english or not deutsch:
            return render_template('add_card.html', error='English and German fields are required!', category=category)

        flashcards = load_flashcards(category)
        card_id = get_next_id(flashcards)
        new_card = build_card_payload(english, deutsch, sample, category, card_id)

        flashcards.append(new_card)
        save_flashcards(flashcards, category)

        try:
            generate_audio(deutsch, card_id, category)
        except Exception as exc:
            print(f"Warning: Could not pre-generate audio: {exc}")

        return redirect(url_for('main.index', category=category))

    return render_template('add_card.html', category=category)


@bp.route('/edit/<int:card_id>', methods=['GET', 'POST'])
def edit_card(card_id):
    """Edit an existing flashcard."""
    category = request.args.get('category', 'verbs')
    flashcards = load_flashcards(category)
    card = next((c for c in flashcards if c['id'] == card_id), None)

    if not card:
        return redirect(url_for('main.index', category=category))

    if request.method == 'POST':
        english = request.form.get('english', '').strip()
        deutsch = request.form.get('deutsch', '').strip()
        sample = request.form.get('sample', '').strip()
        category = request.form.get('category', 'verbs')

        if not english or not deutsch:
            return render_template('edit_card.html', card=card, error='English and German fields are required!', category=category)

        if deutsch != card['deutsch']:
            delete_audio(card_id, category)
            card['audio'] = f"{category}_{card_id}.mp3"
            try:
                generate_audio(deutsch, card_id, category)
            except Exception as exc:
                print(f"Warning: Could not generate audio: {exc}")

        card['english'] = english
        card['deutsch'] = deutsch
        card['sample'] = sample

        save_flashcards(flashcards, category)
        return redirect(url_for('main.index', category=category))

    return render_template('edit_card.html', card=card, category=category)


@bp.route('/delete/<int:card_id>')
def delete_card(card_id):
    """Delete a flashcard."""
    category = request.args.get('category', 'verbs')
    flashcards = load_flashcards(category)

    delete_audio(card_id, category)

    flashcards = [c for c in flashcards if c['id'] != card_id]
    save_flashcards(flashcards, category)

    return redirect(url_for('main.index', category=category))


@bp.route('/api/cards')
def get_cards_api():
    """API endpoint to get all flashcards."""
    category = request.args.get('category', 'verbs')
    flashcards = load_flashcards(category)
    return jsonify({'flashcards': flashcards})
