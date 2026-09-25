"""Renderiza las escenas y las une en el video completo.

    py herramientas/renderizar.py               # borrador 480p15, todas las escenas
    py herramientas/renderizar.py --final       # 1080p30
    py herramientas/renderizar.py 3 5           # solo las escenas 3 y 5
    py herramientas/renderizar.py -j 3          # 3 escenas en paralelo
    py herramientas/renderizar.py --solo-unir   # no renderiza, solo une los clips

Requiere haber generado el audio (py herramientas/generar_audio.py). Al final
une los clips de las 14 escenas en salida/; si falta alguno, no une y lo dice.
Muestra los avisos de disposición (solapes o elementos fuera del cuadro).
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DIR_ESCENAS = RAIZ / "escenas"
DIR_SALIDA = RAIZ / "salida"
TOTAL_ESCENAS = 14  # 0 a 13

CALIDADES = {
    "borrador": {"flags": ["-ql"], "carpeta": "480p15"},
    "final": {"flags": [], "carpeta": "1080p30"},  # manim.cfg: 1920x1080, 30 fps
}

RE_AVISO = re.compile(r"DISPOSICION .*")


def archivo_escena(n: int) -> Path:
    return DIR_ESCENAS / f"escena{n:02d}.py"


def clip(n: int, calidad: str) -> Path:
    return RAIZ / "media" / "videos" / f"escena{n:02d}" / CALIDADES[calidad]["carpeta"] / f"Escena{n:02d}.mp4"


def entorno() -> dict:
    env = {**os.environ, "COLUMNS": "200"}  # que rich no parta las líneas del log
    # Una terminal abierta antes de instalar MiKTeX no tiene latex en el PATH.
    miktex = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64"
    if not shutil.which("latex") and miktex.exists():
        env["PATH"] = f"{miktex}{os.pathsep}{env.get('PATH', '')}"
    return env


def renderizar(n: int, calidad: str) -> tuple[int, bool, list[str], str]:
    cmd = [sys.executable, "-m", "manim", *CALIDADES[calidad]["flags"], str(archivo_escena(n)), f"Escena{n:02d}"]
    proc = subprocess.run(
        cmd, cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace", env=entorno()
    )
    salida = proc.stdout + proc.stderr
    avisos = sorted(set(RE_AVISO.findall(salida)))
    return n, proc.returncode == 0, avisos, salida


def informar(n: int, ok: bool, avisos: list[str], salida: str) -> bool:
    """Imprime el resultado de una escena; devuelve si se renderizó bien."""
    print(f"  escena {n:2d}: {'ok' if ok else 'ERROR'}" + (f", {len(avisos)} avisos" if avisos else ""))
    for aviso in avisos:
        print(f"      {aviso}")
    if not ok:
        print("      " + "\n      ".join(salida.strip().splitlines()[-15:]))
    return ok


def unir(calidad: str) -> Path | None:
    clips = [clip(n, calidad) for n in range(TOTAL_ESCENAS)]
    faltan = [n for n, c in enumerate(clips) if not c.exists()]
    if faltan:
        print(f"\nNo se unió el video: faltan los clips de las escenas {faltan}.")
        return None
    DIR_SALIDA.mkdir(exist_ok=True)
    destino = DIR_SALIDA / ("razonamiento_probabilistico.mp4" if calidad == "final"
                            else "razonamiento_probabilistico_borrador.mp4")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as lista:
        lista.writelines(f"file '{c.as_posix()}'\n" for c in clips)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista.name, "-c", "copy", str(destino)],
        check=True,
    )
    Path(lista.name).unlink()
    return destino


def main() -> None:
    parser = argparse.ArgumentParser(description="Renderiza las escenas y une el video.")
    parser.add_argument("escenas", nargs="*", type=int, help="números de escena (por defecto, todas)")
    parser.add_argument("--final", action="store_true", help="1080p30 en lugar de borrador 480p15")
    parser.add_argument("-j", type=int, default=1, help="escenas en paralelo")
    parser.add_argument("--solo-unir", action="store_true", help="no renderiza; solo une los clips")
    args = parser.parse_args()
    calidad = "final" if args.final else "borrador"

    if not args.solo_unir:
        elegidas = args.escenas or [n for n in range(TOTAL_ESCENAS) if archivo_escena(n).exists()]
        faltantes = [n for n in elegidas if not archivo_escena(n).exists()]
        if faltantes:
            parser.error(f"no existen los archivos de las escenas {faltantes}")

        print(f"Renderizando {len(elegidas)} escenas ({calidad})...")
        with ThreadPoolExecutor(max_workers=args.j) as pool:
            fallos = [n for n, *r in pool.map(lambda n: renderizar(n, calidad), elegidas) if not informar(n, *r)]
        if fallos and args.j > 1:
            # En paralelo, dos escenas pueden compilar el mismo LaTeX a la vez y chocar.
            print(f"Reintentando en serie: {fallos}")
            fallos = [n for n in fallos if not informar(*renderizar(n, calidad))]
        if fallos:
            print(f"\nFallaron las escenas {fallos}; no se une el video.")
            sys.exit(1)

    destino = unir(calidad)
    if destino:
        print(f"\nVideo: {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
