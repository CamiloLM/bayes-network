# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Narrated explainer video (in Spanish) on probabilistic reasoning / Bayesian networks, AIMA chapter 13. Code, comments, script and commit messages are in Spanish.

## Commands

On this machine run Python with `py`, not `python`. Run everything from the repo root (scenes import `escenas.comun`).

```
py herramientas/generar_audio.py            # TTS for every scene in guion/guion.txt
py herramientas/generar_audio.py 3 5        # only scenes 3 and 5
py -m manim -ql escenas/escena01.py Escena01   # 480p draft; -qh for 1080p
py poc/probar_voces.py [PERSONAJE ...]      # voice comparison samples -> poc/muestras/
```

edge-tts needs internet. There are no tests; verify a render with `ffprobe` (the MP4 has an AAC track, but VS Code's video preview plays it silent — use an external player).

## Pipeline

`guion/guion.txt` → `herramientas/generar_audio.py` → `audio/escenaNN/{bloques/, completo.mp3, timings.json}` → `escenas/escenaNN.py` (class `EscenaNN`).

- Script format: the file is split into scenes at lines starting with `ESCENA N`. A block runs from one `[VOZ: X]` to the next and contains `[TEXTO_TTS]...[/TEXTO_TTS]` plus an optional `[PAUSA_DESPUÉS: s]`. `[VISUAL: ...]` (the brief for the animation), `[INICIO]` and `[FIN]` are not spoken.
- Voice names map to edge-tts voice ids in `VOCES` at the top of `generar_audio.py`; the whole script is validated before any synthesis.
- Scenes subclass `EscenaNarrada` (`escenas/comun.py`), set `numero`, and time animations with `iniciar_bloque(i)` / `esperar_hasta(t)` against `timings.json`, so regenerating audio re-syncs the video. The scene's full audio is attached in `setup()`.
- `poc/` holds throwaway experiments, not part of the pipeline.

## Environment

- FFmpeg and MiKTeX (per-user, `%LOCALAPPDATA%\Programs\MiKTeX`, auto-install of missing packages enabled) are installed, so `Tex`/`MathTex` work, including Spanish accents. Update MiKTeX with `miktex packages update`.
- `audio/`, `media/` and `poc/muestras/` are generated output — keep them git-ignored, never commit them.
- Commit messages: short, casual Spanish, no `feat:`/`chore:` prefixes.
