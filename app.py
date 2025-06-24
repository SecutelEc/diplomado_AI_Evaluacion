import os
import tempfile
from langchain_openai import ChatOpenAI
from streamlit_mic_recorder import speech_to_text
import streamlit as st
from openai import OpenAI

# Carga la clave desde Streamlit Secrets o variable de entorno
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no está definida. Configura la variable de entorno.")

# Inicializar clientes
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuración de la página
st.set_page_config(page_title="Asistente Virtual Mejorado", page_icon="🤖")
st.title("🤖 Asistente Virtual Mejorado")
st.write("Habla con el asistente usando tu micrófono y parlantes. Elige modelo y voz.")


# Selección de modelo
model_name = st.selectbox("Modelo OpenAI:", ["gpt-4o", "gpt-3.5-turbo"])

# Selección de voz
voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
voice = st.selectbox("Seleccione la voz:", voices)

# Inicializar historial
if "history" not in st.session_state:
    st.session_state["history"] = []

# Botón para limpiar historial
if st.button("Limpiar historial"):
    st.session_state["history"] = []
    st.success("Historial limpiado.")

# Inicializar modelo de chat
llm = ChatOpenAI(model=model_name, openai_api_key=OPENAI_API_KEY)

# Grabación de voz
st.write("Presiona el botón y habla:")
text = speech_to_text(language="es", use_container_width=True, just_once=True, key="stt")

respuesta = None

if text:
    st.session_state["history"].append({"user": text})
    # Enviar texto al modelo
    response = llm.invoke(text)
    respuesta = response.content
    st.session_state["history"].append({"bot": respuesta})

    # Convertir respuesta a voz usando OpenAI TTS
    tts_response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=respuesta
    )
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        for chunk in tts_response.iter_bytes():
            if chunk:
                fp.write(chunk)
        audio_path = fp.name

    # Reproducir el audio con Streamlit
    audio_file = open(audio_path, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

# Mostrar historial de conversación
if st.session_state["history"]:
    st.write("### Historial de conversación")
    for msg in st.session_state["history"]:
        if "user" in msg:
            st.write("🧑 Tú:", msg["user"])
        else:
            st.write("🤖 Asistente:", msg["bot"])