import os
import datetime
import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import soundfile as sf
import numpy as np
import whisper
import threading
import queue

# Configuración global
SAMPLE_RATE = None
CHANNELS = 1
AUDIO_FORMAT = 'wav'

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.is_paused = False
        self.audio_chunks = []
        self.stream = None
        self.q = queue.Queue()

    def get_sample_rate(self):
        """Detecta automáticamente el mejor sample rate del micrófono."""
        try:
            device_info = sd.query_devices(kind='input')
            sr = int(device_info['default_samplerate'])
            print(f"[INFO] Sample rate detectado: {sr} Hz")
            return sr
        except Exception as e:
            print(f"[ERROR] No se pudo detectar sample rate. Usando 16000 Hz. Error: {e}")
            return 16000

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"[WARNING] {status}")
        if not self.is_paused:
            self.q.put(indata.copy())

    def start_recording(self):
        global SAMPLE_RATE
        if self.is_recording:
            return
        SAMPLE_RATE = self.get_sample_rate()
        self.is_recording = True
        self.is_paused = False
        self.audio_chunks = []
        self.q = queue.Queue()

        try:
            self.stream = sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                callback=self.audio_callback,
                dtype='float32'
            )
            self.stream.start()
            print("[INFO] Grabación iniciada.")
        except Exception as e:
            print(f"[ERROR] No se pudo iniciar la grabación: {e}")
            self.is_recording = False
            messagebox.showerror("Error", f"No se pudo iniciar la grabación:\n{e}")

    def pause_recording(self):
        if self.is_recording and not self.is_paused:
            self.is_paused = True
            print("[INFO] Grabación pausada.")

    def resume_recording(self):
        if self.is_recording and self.is_paused:
            self.is_paused = False
            print("[INFO] Grabación reanudada.")

    def stop_recording(self):
        if not self.is_recording:
            return None
        self.is_recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        # Vaciar la cola y acumular todos los chunks
        while not self.q.empty():
            self.audio_chunks.append(self.q.get())

        if not self.audio_chunks:
            print("[WARNING] No se grabó audio.")
            return None

        audio_data = np.concatenate(self.audio_chunks, axis=0)
        print(f"[INFO] Grabación detenida. Duración aproximada: {len(audio_data) / SAMPLE_RATE:.2f} segundos.")
        return audio_data, SAMPLE_RATE

    def save_audio(self, audio_data, sample_rate):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"grabacion_{timestamp}.wav"
        try:
            sf.write(filename, audio_data, sample_rate)
            print(f"[INFO] Audio guardado como: {filename}")
            return filename
        except Exception as e:
            print(f"[ERROR] No se pudo guardar el archivo: {e}")
            messagebox.showerror("Error", f"No se pudo guardar el audio:\n{e}")
            return None

# Instancia global del grabador
recorder = AudioRecorder()
current_audio_file = None

def transcribe_audio_async():
    global current_audio_file
    if not current_audio_file or not os.path.exists(current_audio_file):
        messagebox.showwarning("Advertencia", "No hay archivo de audio para transcribir.")
        return

    def run_transcription():
        try:
            print("[INFO] Cargando modelo Whisper (large)...")
            model = whisper.load_model("large")
            print("[INFO] Transcribiendo audio...")
            result = model.transcribe(current_audio_file, language="es")
            txt_file = current_audio_file.replace(".wav", ".txt")
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write(result["text"])
            print(f"[INFO] Transcripción guardada en: {txt_file}")
            messagebox.showinfo("Éxito", f"Transcripción completada y guardada en:\n{txt_file}")
        except Exception as e:
            error_msg = f"[ERROR] Falló la transcripción: {e}"
            print(error_msg)
            messagebox.showerror("Error", f"Falló la transcripción:\n{e}")

    # Ejecutar en hilo separado para no bloquear la GUI
    threading.Thread(target=run_transcription, daemon=True).start()

def on_grabar():
    if recorder.is_recording:
        messagebox.showinfo("Info", "Ya estás grabando.")
        return
    recorder.start_recording()

def on_pausar():
    if not recorder.is_recording:
        messagebox.showinfo("Info", "No hay grabación en curso.")
        return
    if recorder.is_paused:
        messagebox.showinfo("Info", "Ya está pausado.")
        return
    recorder.pause_recording()

def on_reanudar():
    if not recorder.is_recording:
        messagebox.showinfo("Info", "No hay grabación en curso.")
        return
    if not recorder.is_paused:
        messagebox.showinfo("Info", "La grabación ya está activa.")
        return
    recorder.resume_recording()

def on_detener():
    global current_audio_file
    if not recorder.is_recording:
        messagebox.showinfo("Info", "No hay grabación en curso.")
        return
    result = recorder.stop_recording()
    if result is None:
        current_audio_file = None
        return
    audio_data, sr = result
    current_audio_file = recorder.save_audio(audio_data, sr)
    if current_audio_file:
        messagebox.showinfo("Éxito", f"Grabación guardada como:\n{current_audio_file}")

# --- Interfaz gráfica ---
def main():
    root = tk.Tk()
    root.title("Grabador de Voz con Transcripción (Español)")
    root.geometry("400x250")

    tk.Button(root, text="▶️ Grabar", command=on_grabar, width=20, bg="#4CAF50", fg="white").pack(pady=5)
    tk.Button(root, text="⏸️ Pausar", command=on_pausar, width=20, bg="#FFC107", fg="black").pack(pady=5)
    tk.Button(root, text="▶️ Reanudar", command=on_reanudar, width=20, bg="#2196F3", fg="white").pack(pady=5)
    tk.Button(root, text="⏹️ Detener y Guardar", command=on_detener, width=20, bg="#F44336", fg="white").pack(pady=5)
    tk.Button(root, text="📝 Transcribir a Texto", command=transcribe_audio_async, width=20, bg="#9C27B0", fg="white").pack(pady=10)

    print("[INFO] Aplicación iniciada. Listo para grabar.")
    root.mainloop()

if __name__ == "__main__":
    main()