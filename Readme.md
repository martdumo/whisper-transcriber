# 🎙️ Whisper Transcriber

Un pequeño proyecto en Python para transcribir audios a texto o subtítulos usando [OpenAI Whisper](https://github.com/openai/whisper).  
Compatible con **GPU NVIDIA (CUDA 12.1)** para mayor velocidad.

---

## 🚀 Requisitos

* Python 3.11+
* [Git](https://git-scm.com/)
* Tarjeta gráfica NVIDIA con soporte CUDA (opcional, pero recomendado)

---

## 📦 Instalación

Cloná el repositorio y creá un entorno virtual:

```bash
git clone https://github.com/martdumo/whisper-transcriber.git
cd whisper-transcriber

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

🖼️ Modo 1: Transcripción de archivos

Ejecutá el script principal y elegí los archivos de audio:

python transcribir.py

    Podés elegir uno o varios archivos de audio (mp3, wav, m4a, etc.)

    El resultado se guarda como .srt (subtítulo) en la carpeta que elijas.

🎤 Modo 2: Grabación en vivo (Beta)

Grabá desde el micrófono y obtené la transcripción automáticamente en un Bloc de Notas:

python grabar_y_transcribir.py

    Se abrirá una ventana con el botón Iniciar grabación.

    Grabá tu voz y presioná OK para detener.

    Se transcribirá en castellano (español argentino).

    Se abrirá Bloc de Notas mostrando el texto transcripto.

📋 Dependencias

Todas las dependencias están en requirements.txt.
Podés reinstalarlas en cualquier momento con:

pip install -r requirements.txt --force-reinstall

🛠️ Notas

    Este proyecto usa el modelo large de Whisper por defecto (más preciso, pero más pesado).

    Para usar otro modelo (ej: medium, small, tiny), editá los scripts y cambiá la línea que carga el modelo:

model = whisper.load_model("large")