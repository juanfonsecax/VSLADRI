import os
import sys
import subprocess
import wave
import numpy as np
from faster_whisper import WhisperModel

VIDEO_FILE = "MINI 2 final.mp4"
AUDIO_FILE = "audio_temp.wav"
OUTPUT_TXT = "transcripcion_completa.txt"
OUTPUT_SRT = "transcripcion.srt"

def format_timestamp_srt(seconds: float) -> str:
    millis = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def extract_audio(video_path: str, audio_path: str):
    print(f"Extrayendo pista de audio de '{video_path}'...")
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-ac", "1", "-ar", "16000",
        "-c:a", "pcm_s16le", audio_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Extracción de audio completada.")

def load_audio_numpy(audio_path: str) -> np.ndarray:
    print("Cargando buffer de audio en memoria...")
    with wave.open(audio_path, "rb") as wf:
        n_frames = wf.getnframes()
        data = wf.readframes(n_frames)
        return np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

def main():
    if not os.path.exists(VIDEO_FILE):
        print(f"Error: no se encontró el archivo {VIDEO_FILE}")
        sys.exit(1)

    if not os.path.exists(AUDIO_FILE):
        extract_audio(VIDEO_FILE, AUDIO_FILE)

    audio = load_audio_numpy(AUDIO_FILE)
    total_duration = len(audio) / 16000.0
    print(f"Duración total del audio: {total_duration / 60:.2f} minutos.")

    print("Cargando modelo Faster-Whisper (small, int8)...")
    model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=10)

    print("Iniciando transcripción completa...")
    segments, info = model.transcribe(
        audio,
        language="es",
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500)
    )

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f_txt, open(OUTPUT_SRT, "w", encoding="utf-8") as f_srt:
        srt_index = 1
        for segment in segments:
            text = segment.text.strip()
            if not text:
                continue

            # Escribir en texto plano
            f_txt.write(text + "\n")
            f_txt.flush()

            # Escribir en formato SRT
            start_srt = format_timestamp_srt(segment.start)
            end_srt = format_timestamp_srt(segment.end)
            f_srt.write(f"{srt_index}\n{start_srt} --> {end_srt}\n{text}\n\n")
            f_srt.flush()

            progress = (segment.end / total_duration) * 100
            print(f"[{progress:5.1f}%] [{start_srt} -> {end_srt}] {text}")
            srt_index += 1

    print("\n¡Transcripción finalizada con éxito!")
    print(f"Archivos generados:\n- {OUTPUT_TXT}\n- {OUTPUT_SRT}")

    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)
        print("Archivo temporal de audio eliminado.")

if __name__ == "__main__":
    main()
