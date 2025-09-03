import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Load your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_genai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or "gpt-3.5-turbo" if you prefer
            messages=[
                {"role": "system", "content": "You are an educational assistant. Help students with learning queries."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"
