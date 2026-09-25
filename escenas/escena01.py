"""Escena 1 — La alarma (versión de prueba del flujo; se reemplaza con la oficial).

    py -m manim -ql escenas/escena01.py Escena01
"""

from manim import *

from escenas.comun import EscenaNarrada


class Escena01(EscenaNarrada):
    numero = 1

    def construct(self):
        # Bloque 1 — Narrador: la llamada de John y Mary.
        b = self.iniciar_bloque(0)
        celular = RoundedRectangle(width=1.2, height=2.2, corner_radius=0.2, color=WHITE)
        self.play(Create(celular))
        self.play(Wiggle(celular), run_time=1)
        john = Text("John: «escuché la alarma»", font_size=32).next_to(celular, DOWN)
        self.esperar_hasta(b["inicio"] + 6)
        self.play(Write(john))
        self.esperar_hasta(b["inicio"] + 20)
        self.play(Wiggle(celular), run_time=1)
        mary = Text("Mary: «yo también la oí»", font_size=32).next_to(john, DOWN)
        self.play(Write(mary))
        self.esperar_hasta(b["inicio"] + 36)
        pregunta = Text("¿Qué ocurrió?", font_size=48, color=YELLOW).to_edge(UP, buff=1)
        self.play(Write(pregunta))
        self.esperar_hasta(b["fin"])
        self.play(FadeOut(celular, john, mary, pregunta), run_time=0.5)

        # Bloque 2 — Estudiante.
        self.iniciar_bloque(1)
        robo = Text("¿Hubo un robo?", font_size=56)
        self.play(Write(robo))

        # Bloque 3 — Profesora: probable no es seguro.
        self.iniciar_bloque(2)
        self.play(robo.animate.to_edge(UP, buff=1.2))
        idea = Text("probable  ≠  seguro", font_size=56, color=GREEN)
        self.play(Write(idea))

        # Bloque 4 — IA: la respuesta es un número.
        self.iniciar_bloque(3)
        formula = Text("P(Robo | evidencia) = ?", font_size=56, color=ORANGE)
        self.play(ReplacementTransform(idea, formula))

        # Bloque 5 — Narrador: título.
        self.iniciar_bloque(4)
        titulo = VGroup(
            Text("Razonamiento probabilístico", font_size=60),
            Text("Capítulo 13", font_size=36, color=GRAY_B),
        ).arrange(DOWN)
        self.play(FadeOut(robo, formula), FadeIn(titulo))
        self.terminar()
