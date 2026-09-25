"""Escena 13 — Créditos de roles (sin voz, 15 s)."""

from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.escena00 import EXPOSITORES
from escenas.style import *


class Escena13(EscenaNarrada):
    numero = 13

    def construct(self):
        creditos = VGroup(
            titulo("CRÉDITOS", TAM_SUBTITULO),
            parrafo("\n".join(EXPOSITORES), TAM_CUERPO - 4, buff=0.2),
            texto("Profesor: Jorge Eduardo Ortiz Triviño", TAM_CUERPO - 4, t2c={"Profesor:": TEXTO_SECUNDARIO}),
            parrafo("Modelos Estocásticos y Simulación en Computación y Comunicaciones\nGrupo 2 · 2026-2",
                    TAM_PEQUENO, TEXTO_SECUNDARIO),
            titulo("Universidad Nacional de Colombia", TAM_CUERPO),
        ).arrange(DOWN, buff=0.6)
        # El desplazamiento entra por abajo y sale por arriba: se sale del cuadro a propósito.
        creditos.permite_solape = True
        altura = config.frame_height
        creditos.next_to([0, -altura / 2, 0], DOWN, buff=0.1)
        recorrido = altura + creditos.height + 0.2
        self.add(creditos)
        self.play(creditos.animate.shift(UP * recorrido), run_time=10, rate_func=linear)
        self.remove(creditos)

        logo = ImageMobject(str(LOGO_UNAL)).set_height(1.6)
        self.play(FadeIn(logo), run_time=1.2)
        self.esperar_hasta(self.duracion_total - 1.5)
        self.play(FadeOut(logo), run_time=1.5)
        self.terminar()
