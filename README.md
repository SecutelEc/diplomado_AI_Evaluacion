# Asistente Virtual Mejorado 🤖

Este proyecto es un asistente virtual basado en voz, construido con Streamlit y OpenAI. Permite conversar por voz en varios idiomas, elegir el modelo de IA y escuchar las respuestas generadas.

## Características

- Conversación por voz (entrada y salida)
- Soporte para español, inglés y francés
- Selección de modelo OpenAI (gpt-4o, gpt-3.5-turbo)
- Historial de conversación
- Botón para limpiar historial

## Requisitos

- Python 3.8+
- Una clave de API de OpenAI

## Instalación

1. Clona el repositorio o copia los archivos.
2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Configura tu clave de OpenAI como variable de entorno:
   ```
   set OPENAI_API_KEY=tu_clave_aqui   # En Windows
   export OPENAI_API_KEY=tu_clave_aqui # En Linux/Mac
   ```

## Uso

Ejecuta la aplicación con:
```
streamlit run app.py
```

Habla con el asistente y disfruta de la experiencia conversacional.

---

**Autor:** Julio Bernal  
**Versión:** 1.0