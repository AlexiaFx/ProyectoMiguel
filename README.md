# Proyecto Miguel - Asistente Académico con IA Local

Este proyecto implementa un asistente académico conversacional usando Gradio y un modelo de lenguaje ejecutado localmente a través de LM Studio.

## 🧠 Descripción

`ProyectoMiguel` es una aplicación de chat basada en IA para asesoría educativa. Está diseñada para:

- Ofrecer respuestas sobre materias académicas, semestres y herramientas de estudio.
- Mantener conversaciones fluidas con continuidad en el historial.
- Ejecutarse de manera local conectándose a LM Studio como servidor de inferencia.

## 🚀 Funcionalidades clave

- Interfaz de chat con `Gradio`.
- Conexión local a LM Studio mediante `OpenAI` con `base_url` apuntando a `http://localhost:1234/v1`.
- Sistema de prompt flexible para respuestas detalladas y orientadas a la educación.
- Estilo visual personalizado mediante CSS dentro de la aplicación.

## 📁 Estructura del proyecto

- `src/app.ipynb`: notebook principal con la implementación del asistente.

## 🛠️ Requisitos previos

- Python 3.10+.
- LM Studio instalado y funcionando.
- Modelo cargado en LM Studio con servidor local activado.
- Paquetes Python necesarios: `gradio`, `openai`.

## ⚙️ Instalación y ejecución

1. Crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install gradio openai
```

3. Iniciar LM Studio y activar el servidor local en:

```text
http://localhost:1234
```

4. Ejecutar el notebook `src/app.ipynb` desde Jupyter o Visual Studio Code.

## 🧩 Configuración del asistente

El archivo `src/app.ipynb` configura la conexión con el servidor local de LM Studio usando:

```python
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
```

También define el prompt principal para que el asistente ofrezca:

- explicaciones detalladas,
- recomendaciones de materiales y herramientas,
- continuidad en la conversación.

## 💡 Uso

Una vez abierto el notebook y ejecutado, la aplicación Gradio mostrará una interfaz de chat donde puedes escribir preguntas sobre materias, semestres o herramientas educativas.

## 🔧 Notas importantes

- Asegúrate de que LM Studio esté en ejecución al momento de usar el asistente.
- Si el servidor local no está activo, el chat mostrará errores de conexión.
- El modelo configurado en el notebook se identifica como `local-model`, así que debes usar un modelo compatible en LM Studio.

## 📌 Autor

Proyecto adaptado para el entorno de `ProyectoMiguel`.
