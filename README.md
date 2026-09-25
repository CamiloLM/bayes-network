# Razonamiento probabilístico — video con Manim

Video explicativo sobre redes bayesianas (Russell & Norvig, *AIMA*, cap. 13), narrado con voces de edge-tts y animado con Manim.

## Estructura

```
guion/guion.txt           guion completo, dividido en "ESCENA N"
herramientas/
  generar_audio.py        guion -> audio/escenaNN/ (MP3 por bloque, completo.mp3, timings.json)
escenas/
  comun.py                clase base EscenaNarrada (carga el audio y sincroniza)
  escena01.py ...         una escena de Manim por archivo
audio/, media/            salidas generadas (ignoradas por git)
```

## Formato del guion

```
ESCENA 1 — LA ALARMA

[VOZ: NARRADOR]
[VISUAL: descripción para la animación; no se lee en voz alta]
[TEXTO_TTS]
Texto que se sintetiza.
[/TEXTO_TTS]
[PAUSA_DESPUÉS: 0.5]
```

Las voces se asignan en el diccionario `VOCES` de `herramientas/generar_audio.py`.

## Flujo

```
py -m pip install -r requirements.txt
py herramientas/generar_audio.py              # todas las escenas (o: ... 3 5)
py -m manim -ql escenas/escena01.py Escena01  # borrador 480p; -qh para 1080p
```

Requiere FFmpeg en el PATH y conexión a internet (edge-tts usa el servicio de Microsoft).
El video queda en `media/videos/escena01/480p15/Escena01.mp4`, con el audio incluido.
