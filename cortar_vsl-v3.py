#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DEFINITIVO DE EDICIÓN AUTOMÁTICA DE VSL (cortar_vsl-v3.py)
Conserva TODA la autoridad verificada de Adriana Fonseca (2017, casi 10 años,
Bloomberg EE.UU., Rankia México, Universidades, Trading Floor, FTMO),
la Simulación Monte Carlo, el estudio de +40R en 50 trades y los casos de éxito
(tanto para traders con experiencia como para quienes inician desde cero).
"""

import os
import subprocess
import sys

INPUT_VIDEO = "video_original.mp4"
OUTPUT_VIDEO = "vsl_optimizado.mp4"
SPEED_FACTOR = 1.06  # Aceleración sutil del 6% para ritmo dinámico y alta retención

SEGMENTOS_VSL = [
    # 1. Hook Central + Casi 10 años de experiencia + Promesa Trading Floor (47 seg)
    ("00:00:00.000", "00:00:47.600", "01_hook_10_anios_trading_floor"),
    
    # 2. Autoridad Total: 2017, Institucionales, FTMO 2020, Trading Floor 2022, Capital Corporativo 2023, Bloomberg, Rankia y Universidades (64 seg)
    ("00:05:32.439", "00:06:36.800", "02_autoridad_bloomberg_rankia_ftmo"),
    
    # 3. Empatía Rápida: Comienzos duros, fraude y saturación en YouTube (48 seg)
    ("00:06:36.800", "00:07:24.600", "03_empatia_rapida"),
    
    # 4. Error #1: Operar con los números equivocados de gestión de riesgo (62 seg)
    ("00:17:34.440", "00:18:36.960", "04_error1_intro"),
    
    # 5. El "Aha! Moment": Trampa de $100k vs $10k reales en FTMO + Simulación Monte Carlo de 300 trades (279 seg)
    ("00:19:27.640", "00:24:07.460", "05_trampa_ftmo_montecarlo"),
    
    # 6. Error #2: El "Frankenstein" de estrategia vs. operar con estadísticas (76 seg)
    ("00:26:07.400", "00:27:24.160", "06_error2_estadisticas"),
    
    # 7. Prueba Irrefutable: Discord (Win Rate >50%, R:R >2) + Estudio de 20 estudiantes (+40R en 50 trades = $4,000 USD) (175 seg)
    ("00:28:32.549", "00:31:27.759", "07_estudio_40R_20_estudiantes"),
    
    # 8. Error #3 y Mecanismo Único: El Ciclo de las Tendencias (93 seg)
    ("00:32:33.000", "00:33:02.599", "08_error3_intro"),
    ("00:34:22.400", "00:35:25.840", "09_ciclo_tendencias"),
    
    # 9. Ráfaga de Casos de Éxito: Salvador (+$19k/mes trabajando 10h al día), Steve (40R en FTMO 50k) y Abigail (74% WR) (175 seg)
    ("01:08:32.829", "01:09:20.710", "10_caso_salvador_parte1"),
    ("01:10:26.029", "01:11:16.000", "11_caso_salvador_parte2"),
    ("01:11:55.000", "01:13:12.630", "12_casos_steve_abigail"),
    
    # 10. Inclusión para todos los niveles: Funciona tanto si llevas años estancado como si empiezas desde cero (Caso Jenny) (41 seg)
    ("01:27:18.439", "01:28:00.039", "13_sirve_desde_cero_y_avanzados"),
    
    # 11. Transición de Cierre: Los 2 caminos e invitación al programa (75 seg)
    ("00:38:28.000", "00:39:43.000", "14_cierre_dos_caminos")
]

def cortar_y_unir(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"[ERROR] No se encontró el archivo de video: {input_file}")
        print("Asegúrate de colocar el video en la misma carpeta y llamarlo 'video_original.mp4'")
        sys.exit(1)

    os.makedirs("temp_clips", exist_ok=True)
    lista_concat = "temp_clips/concat_list.txt"

    with open(lista_concat, "w", encoding="utf-8") as f_list:
        for idx, (start, end, name) in enumerate(SEGMENTOS_VSL):
            clip_path = f"temp_clips/clip_{idx:02d}_{name}.mp4"
            print(f"-> Extrayendo segmento {idx+1}/{len(SEGMENTOS_VSL)}: {name} ({start} -> {end})...")
            
            v_filter = f"setpts=PTS/{SPEED_FACTOR}"
            a_filter = f"atempo={SPEED_FACTOR}"
            
            cmd = [
                "ffmpeg", "-y",
                "-ss", start,
                "-to", end,
                "-i", input_file,
                "-vf", v_filter,
                "-af", a_filter,
                "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                "-c:a", "aac", "-b:a", "192k",
                clip_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            f_list.write(f"file '{os.path.abspath(clip_path)}'\n")

    print("-> Uniendo todos los bloques en el VSL optimizado...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", lista_concat,
        "-c", "copy",
        "-movflags", "+faststart",
        output_file
    ]
    subprocess.run(cmd_concat, check=True)
    print(f"\n[ÉXITO] VSL definitivo generado en: {output_file}")

if __name__ == "__main__":
    video_in = sys.argv[1] if len(sys.argv) > 1 else INPUT_VIDEO
    cortar_y_unir(video_in, OUTPUT_VIDEO)
