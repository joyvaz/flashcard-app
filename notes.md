I'll help you understand how to add a new category of flashcard. Let me first explore the repository structure to understand how the app is organized.Now let me gather evidence about the repository structure and how to add new flashcard categories.Now I have a complete understanding of the flashcard app. Let me provide a comprehensive answer.

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
same way update in 'add_card.html' and edit_card.html files

### 4. **That's it!**
The rest of the app (routes in `routes.py`, add/edit/delete functionality) already uses the `category` parameter generically, so they'll automatically work with your new category.

### Summary of files to modify:
- ✅ Create: `data/adjectives.json`
- ✅ Modify: `services.py` (add ADJECTIVES_DB constant and update category handling)
- ✅ Modify: `templates/index.html` (add dropdown option)

The architecture is already designed to be category-agnostic, so adding new categories is just a matter of following these three simple steps!