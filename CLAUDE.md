# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Narrated explainer video (in Spanish) on probabilistic reasoning / Bayesian networks, AIMA chapter 13. Code, comments, script and commit messages are in Spanish.

## Commands

On this machine run Python with `py`, not `python`. Run everything from the repo root (scenes import `escenas.comun`).

```
py herramientas/generar_audio.py            # TTS for every scene in guion/guion.txt (or: ... 3 5)
py herramientas/renderizar.py               # render all scenes as 480p drafts and join them into salida/
py herramientas/renderizar.py --final -j 3  # 1080p30, 3 scenes in parallel
py herramientas/renderizar.py 3             # re-render one scene (joins only if all 14 clips exist)
py -m manim -ql escenas/escena03.py Escena03   # render one scene directly
```

Do not use `-qh`: it forces 60 fps and ignores `manim.cfg` (1920x1080, 30 fps); the final quality is no `-q` flag. edge-tts needs internet. There are no tests; `renderizar.py` reports layout warnings, and a render can be checked with `ffprobe` (the MP4 has an AAC track, but VS Code's video preview plays it silent — use an external player).

## Pipeline

`guion/guion.txt` → `herramientas/generar_audio.py` → `audio/escenaNN/{bloques/, completo.mp3, timings.json}` → `escenas/escenaNN.py` (class `EscenaNN`) → `herramientas/renderizar.py` → `salida/razonamiento_probabilistico[_borrador].mp4`.

- Script format: the file is split into scenes (0–13) at lines starting with `ESCENA N`. A block runs from one `[VOZ: X]` to the next and contains `[TEXTO_TTS]...[/TEXTO_TTS]` plus an optional `[PAUSA_DESPUÉS: s]`. `[VISUAL: ...]` is the brief for the animation; `[INICIO]`/`[FIN]` are not spoken. Scenes 0, 12 and 13 are `[SIN_VOZ]` + `[DURACIÓN: n]`: no blocks, and their `completo.mp3` is silence so every clip has audio and they concatenate without re-encoding.
- **Do not show the speaker label** ("Rótulo: <PERSONAJE>" in the `[VISUAL]` blocks) in any scene — the team decided against it, overriding the script's convention.
- Voice names map to edge-tts voice ids in `VOCES` at the top of `generar_audio.py`; the whole script is validated before any synthesis.
- Scenes subclass `EscenaNarrada` (`escenas/comun.py`): set `numero`, and time animations with `iniciar_bloque(i)` / `esperar_hasta(t)` / `terminar()` against `timings.json`, so regenerating audio re-syncs the video.
- **Nothing on screen may overlap or leave the frame.** After every `play()`, `EscenaNarrada` checks the top-level mobjects' bounding boxes and logs a `DISPOSICION` warning; `renderizar.py` lists them per scene. Fix every warning. Reserve space explicitly (`components.ajustar()`, `arrange`, `next_to`, the `ancho`/`alto` parameters of the network builders, `ANCHO_UTIL`/`ALTO_UTIL`). For an intentional overlay, group it with what it covers or set `mob.permite_solape = True`.
- Design system: every color, font and size comes from `escenas/style.py`; repeated visuals (`RedBayesiana` and `red_alarma()` / `red_aspersor()` with node states and `renombrar()`, CPT tables, calculation blocks, highlighted results, section titles, lists, phone) come from `escenas/components.py`. Build text with `components.texto()` / `titulo()`, not `Text` directly: they work around Manim's bad letter spacing at small font sizes. Multi-line text that must share baselines should be one `texto("a\nb")`.

## Environment

- FFmpeg and MiKTeX (per-user, `%LOCALAPPDATA%\Programs\MiKTeX`, auto-install of missing packages enabled) are installed, so `Tex`/`MathTex` work, including Spanish accents. Update MiKTeX with `miktex packages update`.
- `audio/`, `media/` and `salida/` are generated output — keep them git-ignored, never commit them.
- Commit messages: short, casual Spanish, no `feat:`/`chore:` prefixes.
