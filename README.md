# flashcard-app
# Flashcard App - English to German

A simple, interactive flashcard application built with Python. Learn English words and their German translations with flip animations.

## Features

- 📚 **Flashcard Management**: Add, edit, and delete flashcards
- 🔄 **Flip Animation**: Click to flip cards between English and German
- 💾 **JSON Database**: All flashcards stored locally in JSON format
- 🎯 **Simple Interface**: Clean and intuitive web-based UI

## Project Structure
flashcard-app/ ├── README.md ├── requirements.txt ├── app.py # Main Flask application ├── flashcards.json # Database with flashcards └── templates/ ├── base.html # Base template with styling ├── index.html # Main flashcard view ├── add_card.html # Add new flashcard form └── edit_card.html # Edit flashcard form


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
