import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

# === CONFIGURACIÓN ===
MODEL = "large"  # usamos el modelo large por defecto
LANGUAGE = "es"  # forzamos español para mayor precisión
OUTPUT_FORMATS = ["srt", "txt"]  # genera subtítulos y texto plano

def main():
    # Inicializar ventana Tkinter
    root = tk.Tk()
    root.withdraw()  # ocultamos ventana principal

    # Seleccionar archivos de audio
    file_paths = filedialog.askopenfilenames(
        title="Selecciona los audios a transcribir",
        filetypes=[("Archivos de audio", "*.mp3 *.wav *.m4a *.flac"), ("Todos los archivos", "*.*")]
    )

    if not file_paths:
        messagebox.showinfo("Aviso", "No seleccionaste ningún archivo. Saliendo.")
        return

    # Seleccionar carpeta de salida
    output_dir = filedialog.askdirectory(
        title="Selecciona la carpeta donde guardar los resultados"
    )

    if not output_dir:
        messagebox.showinfo("Aviso", "No seleccionaste carpeta de destino. Saliendo.")
        return

    output_dir = Path(output_dir)

    # Procesar cada archivo
    for file_path in file_paths:
        audio = Path(file_path)
        for fmt in OUTPUT_FORMATS:
            print(f"⏳ Transcribiendo {audio.name} a {fmt.upper()}...")
            comando = [
                sys.executable, "-m", "whisper", str(audio),
                "--model", MODEL,
                "--language", LANGUAGE,
                "--task", "transcribe",
                "--output_format", fmt,
                "--output_dir", str(output_dir)
            ]
            subprocess.run(comando, check=True)

    messagebox.showinfo("Listo ✅", f"Transcripción finalizada.\nArchivos guardados en:\n{output_dir}")

if __name__ == "__main__":
    main()
