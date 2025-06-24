import os
import tempfile
from langchain_openai import ChatOpenAI
from streamlit_mic_recorder import speech_to_text
import streamlit as st

from gtts import gTTS

# Carga la clave desde Streamlit Secrets o variable de entorno
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no está definida. Configura la variable de entorno.")


llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=OPENAI_API_KEY
)


# Configuración de la página
st.set_page_config(page_title="Asistente Virtual Mejorado", page_icon="🤖")

st.title("🤖 Asistente Virtual Mejorado")
st.write("Habla con el asistente usando tu micrófono. Elige idioma y modelo.")

# Selección de idioma
idioma = st.selectbox("Idioma de entrada/salida:", [("Español", "es"), ("Inglés", "en"), ("Francés", "fr")], format_func=lambda x: x[0])
lang_code = idioma[1]

# Selección de modelo
model_name = st.selectbox("Modelo OpenAI:", ["gpt-4o", "gpt-3.5-turbo"])

# Inicializar historial
if "history" not in st.session_state:
    st.session_state["history"] = []

# Botón para limpiar historial
if st.button("Limpiar historial"):
    st.session_state["history"] = []
    st.success("Historial limpiado.")

# Inicializar modelo
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model=model_name, openai_api_key=OPENAI_API_KEY)

# Grabación de voz
st.write("Presiona el botón y habla:")
text = speech_to_text(language=lang_code, use_container_width=True, just_once=True, key="stt")

if text:
    st.session_state["history"].append({"user": text})
    # Enviar texto al modelo
    response = llm.invoke(text)
    respuesta = response.content
    st.session_state["history"].append({"bot": respuesta})

    # Convertir respuesta a voz
    tts = gTTS(text=respuesta, lang=lang_code)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        audio_path = fp.name

    st.audio(audio_path, format="audio/mp3")

# Mostrar historial de conversación
if st.session_state["history"]:
    st.write("### Historial de conversación")
    for msg in st.session_state["history"]:
        if "user" in msg:
            st.write("🧑 Tú:", msg["user"])
        else:
            st.write("🤖 Asistente:", msg["bot"])