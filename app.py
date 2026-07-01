from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Path to JSON database
DB_PATH = 'flashcards.json'

def load_flashcards():
    """Load flashcards from JSON file"""
    if not os.path.exists(DB_PATH):
        # Create empty database if it doesn't exist
        save_flashcards([])
        return []
    
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('flashcards', [])
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_flashcards(flashcards):
    """Save flashcards to JSON file"""
    data = {'flashcards': flashcards}
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_next_id(flashcards):
    """Get the next available ID"""
    if not flashcards:
        return 1
    return max(card['id'] for card in flashcards) + 1

@app.route('/')
def index():
    """Main page - display flashcards"""
    flashcards = load_flashcards()
    current_index = request.args.get('index', 0, type=int)
    
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
                         total=total_cards)

@app.route('/add', methods=['GET', 'POST'])
def add_card():
    """Add a new flashcard"""
    if request.method == 'POST':
        english = request.form.get('english', '').strip()
        deutsch = request.form.get('deutsch', '').strip()
        
        # Validation
        if not english or not deutsch:
            return render_template('add_card.html', error='Both fields are required!')
        
        flashcards = load_flashcards()
        new_card = {
            'id': get_next_id(flashcards),
            'english': english,
            'deutsch': deutsch,
            'created_at': datetime.now().isoformat()
        }
        
        flashcards.append(new_card)
        save_flashcards(flashcards)
        
        return redirect(url_for('index'))
    
    return render_template('add_card.html')

@app.route('/edit/<int:card_id>', methods=['GET', 'POST'])
def edit_card(card_id):
    """Edit an existing flashcard"""
    flashcards = load_flashcards()
    card = next((c for c in flashcards if c['id'] == card_id), None)
    
    if not card:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        english = request.form.get('english', '').strip()
        deutsch = request.form.get('deutsch', '').strip()
        
        # Validation
        if not english or not deutsch:
            return render_template('edit_card.html', card=card, error='Both fields are required!')
        
        # Update card
        card['english'] = english
        card['deutsch'] = deutsch
        
        save_flashcards(flashcards)
        return redirect(url_for('index'))
    
    return render_template('edit_card.html', card=card)

@app.route('/delete/<int:card_id>')
def delete_card(card_id):
    """Delete a flashcard"""
    flashcards = load_flashcards()
    flashcards = [c for c in flashcards if c['id'] != card_id]
    save_flashcards(flashcards)
    
    return redirect(url_for('index'))

@app.route('/api/cards')
def get_cards_api():
    """API endpoint to get all flashcards"""
    flashcards = load_flashcards()
    return jsonify({'flashcards': flashcards})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
