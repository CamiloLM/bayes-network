"""Base común para las escenas: carga el audio de la escena y sincroniza con él."""

import json
from pathlib import Path

from manim import *

RAIZ = Path(__file__).resolve().parents[1]
DIR_AUDIO = RAIZ / "audio"

# Color con el que se identifica a cada voz en pantalla.
COLOR_VOZ = {
    "NARRADOR": GRAY_B,
    "ESTUDIANTE": BLUE,
    "PROFESORA": GREEN,
    "IA": ORANGE,
    "ANALISTA": PURPLE,
}


class EscenaNarrada(Scene):
    """Escena sincronizada con audio/escenaNN/, generado por herramientas/generar_audio.py.

    Las subclases definen `numero` y usan `self.bloques[i]["inicio"|"fin"]`
    con `esperar_hasta(t)` para que cada animación arranque con su voz.
    """

    numero: int

    def setup(self):
        dir_escena = DIR_AUDIO / f"escena{self.numero:02d}"
        ruta_timings = dir_escena / "timings.json"
        if not ruta_timings.exists():
            raise FileNotFoundError(
                f"No existe {ruta_timings}. Corre primero: py herramientas/generar_audio.py {self.numero}"
            )
        timings = json.loads(ruta_timings.read_text(encoding="utf-8"))
        self.bloques = timings["bloques"]
        self.duracion_total = timings["duracion_total"]
        self.etiqueta_voz = VMobject()
        self.add_sound(str(dir_escena / "completo.mp3"))

    def esperar_hasta(self, t: float):
        """Espera hasta el segundo t del audio (si ya pasó, no espera)."""
        restante = t - self.renderer.time
        if restante > 0.01:
            self.wait(restante)

    def mostrar_voz(self, bloque: dict):
        """Muestra en la esquina el nombre de quien habla."""
        voz = bloque["voz"].upper()
        nueva = Text(voz, font_size=28, color=COLOR_VOZ.get(voz, WHITE)).to_corner(UL)
        self.play(FadeOut(self.etiqueta_voz), FadeIn(nueva), run_time=0.4)
        self.etiqueta_voz = nueva

    def iniciar_bloque(self, i: int) -> dict:
        """Espera al inicio del bloque i (desde 0), muestra su voz y lo devuelve."""
        bloque = self.bloques[i]
        self.esperar_hasta(bloque["inicio"])
        self.mostrar_voz(bloque)
        return bloque

    def terminar(self, margen: float = 1.0):
        """Espera a que termine el audio de la escena, más un margen."""
        self.esperar_hasta(self.duracion_total + margen)
