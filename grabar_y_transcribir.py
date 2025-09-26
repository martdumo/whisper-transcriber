import sounddevice as sd
import numpy as np
import whisper
import tempfile
import os
import tkinter as tk
from tkinter import messagebox
from scipy.io.wavfile import write
import subprocess

# Configuración
SAMPLE_RATE = 16000
DURATION = []  # se define dinámicamente

def grabar_audio():
    global grabando, audio_data
    grabando = True
    audio_data = []

    def callback(indata, frames, time, status):
        if grabando:
            audio_data.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback):
        root.wait_variable(grabando_var)

    # Combinar datos grabados
    audio_np = np.concatenate(audio_data, axis=0)
    return audio_np

def iniciar_grabacion():
    messagebox.showinfo("Grabación", "Grabando... presiona OK para detener.")
    grabando_var.set(False)  # detener grabación

def main():
    global grabando_var, root

    root = tk.Tk()
    root.title("Grabador de audio")
    grabando_var = tk.BooleanVar(value=True)

    boton = tk.Button(root, text="Iniciar grabación", command=iniciar_grabacion, font=("Arial", 14), width=20)
    boton.pack(pady=20)

    # Captura de audio
    audio_np = grabar_audio()

    # Guardar en archivo temporal
    temp_wav = os.path.join(tempfile.gettempdir(), "grabacion.wav")
    write(temp_wav, SAMPLE_RATE, (audio_np * 32767).astype(np.int16))

    root.destroy()

    # Transcribir con Whisper
    model = whisper.load_model("large")
    result = model.transcribe(temp_wav, language="es")

    temp_txt = os.path.join(tempfile.gettempdir(), "transcripcion.txt")
    with open(temp_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Abrir Bloc de notas
    subprocess.Popen(["notepad.exe", temp_txt])

if __name__ == "__main__":
    main()
