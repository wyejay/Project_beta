import json
import os
import logging
from openai import OpenAI

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def get_word_definition(word):
    """
    Get comprehensive word information from OpenAI including definition, 
    part of speech, examples, and contextual sentences.
    
    Args:
        word (str): The word to define
        
    Returns:
        dict: Contains success status and either data or error message
    """
    try:
        if not OPENAI_API_KEY:
            return {
                'success': False,
                'error': 'OpenAI API key is not configured. Please set the OPENAI_API_KEY environment variable.'
            }
        
        # Create a comprehensive prompt for word analysis
        prompt = f"""
        Analyze the word "{word}" and provide comprehensive information in JSON format.
        
        Please provide:
        1. definition: A clear, concise definition of the word
        2. part_of_speech: The grammatical category (noun, verb, adjective, etc.)
        3. examples: An array of 3-4 short example phrases or sentences showing different uses
        4. contextual_sentences: An array of 2-3 complete, meaningful sentences using the word in context
        5. pronunciation: Phonetic pronunciation guide if helpful
        6. etymology: Brief origin or word history if interesting
        
        Format your response as a JSON object with these exact keys:
        {{
            "definition": "string",
            "part_of_speech": "string", 
            "examples": ["string1", "string2", "string3"],
            "contextual_sentences": ["sentence1", "sentence2", "sentence3"],
            "pronunciation": "string",
            "etymology": "string"
        }}
        
        If the word has multiple meanings, focus on the most common definition.
        If it's not a real word, indicate that in the definition field.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-5",  # newest OpenAI model released August 7, 2025
            messages=[
                {
                    "role": "system",
                    "content": "You are a comprehensive dictionary and linguistics expert. "
                    "Provide accurate, educational word information in the requested JSON format."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=800,
            temperature=0.3  # Lower temperature for more consistent, factual responses
        )
        
        # Parse the JSON response
        response_content = response.choices[0].message.content
        word_data = json.loads(response_content)
        
        # Validate that we have the required fields
        required_fields = ['definition', 'part_of_speech', 'examples', 'contextual_sentences']
        for field in required_fields:
            if field not in word_data:
                word_data[field] = "Information not available"
        
        # Ensure examples and sentences are lists
        if not isinstance(word_data.get('examples'), list):
            word_data['examples'] = [word_data.get('examples', 'No examples available')]
        
        if not isinstance(word_data.get('contextual_sentences'), list):
            word_data['contextual_sentences'] = [word_data.get('contextual_sentences', 'No sentences available')]
        
        logging.info(f"Successfully retrieved definition for word: {word}")
        
        return {
            'success': True,
            'data': word_data
        }
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error for word '{word}': {str(e)}")
        return {
            'success': False,
            'error': 'Failed to parse the response from the AI service. Please try again.'
        }
        
    except Exception as e:
        logging.error(f"OpenAI API error for word '{word}': {str(e)}")
        
        # Provide more specific error messages based on the exception
        if "API key" in str(e).lower():
            error_msg = "Invalid or missing API key. Please check your OpenAI API configuration."
        elif "rate limit" in str(e).lower():
            error_msg = "Rate limit exceeded. Please wait a moment and try again."
        elif "quota" in str(e).lower():
            error_msg = "API quota exceeded. Please try again later."
        else:
            error_msg = f"Failed to get word definition. Please try again. ({str(e)[:100]})"
        
        return {
            'success': False,
            'error': error_msg
        }
