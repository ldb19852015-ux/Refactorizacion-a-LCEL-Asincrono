import asyncio
import os
import sys

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()


def obtener_modelo_lcel(provider: str, model_name: str, temperature: float = 0.7):
    """Instancia de forma declarativa el modelo LCEL correspondiente."""
    if provider == "openai":
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    elif provider == "anthropic":
        return ChatAnthropic(
            model=model_name,
            temperature=temperature,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
    else:
        raise ValueError(f"Proveedor no soportado: {provider}")


async def ejecutar_cadena_lcel(
    provider: str, model_name: str, pregunta_input: dict
):
    print("--------------------------------------------------")
    print(f"🟢 PRUEBA LCEL ASÍNCRONA CON {provider.upper()} ({model_name})")
    print("--------------------------------------------------")

    # 1. Configuración del Modelo
    llm = obtener_modelo_lcel(provider, model_name)

    # 2. Definición del Template con roles (System/Human)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Sos un asistente técnico especializado. Respondé de manera concisa.",
            ),
            ("human", "{pregunta}"),
        ]
    )

    # 3. Construcción de la Cadena (Pipeline LCEL con el operador |)
    chain = prompt | llm | StrOutputParser()

    # 4. Ejecución Asíncrona (.ainvoke con await)
    print("Enviando consulta asíncrona...\n")
    respuesta = await chain.ainvoke(pregunta_input)

    # 5. Salida en texto plano extraída por StrOutputParser
    print("--- Respuesta del Modelo ---")
    print(respuesta)
    print("\n")


async def main():
    # Diccionario de entrada requerido por la consigna
    payload = {
        "pregunta": "¿Cuál es la principal ventaja de migrar un flujo imperativo a LangChain Expression Language?"
    }

    # Prueba con los proveedores disponibles en el .env
    if os.getenv("OPENAI_API_KEY"):
        await ejecutar_cadena_lcel("openai", "gpt-4o-mini", payload)
    elif os.getenv("ANTHROPIC_API_KEY"):
        await ejecutar_cadena_lcel("anthropic", "claude-3-5-sonnet-20240620", payload)
    elif os.getenv("GOOGLE_API_KEY"):
        await ejecutar_cadena_lcel("gemini", "gemini-1.5-flash", payload)
    else:
        print("❌ No se encontró ninguna API key en el archivo .env")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())