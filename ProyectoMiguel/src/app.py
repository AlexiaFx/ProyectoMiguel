import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# Motores de extracción de texto para documentos binarios
from pypdf import PdfReader
import docx

# Cargar variables de entorno por seguridad
load_dotenv()

# =====================================================================
# 🖥️ CONEXIÓN A LM STUDIO (SERVIDOR LOCAL)
# =====================================================================
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

# =====================================================================
# 📂 PARSER UNIVERSAL DE ARCHIVOS
# =====================================================================
def extraer_texto_de_archivo(file_obj):
    if file_obj is None:
        return ""
    
    nombre_archivo = file_obj.name
    extension = os.path.splitext(nombre_archivo)[1].lower()
    texto_extraido = ""

    try:
        if extension == ".pdf":
            reader = PdfReader(nombre_archivo)
            for page in reader.pages:
                texto_pagina = page.extract_text()
                if texto_pagina:
                    texto_extraido += texto_pagina + "\n"
            return texto_extraido

        elif extension == ".docx":
            doc = docx.Document(nombre_archivo)
            paragraphs = [p.text for p in doc.paragraphs]
            return "\n".join(paragraphs)

        else:
            with open(nombre_archivo, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
    except Exception as e:
        return f"[Error crítico al procesar archivo]: {str(e)}"

# =====================================================================
# 💬 LÓGICA DEL CHAT INTERACTIVO (MEMORIA FLUIDA)
# =====================================================================
def chat_evaluacion(message, history, archivo_adjunto):
    contents = []
    
    instrucciones_sistema = (
        "Eres un sistema experto en psicopedagogía e ingeniería educativa. Tu objetivo central es el "
        "'Sistema de Evaluación de Carga Cognitiva en Materiales Docentes'. Tu tarea obligatoria es: "
        "analizar complejidad, estimar carga cognitiva, clasificar niveles y sugerir mejoras pedagógicas. "
        "Si es la primera interacción, genera el reporte estructurado de 4 puntos. "
        "Si el usuario continúa la conversación, responde de manera fluida y conversacional basándote en el historial."
    )

    contents.append({"role": "system", "content": instrucciones_sistema})

    for turno in history:
        if isinstance(turno, dict):
            user_content = turno.get("text", "") if isinstance(turno.get("text"), str) else turno.get("content", "")
            bot_content = turno.get("label", "") if isinstance(turno.get("label"), str) else ""
        else:
            user_content = turno[0]
            bot_content = turno[1]
            
        if user_content:
            contents.append({"role": "user", "content": user_content})
        if bot_content:
            contents.append({"role": "assistant", "content": bot_content})

    texto_actual = ""
    if archivo_adjunto is not None and len(history) == 0:
        texto_archivo = extraer_texto_de_archivo(archivo_adjunto)
        
        limite_caracteres = 9000
        if len(texto_archivo) > limite_caracteres:
            texto_archivo = texto_archivo[:limite_caracteres] + "\n\n[...Texto truncado por longitud...]"
        texto_actual = f"Por favor evalúa la carga cognitiva del siguiente material docente:\n\n{texto_archivo}"
    else:
        texto_actual = message

    if not texto_actual.strip():
        return "Por favor, escribe un mensaje o sube un archivo para comenzar."

    contents.append({"role": "user", "content": texto_actual})

    try:
        if len(history) == 0:
            contents[-1]["content"] += (
                "\n\nResponde estructurando el reporte exactamente con este formato Markdown:\n"
                "## 📊 1. Análisis de Complejidad:\n[Tu análisis aquí]\n\n"
                "## 🧠 2. Carga Cognitiva Estimada:\n[Tu estimación aquí]\n\n"
                "## 📈 3. Clasificación de Nivel:\n[Tu clasificación aquí]\n\n"
                "## 💡 4. Sugerencias Pedagógicas Automáticas:\n- [Sugerencia 1]\n- [Sugerencia 2]"
            )

        response = client.chat.completions.create(
            model="local-model",
            messages=contents,
            temperature=0.3
        )
        return response.choices[0].message.content

    except Exception as e:
        if "context length" in str(e).lower() or "400" in str(e):
            return "⚠️ Error de Contexto: El documento es demasiado largo para LM Studio. Incrementa el n_ctx a 8192 o superior."
        return f"Error de enlace local: {str(e)}. Asegúrate de que el servidor local esté encendido."

# =====================================================================
# 🎨 INTERFAZ WEB MAXIMIZADA HASTA EL FONDO (Gradio)
# =====================================================================
# Inyectamos CSS para obligar a que el contenedor del chat use una altura expandida
css_personalizado = """
.contenedor-chat { height: 70vh !important; }
"""

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate"), css=css_personalizado) as demo:
    
    # Encabezado Minimalista
    gr.HTML("""
    <div style="text-align: left; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid #1e293b;">
        <h1 style="font-size: 1.6rem; font-weight: 800; color: #3b82f6; margin-bottom: 4px; display: inline-block;">🎓 Sistema de Evaluación de Carga Cognitiva</h1>
        <span style="font-size: 0.8rem; color: #64748b; margin-left: 10px; font-weight: 500;">| Módulo Inteligente de Auditoría Didáctica</span>
    </div>
    """)
    
    with gr.Row():
        
        # Panel Izquierdo Compacto
        with gr.Column(scale=1, variant="panel"):
            gr.Markdown("### 📂 Documento a Evaluar")
            archivo_input = gr.File(
                label="Sube o arrastra lecturas (.pdf, .docx, .txt)", 
                file_types=[".pdf", ".docx", ".txt", ".md"],
                container=True
            )
            gr.HTML("""
            <div style="margin-top: 15px; font-size: 0.75rem; color: #64748b; line-height: 1.4;">
                📌 <b>Nota de uso:</b> Sube el documento una sola vez antes de iniciar. Los siguientes mensajes servirán para debatir el reporte de manera fluida.
            </div>
            """)
            
        # Panel Derecho Maximizado en Ancho y Alto
        with gr.Column(scale=8, variant="elevation", elem_classes=["contenedor-chat"]):
            chat = gr.ChatInterface(
                fn=chat_evaluacion,
                additional_inputs=[archivo_input],
                textbox=gr.Textbox(
                    placeholder="Escribe tus dudas sobre el reporte, solicita modificaciones al texto o continúa el debate aquí...", 
                    scale=8
                )
            )

if __name__ == "__main__":
    print("\n[INFO] Desplegando interfaz optimizada con pantalla completa...")
    demo.launch(inbrowser=True)