# Razonamiento probabilístico — video con Manim

Video explicativo sobre redes bayesianas (Russell & Norvig, *AIMA*, cap. 13), narrado con voces de edge-tts y animado con Manim.

## Estructura

```
guion/guion.txt           guion completo, dividido en "ESCENA N"
herramientas/
  generar_audio.py        guion -> audio/escenaNN/ (MP3 por bloque, completo.mp3, timings.json)
  renderizar.py           renderiza las escenas y las une en salida/
escenas/
  style.py                sistema de diseño: colores, fuentes, tamaños, grafos
  components.py           redes bayesianas, tablas CPT, títulos, resultados, etc.
  comun.py                clase base EscenaNarrada (carga el audio y sincroniza)
  escena00.py ...         una escena de Manim por archivo (Escena00 ... Escena13)
assets/                   logo de la UNAL
manim.cfg                 1920x1080 a 30 fps
audio/, media/, salida/   salidas generadas (ignoradas por git)
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
py herramientas/generar_audio.py              # audio de todas las escenas (o: ... 3 5)
py herramientas/renderizar.py                 # borrador 480p de todo el video
py herramientas/renderizar.py --final -j 3    # versión final 1080p30
```

Requiere FFmpeg y MiKTeX en el PATH, y conexión a internet (edge-tts usa el servicio de Microsoft).
El video completo queda en `salida/razonamiento_probabilistico_borrador.mp4` (o sin `_borrador` en la versión final).
Cada escena por separado está en `media/videos/escenaNN/`. `renderizar.py` avisa si en alguna escena hay elementos que se sobreponen o se salen del cuadro.
