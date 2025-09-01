import logging
from flask import render_template, request, jsonify, flash, redirect, url_for
from .app import app
from .openai_service import get_word_definition


# Home page with form
@app.route('/')
def index():
    return render_template('index.html')


# Handle form submission (POST from HTML form)
@app.route('/search', methods=['POST'])
def search_word():
    """Handle word search requests from form"""
    try:
        word = request.form.get('word', '').strip()

        if not word:
            flash('Please enter a word to search.')
            return redirect(url_for('index'))

        if len(word) > 50 or not word.replace("-", "").isalpha():
            flash('Please enter a valid word.')
            return redirect(url_for('index'))

        # Get word definition (dictionary lookup)
        definition_data = get_word_definition(word)

        # Render the result page
        return render_template('result.html', word=word, result=definition_data)

    except Exception as e:
        logging.error(f"Error during search: {e}")
        flash("An error occurred while processing your request.")
        return redirect(url_for('index'))


# API endpoint for frontend fetch requests (returns JSON)
@app.route('/define', methods=['GET'])
def define_word():
    """Return word definition as JSON for frontend JS"""
    word = request.args.get('word', '').strip()

    if not word:
        return jsonify({"error": "No word provided"}), 400

    try:
        definition_data = get_word_definition(word)
        return jsonify(definition_data)
    except Exception as e:
        logging.error(f"Error in /define: {e}")
        return jsonify({"error": str(e)}), 500
