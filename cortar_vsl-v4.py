#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DEFINITIVO ULTRA-COMPACTO DE VSL (cortar_vsl-v4.py)
Duración final exacta: 12 minutos y 40 segundos (a 1.08x).
Conserva el 100% de la autoridad de Adriana Fonseca (2017, casi 10 años,
Bloomberg EE.UU., Rankia México, Universidades, Trading Floor, FTMO),
pero elimina las pausas y repeticiones internas dentro del Error #1 y Error #2
para maximizar la retención hasta el llamado a la acción.
"""

import os
import subprocess
import sys

INPUT_VIDEO = "video_original.mp4"
OUTPUT_VIDEO = "vsl_optimizado.mp4"
SPEED_FACTOR = 1.08  # Ritmo ágil de VSL de alta conversión (reduce de 13m41s a 12m40s)

SEGMENTOS_VSL = [
    # 1. Hook Central + Casi 10 años de experiencia + Trading Floor (47.6s)
    ("00:00:00.000", "00:00:47.600", "01_hook_10_anios_trading_floor"),
    
    # 2. Autoridad Total: 2017, Institucionales, FTMO 2020, Trading Floor 2022, Capital Corporativo 2023, Bloomberg, Rankia y Universidades (55.7s)
    ("00:05:38.439", "00:06:34.100", "02_autoridad_bloomberg_rankia_ftmo"),
    
    # 3. Empatía Rápida: Comienzos duros, fraude y saturación en YouTube (32.4s)
    ("00:06:44.079", "00:07:16.480", "03_empatia_rapida"),
    
    # 4. Error #1 Intro directa (37.6s)
    ("00:17:34.440", "00:18:12.000", "04_error1_intro"),
    
    # 5. El "Aha! Moment" sin relleno: Andrés $100k FTMO -> $10k reales + Simulación Monte Carlo 300 trades (223.1s)
    ("00:19:46.279", "00:20:28.819", "05a_andres_100k_ftmo"),
    ("00:20:56.220", "00:23:56.859", "05b_trampa_10porciento_montecarlo"),
    
    # 6. Error #2 al grano: Frankenstein de estrategia vs. operar con números (53.2s)
    ("00:26:07.400", "00:26:44.160", "06a_error2_frankenstein"),
    ("00:27:03.720", "00:27:20.119", "06b_apostar_vs_profesional"),
    
    # 7. Prueba Irrefutable: Discord (Win Rate >50%, R:R >2) + Estudio de 20 estudiantes (+40R en 50 trades = $4,000 USD) (119.5s)
    ("00:28:44.549", "00:29:42.950", "07a_discord_winrate_rr"),
    ("00:30:20.769", "00:31:21.920", "07b_estudio_20_estudiantes_40R"),
    
    # 8. Error #3 y Mecanismo Único: El Ciclo de las Tendencias (59.5s)
    ("00:32:33.000", "00:32:52.119", "08a_error3_ciclos"),
    ("00:34:22.400", "00:35:02.800", "08b_brujula_tendencias"),
    
    # 9. Casos de Éxito Rápidos: Salvador (+$19k/mes trabajando 10h), Steve (40R FTMO 50k), Abigail (74% WR) (103.0s)
    ("01:09:06.789", "01:09:24.789", "09a_salvador_contexto"),
    ("01:10:35.390", "01:11:02.829", "09b_salvador_19k_mes"),
    ("01:11:59.350", "01:12:56.949", "09c_steve_abigail"),
    
    # 10. Inclusión (Sirve desde cero como Jenny y avanzados) + Cierre Los 2 Caminos (90.1s)
    ("01:27:18.439", "01:27:55.720", "10_sirve_desde_cero"),
    ("00:38:31.269", "00:39:24.110", "11_cierre_dos_caminos")
]

def cortar_y_unir(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"[ERROR] No se encontró el archivo de video: {input_file}")
        sys.exit(1)

    os.makedirs("temp_clips", exist_ok=True)
    lista_concat = "temp_clips/concat_list.txt"

    with open(lista_concat, "w", encoding="utf-8") as f_list:
        for idx, (start, end, name) in enumerate(SEGMENTOS_VSL):
            clip_path = f"temp_clips/clip_{idx:02d}_{name}.mp4"
            print(f"-> Extrayendo {idx+1}/{len(SEGMENTOS_VSL)}: {name} ({start} -> {end})...")
            
            v_filter = f"setpts=PTS/{SPEED_FACTOR}"
            a_filter = f"atempo={SPEED_FACTOR}"
            
            cmd = [
                "ffmpeg", "-y", "-ss", start, "-to", end, "-i", input_file,
                "-vf", v_filter, "-af", a_filter,
                "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                "-c:a", "aac", "-b:a", "192k", clip_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            f_list.write(f"file '{os.path.abspath(clip_path)}'\n")

    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", lista_concat, "-c", "copy", "-movflags", "+faststart", output_file
    ]
    subprocess.run(cmd_concat, check=True)
    print(f"\n[ÉXITO] VSL de 12m 40s generado en: {output_file}")

if __name__ == "__main__":
    video_in = sys.argv[1] if len(sys.argv) > 1 else INPUT_VIDEO
    cortar_y_unir(video_in, OUTPUT_VIDEO)
