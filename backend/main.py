import modal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Importa el servicio OpenAI de la manera correcta
# Ajusta la ruta si backend.openai_service no es la correcta
from backend.openai_service import generate_question

# Crear la instancia de la aplicación FastAPI
app = FastAPI()

class QuestionRequest(BaseModel):
    topic: str
    level: str

@app.get("/ping")
async def ping():
    return "pong"

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API de generación de preguntas con OpenAI"}

@app.post("/generate-question")
async def create_question(request: QuestionRequest):
    try:
        question = generate_question(request.topic, request.level)
        return {"question": question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Configuración de la imagen para Modal
image = (
    modal.Image.debian_slim()
    .pip_install(
        "fastapi",
        "openai==0.27.0",
        "pydantic",
        "python-dotenv",
        "uvicorn",
    )
)

# Crear la aplicación de Modal
modal_app = modal.App(name="fastapi-openai-app", image=image)

# Definimos la función que se ejecutará en Modal
@modal_app.function()
def run_app():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Entrypoint local y remoto
@modal_app.local_entrypoint()
def main():
    print("Running locally...")
    # Ejecutar la aplicación localmente
    uvicorn.run(app, host="127.0.0.1", port=8000)
    print("Deploying to Modal...")
    run_app.remote()  # Desplegar y ejecutar en Modal

if __name__ == "__main__":
    main()
