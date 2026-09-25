# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

- On this machine run Python with `py` (e.g. `py -m manim ...`), not `python`.
- Pipeline: `guion/guion.txt` → `py herramientas/generar_audio.py [N ...]` → `audio/escenaNN/{completo.mp3,timings.json}` → `py -m manim -ql escenas/escenaNN.py EscenaNN`.
- Scenes subclass `EscenaNarrada` (`escenas/comun.py`), set `numero`, and time animations with `iniciar_bloque(i)` / `esperar_hasta(t)` against the block timings, so re-generating audio re-syncs the video.
- Manim needs system tools outside `requirements.txt`: FFmpeg for video output, and a LaTeX distribution (e.g. MiKTeX) if scenes use `Tex`/`MathTex`.
- `audio/` and `media/` are generated output — keep them git-ignored, never commit them.
