"""Genera la narración del video a partir del guion.

El guion (guion/guion.txt) se divide en escenas con líneas que empiezan por
"ESCENA N". Dentro de cada escena, cada bloque tiene este formato:

    [VOZ: NARRADOR]
    [VISUAL: acotaciones opcionales, se ignoran]
    [TEXTO_TTS] Texto que se va a sintetizar. [/TEXTO_TTS]
    [PAUSA_DESPUÉS: 1.5]

Si el guion no tiene encabezados "ESCENA N", todo el archivo es la escena 1.

Salidas, por escena (audio/escenaNN/):
    bloques/bloque_XX.mp3  -> un MP3 por bloque
    completo.mp3           -> audio concatenado con las pausas
    timings.json           -> inicio y duración de cada bloque (lo lee Manim)

Uso:
    py herramientas/generar_audio.py              # todas las escenas
    py herramientas/generar_audio.py 3 5          # solo las escenas 3 y 5
    py herramientas/generar_audio.py --guion otro.txt
"""

import argparse
import asyncio
import json
import re
from dataclasses import dataclass
from pathlib import Path

import edge_tts
from pydub import AudioSegment

# --- Configuración -----------------------------------------------------------

# Nombre de voz en el guion (sin distinguir mayúsculas) -> voice_id de edge-tts.
# Lista completa de voces: `py -m edge_tts --list-voices`
VOCES = {
    "NARRADOR": "es-CO-GonzaloNeural",
    "PROFESORA": "es-CO-SalomeNeural",
    "ESTUDIANTE": "es-MX-JorgeNeural",
    "ANALISTA": "es-MX-DaliaNeural",
    "IA": "es-US-AlonsoNeural",
}

# Parámetros de prosodia de edge-tts (p. ej. "+10%", "-5Hz").
RATE = "+0%"
PITCH = "+0Hz"

RAIZ = Path(__file__).resolve().parents[1]
GUION = RAIZ / "guion" / "guion.txt"
DIR_AUDIO = RAIZ / "audio"

# --- Parseo ------------------------------------------------------------------

RE_ESCENA = re.compile(r"^ESCENA\s+(\d+)\b.*$", re.IGNORECASE | re.MULTILINE)
RE_VOZ = re.compile(r"\[VOZ:\s*([^\]]+?)\s*\]", re.IGNORECASE)
RE_TEXTO = re.compile(r"\[TEXTO_TTS\](.*?)\[/TEXTO_TTS\]", re.IGNORECASE | re.DOTALL)
RE_PAUSA = re.compile(r"\[PAUSA_DESPU[ÉE]S:\s*([\d.,]+)\s*s?\s*\]", re.IGNORECASE)


@dataclass
class Bloque:
    voz: str
    texto: str
    pausa: float  # segundos de silencio tras el bloque


def dividir_escenas(contenido: str) -> dict[int, str]:
    """Devuelve {número de escena: texto de la escena}."""
    marcas = list(RE_ESCENA.finditer(contenido))
    if not marcas:
        return {1: contenido}
    escenas = {}
    for i, marca in enumerate(marcas):
        fin = marcas[i + 1].start() if i + 1 < len(marcas) else len(contenido)
        numero = int(marca.group(1))
        if numero in escenas:
            raise ValueError(f"La escena {numero} aparece dos veces en el guion.")
        escenas[numero] = contenido[marca.start():fin]
    return escenas


def parsear_bloques(contenido: str, escena: int) -> list[Bloque]:
    """Devuelve los bloques en orden. Cada bloque va desde un [VOZ: X] hasta el siguiente."""
    marcas = list(RE_VOZ.finditer(contenido))
    if not marcas:
        raise ValueError(f"La escena {escena} no tiene ningún marcador [VOZ: ...].")

    bloques = []
    for i, marca in enumerate(marcas):
        fin = marcas[i + 1].start() if i + 1 < len(marcas) else len(contenido)
        tramo = contenido[marca.end():fin]

        m_texto = RE_TEXTO.search(tramo)
        if not m_texto:
            raise ValueError(
                f"Escena {escena}, bloque {i + 1} ({marca.group(1)}): falta [TEXTO_TTS]...[/TEXTO_TTS]."
            )
        texto = " ".join(m_texto.group(1).split())

        m_pausa = RE_PAUSA.search(tramo)
        pausa = float(m_pausa.group(1).replace(",", ".")) if m_pausa else 0.0

        bloques.append(Bloque(voz=marca.group(1).strip(), texto=texto, pausa=pausa))
    return bloques


def resolver_voz(nombre: str) -> str:
    voces = {k.upper(): v for k, v in VOCES.items()}
    try:
        return voces[nombre.upper()]
    except KeyError:
        raise KeyError(
            f"La voz '{nombre}' no está en VOCES. Añádela al diccionario al inicio del script."
        ) from None


# --- Síntesis y montaje ------------------------------------------------------

async def sintetizar(bloques: list[Bloque], dir_bloques: Path) -> list[Path]:
    dir_bloques.mkdir(parents=True, exist_ok=True)
    rutas = []
    for i, b in enumerate(bloques, start=1):
        ruta = dir_bloques / f"bloque_{i:02d}.mp3"
        print(f"  [{i}/{len(bloques)}] {b.voz}: {b.texto[:60]}{'...' if len(b.texto) > 60 else ''}")
        await edge_tts.Communicate(b.texto, resolver_voz(b.voz), rate=RATE, pitch=PITCH).save(str(ruta))
        rutas.append(ruta)
    return rutas


def montar(bloques: list[Bloque], rutas: list[Path], dir_escena: Path) -> dict:
    final = AudioSegment.empty()
    timings = []
    for i, (b, ruta) in enumerate(zip(bloques, rutas), start=1):
        audio = AudioSegment.from_mp3(ruta)
        inicio = len(final) / 1000
        final += audio
        if b.pausa > 0:
            final += AudioSegment.silent(duration=round(b.pausa * 1000), frame_rate=audio.frame_rate)
        timings.append({
            "indice": i,
            "voz": b.voz,
            "voice_id": resolver_voz(b.voz),
            "texto": b.texto,
            "archivo": ruta.relative_to(dir_escena).as_posix(),
            "inicio": round(inicio, 3),
            "duracion": round(len(audio) / 1000, 3),
            "pausa_despues": b.pausa,
            "fin": round(inicio + len(audio) / 1000, 3),
        })

    final.export(dir_escena / "completo.mp3", format="mp3")
    return {"duracion_total": round(len(final) / 1000, 3), "bloques": timings}


def generar_escena(numero: int, contenido: str) -> float:
    bloques = parsear_bloques(contenido, numero)
    for b in bloques:
        resolver_voz(b.voz)  # falla antes de sintetizar si falta alguna voz

    dir_escena = DIR_AUDIO / f"escena{numero:02d}"
    print(f"Escena {numero}: {len(bloques)} bloques")
    rutas = asyncio.run(sintetizar(bloques, dir_escena / "bloques"))
    resultado = montar(bloques, rutas, dir_escena)
    (dir_escena / "timings.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  -> {dir_escena.relative_to(RAIZ).as_posix()}/ ({resultado['duracion_total']:.1f} s)")
    return resultado["duracion_total"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera el audio del guion con edge-tts.")
    parser.add_argument("escenas", nargs="*", type=int, help="números de escena (por defecto, todas)")
    parser.add_argument("--guion", type=Path, default=GUION, help="archivo del guion")
    args = parser.parse_args()

    escenas = dividir_escenas(args.guion.read_text(encoding="utf-8"))
    elegidas = args.escenas or sorted(escenas)
    faltantes = [n for n in elegidas if n not in escenas]
    if faltantes:
        parser.error(f"el guion no tiene las escenas {faltantes}; tiene {sorted(escenas)}")

    # Valida todo el guion antes de gastar tiempo sintetizando.
    for n in elegidas:
        for b in parsear_bloques(escenas[n], n):
            resolver_voz(b.voz)

    total = sum(generar_escena(n, escenas[n]) for n in elegidas)
    minutos, segundos = divmod(total, 60)
    print(f"\nDuración total: {int(minutos)}:{segundos:04.1f} ({len(elegidas)} escenas)")


if __name__ == "__main__":
    main()
