import os
import logging
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_word_definition(word: str) -> dict:
    """
    Get word definition, examples, synonyms, and part of speech from OpenAI.
    Returns a dict with keys:
      success (bool), definition (str), examples (list), synonyms (list), part_of_speech (str), error (optional).
    """
    try:
        prompt = f"""
        Provide a dictionary-style entry for the word "{word}".
        Include:
        - Part of speech
        - Definition
        - 2 example sentences
        - 3 synonyms

        Return it strictly as valid JSON with this structure:
        {{
            "part_of_speech": "...",
            "definition": "...",
            "examples": ["...", "..."],
            "synonyms": ["...", "...", "..."]
        }}
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.7,
        )

        # Extract text output
        output_text = response.output[0].content[0].text

        import json
        data = json.loads(output_text)

        return {
            "success": True,
            "definition": data.get("definition", ""),
            "examples": data.get("examples", []),
            "synonyms": data.get("synonyms", []),
            "part_of_speech": data.get("part_of_speech", "")
        }

    except Exception as e:
        logging.error(f"OpenAI API error for word '{word}': {e}")
        return {
            "success": False,
            "error": "Failed to fetch definition from AI service."
        }
