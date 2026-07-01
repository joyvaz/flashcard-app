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
