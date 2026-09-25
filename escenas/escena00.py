"""Escena 0 — Portada (sin voz, 12 s).

    py -m manim -ql escenas/escena00.py Escena00
"""

from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import texto, titulo
from escenas.style import *

EXPOSITORES = [
    "Julián David Albarracín Galindo",
    "Andrés David Caro Mora",
    "Daniel Alfonso Cely Infante",
    "Camilo Ferney Londoño Moreno",
    "Daniel Alejandro Ochoa Ruiz",
    "Sara Isabel Ospina Valderrama",
    "Juan Camilo Vergara Tao",
]


class Escena00(EscenaNarrada):
    numero = 0

    def construct(self):
        logo = ImageMobject(str(LOGO_UNAL)).set_height(0.8)
        universidad = titulo("UNIVERSIDAD NACIONAL DE COLOMBIA", 22)
        cabecera = Group(logo, universidad).arrange(DOWN, buff=0.15)

        asignatura = VGroup(
            texto("MODELOS ESTOCÁSTICOS Y SIMULACIÓN EN COMPUTACIÓN Y COMUNICACIONES", 20, TEXTO_SECUNDARIO),
            texto("Grupo 2 · Semestre 2026-2", 20, TEXTO_SECUNDARIO),
        ).arrange(DOWN, buff=0.12)

        capitulo = titulo("CAPÍTULO 13", 30, RESALTADO)
        nombre = titulo("RAZONAMIENTO PROBABILÍSTICO", 50)
        subtitulo = texto("Redes bayesianas, inferencia y causalidad", 30, NODO)
        fuente = texto(
            "Basado en: Russell y Norvig, Artificial Intelligence: A Modern Approach (4.ª ed.)",
            18, TEXTO_SECUNDARIO, slant=ITALIC,
        )
        bloque_titulo = VGroup(capitulo, nombre, subtitulo, fuente).arrange(DOWN, buff=0.14)
        fuente.shift(DOWN * 0.06)

        # Cada columna es un solo Text para que las líneas compartan línea base.
        columnas = VGroup(
            texto("\n".join(EXPOSITORES[:4]), 20, line_spacing=0.9),
            texto("\n".join(EXPOSITORES[4:]), 20, line_spacing=0.9),
        ).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        expositores = VGroup(texto("Expositores", 20, TEXTO_SECUNDARIO), columnas).arrange(DOWN, buff=0.15)
        profesor = texto("Profesor: Jorge Eduardo Ortiz Triviño", 20, t2c={"Profesor:": TEXTO_SECUNDARIO})
        personas = VGroup(expositores, profesor).arrange(DOWN, buff=0.25)

        Group(cabecera, asignatura, bloque_titulo, personas).arrange(DOWN, buff=0.3).move_to(UP * 0.15)

        pie = texto("Universidad Nacional de Colombia · 2026", 16, TEXTO_SECUNDARIO)
        pie.to_edge(DOWN, buff=0.2)
        linea = Line(LEFT, RIGHT, stroke_width=1.5, color=TEXTO_SECUNDARIO).set_width(config.frame_width * 0.5)
        linea.next_to(bloque_titulo, UP, buff=0.15)

        self.play(FadeIn(cabecera, shift=DOWN * 0.2), run_time=1.2)
        self.play(FadeIn(asignatura), Create(linea), run_time=0.8)
        self.play(FadeIn(capitulo, shift=UP * 0.2), Write(nombre), run_time=1.5)
        self.play(FadeIn(subtitulo), FadeIn(fuente), run_time=0.8)
        self.play(LaggedStart(FadeIn(expositores), FadeIn(profesor), FadeIn(pie), lag_ratio=0.3), run_time=1.2)

        self.esperar_hasta(self.duracion_total - 1)
        self.play(*(FadeOut(m) for m in self.mobjects), run_time=1)
        self.terminar()
