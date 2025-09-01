import logging
from flask import render_template, request, jsonify, flash, redirect, url_for
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
        
        if result['success']:
            return render_template('index.html', 
                                 word=word, 
                                 definition_data=result['data'])
        else:
            flash(f'Error getting definition: {result["error"]}', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        logging.error(f"Error in search_word: {str(e)}")
        flash('An unexpected error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    logging.error(f"Internal server error: {str(e)}")
    flash('An internal server error occurred. Please try again later.', 'error')
    return render_template('index.html'), 500
