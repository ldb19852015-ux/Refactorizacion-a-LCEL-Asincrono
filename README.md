# Refactorización a LCEL Asíncrono (LangChain)

Este proyecto migra la arquitectura imperativa basada en los SDKs crudos de OpenAI, Anthropic y Gemini hacia una arquitectura declarativa usando **LCEL (LangChain Expression Language)**.

## 🚀 Características

- **Composición Declarativa**: Definición del pipeline utilizando el operador `|` (`ChatPromptTemplate | Model | StrOutputParser`).
- **Ejecución Asíncrona**: Procesamiento no bloqueante mediante `.ainvoke()`.
- **Salida en Texto Plano**: Limpieza automática de la respuesta del modelo usando `StrOutputParser`.
- **Soporte Multi-proveedor**: Integración con OpenAI (`ChatOpenAI`), Anthropic (`ChatAnthropic`) y Google Gemini (`ChatGoogleGenerativeAI`).

## 📦 Instalación

1. Clona el repositorio e instala las dependencias:
   ```bash
   pip install -r requirements.txt
