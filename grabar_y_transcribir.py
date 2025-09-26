import sounddevice as sd
import numpy as np
import whisper
import tempfile
import os
import tkinter as tk
from tkinter import messagebox
from scipy.io.wavfile import write
import subprocess
import logging
import time

# =========================
# Configuración logging
# =========================
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# Configuración de audio
# =========================
SAMPLE_RATE = 16000
CHANNELS = 1

# =========================
# Función para mostrar nivel en dB
# =========================
def db_level(audio_chunk):
    rms = np.sqrt(np.mean(np.square(audio_chunk)))
    db = 20 * np.log10(rms + 1e-6)  # añadir epsilon para evitar log(0)
    return db

# =========================
# Función para normalizar volumen
# =========================
def normalize_audio(audio):
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak  # normaliza a [-1, 1]
    return audio

# =========================
# Función para grabar audio
# =========================
def grabar_audio():
    try:
        print("⏳ Iniciando grabación...")
        audio_data = []

        def callback(indata, frames, time_info, status):
            audio_data.append(indata.copy())
            nivel_db = db_level(indata)
            print(f"\rNivel: {nivel_db:.1f} dB", end="")

        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback):
            messagebox.showinfo("Grabación", "Grabando... presiona OK para detener.")
        
        print("\n✅ Grabación finalizada.")
        audio_np = np.concatenate(audio_data, axis=0)
        audio_np = normalize_audio(audio_np)
        return audio_np
    except Exception as e:
        logging.error("Error durante la grabación", exc_info=True)
        raise e

# =========================
# Función principal
# =========================
def main():
    try:
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal de tkinter

        print("🎙️ Grabador y transcriptor de audio iniciado")

        # Grabar audio
        audio_np = grabar_audio()

        # Guardar audio en archivo temporal
        temp_wav = os.path.join(tempfile.gettempdir(), "grabacion.wav")
        write(temp_wav, SAMPLE_RATE, (audio_np * 32767).astype(np.int16))
        print(f"💾 Audio guardado en: {temp_wav}")

        # Cargar modelo Whisper
        print("⏳ Cargando modelo Whisper (large)...")
        model = whisper.load_model("large")
        print("✅ Modelo cargado")

        # Transcribir
        print("⏳ Iniciando transcripción...")
        result = model.transcribe(temp_wav, language="es", task="transcribe", verbose=True)
        print("✅ Transcripción completada")

        # Guardar transcripción en archivo temporal
        temp_txt = os.path.join(tempfile.gettempdir(), "transcripcion.txt")
        with open(temp_txt, "w", encoding="utf-8") as f:
            f.write(result["text"])
        print(f"💾 Transcripción guardada en: {temp_txt}")

        # Abrir Bloc de notas
        subprocess.Popen(["notepad.exe", temp_txt])
        print("📝 Bloc de notas abierto con la transcripción")

    except Exception as e:
        logging.error("Error en main", exc_info=True)
        print("❌ Ha ocurrido un error, revisá error.log para más detalles")

if __name__ == "__main__":
    main()
