# Whisper Transcriber (Spanish)

Script en Python para transcribir audios a texto y subtítulos (`.srt` y `.txt`)
usando [OpenAI Whisper](https://github.com/openai/whisper) y aceleración por GPU (CUDA).

## 🚀 Características
- Permite seleccionar **uno o varios audios** en una ventana gráfica.
- Genera automáticamente:
  - Subtítulos en formato `.srt`.
  - Texto plano en `.txt`.
- Usa el modelo **large** para máxima precisión en español.
- Compatible con CUDA (usa GPU si está disponible).

## 🖥️ Requisitos
- Python 3.11+
- CUDA 12+ (opcional, recomendado si tenés GPU NVIDIA)

## 📦 Instalación
Clonar el repositorio y crear entorno virtual:

```bash
git clone https://github.com/TU_USUARIO/whisper_transcriber.git
cd whisper_transcriber
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

▶️ Uso

Ejecutar el script:

venv\Scripts\python.exe transcribir.py

Se abrirán ventanas para:

    Seleccionar uno o varios archivos de audio.

    Seleccionar carpeta de salida.

Los resultados se guardarán en la carpeta elegida.
🎯 Modelos soportados

Por defecto se usa el modelo large.
Si querés cambiarlo, edita la línea MODEL = "large" en transcribir.py.
📄 Licencia

Este proyecto es de uso personal/educativo.
Whisper es de OpenAI bajo licencia MIT.