import logging
from flask import render_template, request, flash, redirect, url_for
from .app import app
from .openai_service import get_word_definition


@app.route('/')
def index():
    """Main page with search form"""
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_word():
    """Handle word search requests"""
    try:
        word = request.form.get('word', '').strip()
        
        if not word:
            flash('Please enter a word to search for.', 'warning')
            return redirect(url_for('index'))
        
        # Validate word (basic check for reasonable input)
        if len(word) > 50 or not word.replace('-', '').replace("'", "").isalpha():
            flash('Please enter a valid word (letters, hyphens, and apostrophes only).', 'error')
            return redirect(url_for('index'))
        
        # Get word definition from OpenAI
        result = get_word_definition(word)
        
        if result.get('success'):
            return render_template(
                'result.html',
                word=word,
                definition=result.get('definition', "No definition found."),
                examples=result.get('examples', []),
                synonyms=result.get('synonyms', []),
                part_of_speech=result.get('part_of_speech', None)
            )
        else:
            flash(result.get('error', 'Could not fetch definition. Please try again.'), 'error')
            return redirect(url_for('index'))
    
    except Exception as e:
        logging.error(f"Error in search_word route: {str(e)}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect(url_for('index'))
