"""Escena 5 — ¿Qué hacemos con la evidencia?"""

from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.style import *


class Escena05(EscenaNarrada):
    numero = 5

    def construct(self):
        # Bloque 0 — Narrador: dos celulares sonando.
        b = self.iniciar_bloque(0)
        moviles = VGroup(celular("Camilo llamando..."), celular("Isabel llamando...")).arrange(RIGHT, buff=2.0)
        moviles.shift(UP * 0.8)
        self.play(FadeIn(moviles[0]))
        self.play(Wiggle(moviles[0]))
        self.en(b, "Isabel llamó")
        self.play(FadeIn(moviles[1]))
        self.play(Wiggle(moviles[1]))
        leyenda = texto("Camilo llamó. Isabel llamó. Nadie vio nada.", TAM_CUERPO).next_to(moviles, DOWN, buff=0.7)
        self.play(FadeIn(leyenda))
        self.en(b, "Esta es una pregunta de inferencia")
        etiqueta = titulo("Pregunta de inferencia", TAM_SUBTITULO, RESALTADO).next_to(leyenda, DOWN, buff=0.5)
        self.play(FadeIn(etiqueta))
        self.esperar_hasta(b["fin"])

        # Bloque 1 — Profesora: previa y posterior.
        b = self.iniciar_bloque(1)
        self.limpiar()
        filas = tabla_formulas([
            [r"\text{Antes de la evidencia:}", r"P(\text{Robo}) = 0{,}001",
             r"\rightarrow \text{probabilidad previa}"],
            [r"\text{Después de la evidencia:}", r"P(\text{Robo} \mid \text{Camilo}, \text{Isabel}) = \;?",
             r"\rightarrow \text{probabilidad posterior}"],
        ], tam=40, alineacion="rll", buff=(0.4, 0.8))
        ajustar(filas).move_to(ORIGIN)
        self.play(FadeIn(filas.filas[0]))
        self.en(b, "Después de observar")
        self.play(FadeIn(filas.filas[1]))
        self.esperar_hasta(b["fin"])

        # Bloque 2 — Analista: el resultado.
        b = self.iniciar_bloque(2)
        self.limpiar()
        resultado = resultado_destacado("P(Robo | Camilo llamó, Isabel llamó) ≈ 28,4 %", 48)
        ajustar(resultado).shift(UP * 0.8)
        self.play(GrowFromCenter(resultado), run_time=1.2)
        self.play(Indicate(resultado[1], color=RESALTADO, scale_factor=1.05))
        self.esperar_hasta(b["fin"])

        # Bloque 3 — Profesora: menos de lo que creías.
        b = self.iniciar_bloque(3)
        self.en(b, "lo más probable es que no haya ladrón")
        sin_ladron = texto("71,6 % : no hay ladrón", TAM_SUBTITULO, TEXTO_SECUNDARIO).next_to(resultado, DOWN, buff=0.7)
        self.play(FadeIn(sin_ladron))
        self.esperar_hasta(b["fin"])

        # Bloque 4 — Estudiante (se mantiene).
        self.iniciar_bloque(4)

        # Bloque 5 — Profesora: por qué tan bajo.
        b = self.iniciar_bloque(5)
        razones = VGroup(
            texto("•  los robos son rarísimos: 1 en 1.000", TAM_CUERPO),
            texto("•  otras explicaciones: temblor, falsa alarma, teléfono confundido", TAM_CUERPO),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(sin_ladron, DOWN, buff=0.6)
        ajustar(razones)
        self.play(FadeIn(razones[0]))
        self.en(b, "Y porque las dos llamadas")
        self.play(FadeIn(razones[1]))
        self.en(b, "La evidencia no eliminó")
        cambio = titulo("de 1 en 1.000  →  casi 1 de cada 3", TAM_SUBTITULO, RESALTADO)
        cambio.next_to(resultado, DOWN, buff=0.7)
        self.play(FadeOut(sin_ladron, razones), FadeIn(cambio))
        self.terminar()
