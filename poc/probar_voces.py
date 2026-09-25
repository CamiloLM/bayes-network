"""Genera muestras de voces candidatas por personaje para compararlas de oído.

    py poc/probar_voces.py                  # todos los personajes con texto
    py poc/probar_voces.py ESTUDIANTE       # solo algunos

Salida: poc/muestras/{personaje}_{voice_id}.mp3 y ..._alt.mp3 para las
entradas con rate/pitch modificados. No toca herramientas/generar_audio.py.
"""

import asyncio
import sys
from pathlib import Path

import edge_tts

# --- Configuración -----------------------------------------------------------

# Fragmento real del guion por personaje. Un personaje sin texto se omite.
TEXTOS_PRUEBA = {
    # guion/guion.txt, escena 1, bloque 3.
    "PROFESORA": (
        "Guarda esa respuesta. Vamos a volver a ella. "
        "Pero fíjate en la palabra que usaste: \"probable\". No dijiste \"seguro\". "
        "Una máquina inteligente casi nunca sabe con certeza qué ocurrió."
    ),
    # guion/guion.txt, escena 1, bloque 2 (su única línea hasta ahora).
    "ESTUDIANTE": (
        "Bueno... si dos personas llamaron por la alarma, "
        "yo diría que es bastante probable que haya un robo."
    ),
    # Pendiente: la Analista no habla en la escena 1; falta el guion completo.
    "ANALISTA": None,
}

# Rate/pitch para "rejuvenecer" la voz del Estudiante.
JUVENIL = {"rate": "+12%", "pitch": "+15Hz"}


def con_variante(voces: list[str], ajuste: dict) -> list[dict]:
    """Cada voz tal cual y, justo después, su variante con el ajuste."""
    return [e for v in voces for e in ({"voz": v}, {"voz": v, **ajuste})]


# Voces a probar por personaje. Cada entrada: {"voz", "rate"?, "pitch"?}.
CANDIDATAS = {
    "PROFESORA": [
        {"voz": "es-ES-XimenaNeural"},
        {"voz": "es-MX-DaliaNeural"},
        {"voz": "es-AR-ElenaNeural"},
        {"voz": "es-CL-CatalinaNeural"},
        {"voz": "en-US-AvaMultilingualNeural"},
        {"voz": "en-US-EmmaMultilingualNeural"},
        {"voz": "de-DE-SeraphinaMultilingualNeural"},
        {"voz": "fr-FR-VivienneMultilingualNeural"},
    ],
    "ESTUDIANTE": con_variante(
        [
            "es-PE-CamilaNeural",
            "es-VE-PaolaNeural",
            "es-UY-ValentinaNeural",
            "es-PE-AlexNeural",
            "es-UY-MateoNeural",
        ],
        JUVENIL,
    ),
    "ANALISTA": [
        {"voz": "es-ES-ElviraNeural"},
        {"voz": "es-ES-AlvaroNeural"},
        {"voz": "es-AR-TomasNeural"},
        {"voz": "es-CL-LorenzoNeural"},
        {"voz": "es-VE-SebastianNeural"},
        {"voz": "en-US-AndrewMultilingualNeural"},
        {"voz": "en-US-BrianMultilingualNeural"},
    ],
}

DIR_MUESTRAS = Path(__file__).resolve().parent / "muestras"

# -----------------------------------------------------------------------------


def nombre_archivo(personaje: str, entrada: dict) -> str:
    alt = "_alt" if "rate" in entrada or "pitch" in entrada else ""
    return f"{personaje.lower()}_{entrada['voz']}{alt}.mp3"


async def main() -> None:
    personajes = [p.upper() for p in sys.argv[1:]] or list(CANDIDATAS)

    disponibles = {v["ShortName"] for v in await edge_tts.list_voices()}
    descartadas = sorted(
        {e["voz"] for p in personajes for e in CANDIDATAS[p]} - disponibles
    )
    if descartadas:
        print("Descartadas (no existen en edge-tts):", ", ".join(descartadas))

    DIR_MUESTRAS.mkdir(exist_ok=True)
    generados: dict[str, list[Path]] = {}
    for personaje in personajes:
        texto = TEXTOS_PRUEBA.get(personaje)
        if not texto:
            print(f"{personaje}: sin texto en TEXTOS_PRUEBA, se omite.")
            continue
        for entrada in CANDIDATAS[personaje]:
            if entrada["voz"] not in disponibles:
                continue
            ruta = DIR_MUESTRAS / nombre_archivo(personaje, entrada)
            print(f"  {ruta.name}")
            await edge_tts.Communicate(
                texto,
                entrada["voz"],
                rate=entrada.get("rate", "+0%"),
                pitch=entrada.get("pitch", "+0Hz"),
            ).save(str(ruta))
            generados.setdefault(personaje, []).append(ruta)

    total = sum(len(r) for r in generados.values())
    print(f"\nResumen: {total} archivos en {DIR_MUESTRAS}")
    for personaje, rutas in generados.items():
        print(f"\n{personaje} ({len(rutas)})")
        for i, ruta in enumerate(rutas, start=1):
            print(f"  {i:2d}. {ruta}")


if __name__ == "__main__":
    asyncio.run(main())
