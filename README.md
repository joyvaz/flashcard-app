# flashcard-app
# Flashcard App - English to German

A simple, interactive flashcard application built with Python. Learn English words and their German translations with flip animations.

## Features

- 📚 **Category Support**: Learn from Verbs and Nouns (with easy extensibility for more categories)
- 🎯 **Flashcard Management**: Add, edit, and delete flashcards
- 🔄 **Flip Animation**: Click to flip cards between English and German
- 💬 **Sample Sentences**: See German words used in context with example sentences
- 🔊 **German Pronunciation Audio**: Click speaker icon to hear native German pronunciation of each word
- 📊 **Progress Tracking**: Automatically saves your current position for each category - pick up where you left off!
- 📈 **Progress Bar**: Visual indicator showing your position in the deck
- 💾 **JSON Database**: All flashcards stored separately by category in JSON format
- 🎨 **Simple Interface**: Clean and intuitive web-based UI

## Project Structure

└── flashcard-app/
    ├── README.md
    ├── requirements.txt
    ├── app.py
    ├── data/
    │   ├── nouns.json
    │   └── verbs.json
    └── templates/
        ├── base.html
        ├── index.html
        ├── add_card.html
        └── edit_card.html



## Installation

1. Clone the repository:
```bash
git clone https://github.com/joyvaz/flashcard-app.git
cd flashcard-app
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Run the application:
```
python app.py
```
4. Open your browser and visit http://localhost:5000
