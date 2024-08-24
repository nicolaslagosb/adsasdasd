import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_question(topic: str, level: str) -> str:
    try:
        prompt = f"Genera una pregunta reflexiva sobre {topic} adecuada para un nivel {level} en análisis de datos, machine learning o big data."
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en ciencia de datos. Genera una pregunta reflexiva basada en el tema proporcionado."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        error_message = f"Error al generar la pregunta con OpenAI: {str(e)}"
        print(error_message)
        return error_message
