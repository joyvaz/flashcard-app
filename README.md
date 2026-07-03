# Flashcard App

A small Flask-based flashcard application for practicing English-to-German vocabulary. The app lets you browse flashcards, flip between English and German, listen to generated German pronunciation audio, and manage your cards and progress.

## Features

- 📚 Supports multiple decks, including verbs and nouns
- 🔄 Flip cards to reveal the translation
- 🎧 Play German audio using gTTS
- ➕ Add, edit, and delete flashcards
- 📈 Save your current position per category so you can resume where you left off
- 💾 Store card data and progress in JSON files
- 🌐 Use a simple web interface with Flask templates

## Categories
- Noun
- Verbs
- prepositions
- Modal Verbs (TBD)
- phrases
- Connectors (TBD)
- Contractions (TBD)
- Trennbare (TBD)
- W-Fragen (TBD)

## Project Structure

```text
flashcard-app/
├── app.py
├── routes.py
├── services.py
├── requirements.txt
├── README.md
├── data/
│   ├── nouns.json
│   └── verbs.json
├── progress/
│   └── progress.json
├── static/
│   └── audio/
└── templates/
    ├── add_card.html
    ├── base.html
    ├── edit_card.html
    └── index.html
```

## Requirements

- Python 3.9+
- Flask
- gTTS

## Installation

1. Clone the repository:

```bash
git clone https://github.com/joyvaz/flashcard-app.git
cd flashcard-app
```

2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Start the app:

```bash
python app.py
```

5. Open your browser at http://127.0.0.1:5000

## Usage

- Open the home page to begin reviewing cards.
- Use the navigation controls to move through the current deck.
- Click the card to flip between English and German.
- Use the speaker icon to play German pronunciation audio.
- Add new cards from the Add Card page.
- Edit or delete cards from the card management options.

## Data and Persistence

- Flashcards are stored in JSON files under the data directory.
- Progress is stored in progress/progress.json and is saved per category.
- Audio files are generated on demand and cached in static/audio.

## API

The app also exposes a simple JSON endpoint for retrieving cards:

```text
GET /api/cards?category=verbs
```

## Notes

- Audio generation depends on gTTS and may require network access the first time a sound is created.
- You can add more categories by extending the data files and matching routes in the app.

## To add a new category of flashcards, follow these steps:

### 1. **Create a new JSON data file**
Add a new file in the `data/` directory (e.g., `data/adjectives.json`):

```json
{
  "flashcards": []
}
```

### 2. **Update `services.py`** to support the new category
Add a constant for your new category file path:

```python
ADJECTIVES_DB = os.path.join(DATA_DIR, 'adjectives.json')
```

Then modify the `load_flashcards()` and `save_flashcards()` functions to handle the new category:

```python
def load_flashcards(category='verbs'):
    """Load flashcards from JSON file based on category."""
    if category == 'verbs':
        db_path = VERBS_DB
    elif category == 'nouns':
        db_path = NOUNS_DB
    elif category == 'adjectives':
        db_path = ADJECTIVES_DB
    # Add more categories as needed
    else:
        db_path = VERBS_DB  # Default fallback
    
    # ... rest of the function
```

Do the same for `save_flashcards()`.

### 3. **Update the category dropdown in `templates/index.html`**
Add a new option to the category selector dropdown (around line 432):

```html
<select id="categorySelect" onchange="changeCategory(this)">
    <option value="verbs" {% if category == 'verbs' %}selected{% endif %}>Verbs</option>
    <option value="nouns" {% if category == 'nouns' %}selected{% endif %}>Nouns</option>
    <option value="adjectives" {% if category == 'adjectives' %}selected{% endif %}>Adjectives</option>
</select>
```
#### Same way update in `templates/add_card.html` and `templates/edit_card.html` files

### 4. **That's it!**
The rest of the app (routes in `routes.py`, add/edit/delete functionality) already uses the `category` parameter generically, so they'll automatically work with your new category.

### Summary of files to modify:
- ✅ Create: `data/adjectives.json`
- ✅ Modify: `services.py` (add ADJECTIVES_DB constant and update category handling)
- ✅ Modify: `templates/index.html` (add dropdown option)

The architecture is already designed to be category-agnostic, so adding new categories is just a matter of following these three simple steps!