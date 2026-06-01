# Proyecto Miguel - Evaluador de Carga Cognitiva con IA Local

Este proyecto contiene una aplicación de Gradio que evalúa material docente y estima su carga cognitiva utilizando un modelo local desplegado en LM Studio.

## 🧠 Descripción

`ProyectoMiguel` es una herramienta basada en IA para analizar documentos académicos y generar un reporte estructurado de:

- Análisis de complejidad.
- Carga cognitiva estimada.
- Clasificación de nivel.
- Sugerencias pedagógicas.

La aplicación acepta archivos `.pdf`, `.docx`, `.txt` y `.md`, y genera respuestas inteligentes con continuidad de historial.

## 🚀 Funcionalidades clave

- Interfaz de chat con `Gradio`.
- Evaluación de contenido educativo en formato Markdown.
- Procesamiento de archivos PDF, DOCX y texto plano.
- Conexión local a LM Studio a través de la API de OpenAI.
- Mensajes de error claros cuando el modelo no puede procesar el texto.

## 📁 Estructura del proyecto

- `src/app.py`: aplicación principal que define la interfaz y la lógica del chat.

## 🛠️ Requisitos previos

- Python 3.10 o superior.
- LM Studio instalado y con el servidor local activado.
- Modelo cargado y disponible como `local-model` en LM Studio.
- Dependencias Python:
  - `gradio`
  - `openai`
  - `python-dotenv`
  - `pypdf`
  - `python-docx`

## ⚙️ Instalación y ejecución

1. Crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install gradio openai python-dotenv pypdf python-docx
```

3. Iniciar LM Studio y activar el servidor local en:

```text
http://localhost:1234
```

4. Ejecutar la aplicación:

```powershell
python src/app.py
```

## 🔧 Configuración de la conexión

En `src/app.py` se configura la conexión con LM Studio de esta forma:

```python
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)
```

Si prefieres usar variables de entorno, el proyecto carga `dotenv` para extender esta configuración.

## 💡 Uso

- Sube el documento que deseas evaluar.
- Envía el primer mensaje para que el sistema genere un reporte inicial estructurado.
- Continúa la conversación para solicitar aclaraciones, correcciones o recomendaciones pedagógicas.

## 📝 Comportamiento de la aplicación

- En la primera interacción con un archivo, el asistente genera un reporte con formato Markdown.
- En interacciones posteriores, mantiene el contexto y responde de forma conversacional.
- Si el archivo es demasiado largo, el sistema recomienda aumentar `n_ctx` en LM Studio.

## 📌 Notas importantes

- Asegúrate de que LM Studio esté en ejecución antes de abrir la aplicación.
- El archivo solo se procesa en la primera interacción; después, el chat sigue usando el historial.
- La interfaz se abre automáticamente en el navegador con `demo.launch(inbrowser=True)`.

## 🔎 Sobre el enfoque

Este proyecto está orientado a la evaluación didáctica y a la auditoría de cargas cognitivas en materiales de estudio, más que a un asistente genérico de preguntas y respuestas.
