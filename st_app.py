import streamlit as st
import requests
import subprocess
import time

st.title("Generador de Preguntas Reflexivas con OpenAI")

API_URL = "https://modal.com/apps/matiasmercandino/main/deployed/fastapi-openai-app.modal.run/generate-question"


# Función para verificar si la API está activa
def check_api():
    try:
        response = requests.get(f"{API_URL}/ping")
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        return False
    return False

# Función para reactivar la API usando Modal
def start_api():
    st.write("Intentando iniciar la API...")
    try:
        subprocess.run(["modal", "run", "--detach", "backend/main.py::run_app"], check=True)
        time.sleep(5)  # Esperar un momento para que la API se inicie
        if check_api():
            st.success("API iniciada exitosamente.")
        else:
            st.error("No se pudo iniciar la API.")
    except subprocess.CalledProcessError as e:
        st.error(f"Error al intentar iniciar la API: {e}")

# Campos de entrada
topic = st.text_input("Tema (e.g., Redes Neuronales, Big Data):")
level = st.selectbox("Nivel", ["principiante", "intermedio", "avanzado"])

# Botón para generar la pregunta
if st.button("Generar Pregunta"):
    if topic:
        if not check_api():
            start_api()
        if check_api():
            try:
                response = requests.post(
                    f"{API_URL}/generate-question/",
                    json={"topic": topic, "level": level}
                )
                if response.status_code == 200:
                    question = response.json().get("question")
                    st.success(f"Pregunta Generada: {question}")
                else:
                    st.error(f"Error al generar la pregunta: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error en la conexión: {e}")
        else:
            st.error("No se pudo conectar con la API.")
    else:
        st.warning("Por favor, introduce un tema.")

# Opción para probar la conexión con la API
if st.button("Probar Conexión"):
    if not check_api():
        start_api()
    if check_api():
        st.success("¡Conexión exitosa con la API!")
    else:
        st.error("No se pudo conectar con la API.")
