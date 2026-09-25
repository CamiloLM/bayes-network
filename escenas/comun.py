"""Base común para las escenas: carga el audio de la escena, sincroniza con él
y revisa que nada se sobreponga ni se salga del cuadro."""

import json
from itertools import combinations

from manim import *

from escenas.style import RAIZ

DIR_AUDIO = RAIZ / "audio"

# Marca de los avisos de disposición; herramientas/renderizar.py los busca.
AVISO = "DISPOSICION"
TOLERANCIA = 0.02


class EscenaNarrada(Scene):
    """Escena sincronizada con audio/escenaNN/, generado por herramientas/generar_audio.py.

    Las subclases definen `numero` y usan `iniciar_bloque(i)` / `esperar_hasta(t)`
    para que cada animación arranque con su voz. En escenas [SIN_VOZ] no hay
    bloques: el audio es silencio de `duracion_total` segundos.

    Tras cada play() se revisa la pantalla: si dos objetos de primer nivel se
    sobreponen o uno se sale del cuadro, se registra un aviso. Para un solape
    intencional (p. ej. un marco de resaltado encima de algo), agrupa ambos en
    un VGroup o marca el objeto con `mob.permite_solape = True`.
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
        self.add_sound(str(dir_escena / "completo.mp3"))
        self._avisos = set()

    def esperar_hasta(self, t: float):
        """Espera hasta el segundo t del audio (si ya pasó, no espera)."""
        restante = t - self.renderer.time
        if restante > 0.01:
            self.wait(restante)

    def iniciar_bloque(self, i: int) -> dict:
        """Espera al inicio del bloque i (desde 0) y lo devuelve."""
        bloque = self.bloques[i]
        self.esperar_hasta(bloque["inicio"])
        return bloque

    def terminar(self, margen: float = 0.0):
        """Espera a que termine la escena (audio o [DURACIÓN]), más un margen."""
        self.esperar_hasta(self.duracion_total + margen)

    # --- Revisión de disposición --------------------------------------------

    def play(self, *args, **kwargs):
        super().play(*args, **kwargs)
        self.revisar_disposicion()

    def revisar_disposicion(self):
        visibles = [
            m for m in self.mobjects
            if not getattr(m, "permite_solape", False) and m.width > 0 and m.height > 0 and _visible(m)
        ]
        ancho, alto = config.frame_width / 2, config.frame_height / 2
        for m in visibles:
            if (m.get_left()[0] < -ancho - TOLERANCIA or m.get_right()[0] > ancho + TOLERANCIA
                    or m.get_bottom()[1] < -alto - TOLERANCIA or m.get_top()[1] > alto + TOLERANCIA):
                self._avisar(f"se sale del cuadro: {_nombre(m)}")
        for a, b in combinations(visibles, 2):
            if _se_cruzan(a, b):
                self._avisar(f"se sobreponen: {_nombre(a)} / {_nombre(b)}")

    def _avisar(self, mensaje: str):
        if mensaje not in self._avisos:
            self._avisos.add(mensaje)
            logger.warning(f"{AVISO} escena {self.numero} t={self.renderer.time:.1f}s: {mensaje}")


def _visible(m: Mobject) -> bool:
    if isinstance(m, ImageMobject):
        return True
    return any(
        sm.get_fill_opacity() > 0.05 or (sm.get_stroke_opacity() > 0.05 and sm.get_stroke_width() > 0)
        for sm in m.family_members_with_points()
    )


def _se_cruzan(a: Mobject, b: Mobject) -> bool:
    return (
        a.get_left()[0] < b.get_right()[0] - TOLERANCIA and b.get_left()[0] < a.get_right()[0] - TOLERANCIA
        and a.get_bottom()[1] < b.get_top()[1] - TOLERANCIA and b.get_bottom()[1] < a.get_top()[1] - TOLERANCIA
    )


def _nombre(m: Mobject) -> str:
    """Descripción corta para el aviso: el texto si lo tiene, si no la clase."""
    for sm in [m, *m.submobjects]:
        if isinstance(sm, Text):
            return f'"{sm.text[:30]}"'
    return type(m).__name__
