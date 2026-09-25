"""Escena 4 — ¿Qué significa realmente la red?"""

from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.style import *


class Escena04(EscenaNarrada):
    numero = 4

    def construct(self):
        # Bloque 0 — Narrador: la red con sus tablas.
        self.iniciar_bloque(0)
        grupo = red_alarma_con_tablas()
        self.play(FadeIn(grupo), run_time=1.2)

        # Bloque 1 — Profesora: factorización.
        b = self.iniciar_bloque(1)
        fact = formula(r"P(x_1, \dots, x_n) = \prod_i P\big(x_i \mid \text{padres}(X_i)\big)", 52, RESALTADO)
        destino = grupo.copy()
        ajustar(destino, alto=ALTO_UTIL - fact.height - 0.8).to_edge(UP, buff=MARGEN)
        fact.next_to(destino, DOWN, buff=0.6)
        self.play(Transform(grupo, destino))
        self.play(Write(fact), run_time=1.5)
        self.esperar_hasta(b["fin"])

        # Bloque 2 — IA: un ejemplo con cinco multiplicaciones.
        b = self.iniciar_bloque(2)
        self.limpiar()
        caso = texto("Robo, sin terremoto, la alarma sonó, Camilo e Isabel llamaron", TAM_CUERPO, TEXTO_SECUNDARIO)
        pasos = tabla_formulas([
            [r"P(r, \neg t, a, c, i)", r"= P(c \mid a)\, P(i \mid a)\, P(a \mid r, \neg t)\, P(r)\, P(\neg t)"],
            ["", r"= 0{,}90 \times 0{,}70 \times 0{,}94 \times 0{,}001 \times 0{,}998"],
            ["", r"\approx 0{,}000591"],
        ], tam=44, alineacion="rl", buff=(0.15, 0.45))
        bloque = VGroup(caso, pasos).arrange(DOWN, buff=0.8)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(caso))
        self.en(b, "Tomo un número")
        self.play(FadeIn(pasos.filas[0]))
        self.en(b, "Cinco multiplicaciones")
        self.play(FadeIn(pasos.filas[1]))
        self.play(FadeIn(pasos.filas[2]), pasos.filas[2].animate.set_color(RESALTADO))
        self.esperar_hasta(b["fin"])

        # Bloque 3 — Estudiante (se mantiene).
        self.iniciar_bloque(3)

        # Bloque 4 — Profesora: independencia condicional.
        b = self.iniciar_bloque(4)
        self.limpiar()
        cabecera = titulo("Independencia condicional", TAM_SUBTITULO, RESALTADO).to_edge(UP, buff=MARGEN)
        red = red_alarma(escala=1.1)
        ajustar(red, alto=ALTO_UTIL - cabecera.height - 0.8).next_to(cabecera, DOWN, buff=0.8)
        self.play(FadeIn(cabecera), FadeIn(red))
        self.en(b, "Piensa en Isabel")
        self.play(red.estados(isabel="activo", alarma="activo", robo="inactivo", terremoto="inactivo"))
        self.en(b, "Indirectamente sí")
        self.play(red.estados(robo="normal", terremoto="activo"))
        self.en(b, "Pero si ya sabes")
        self.play(red.estados(alarma="evidencia", terremoto="inactivo", robo="inactivo"))
        self.esperar_hasta(b["fin"])

        # Bloque 5 — Analista: las dos reglas y el manto de Markov.
        b = self.iniciar_bloque(5)
        reglas = VGroup(
            parrafo("Regla 1: cada nodo es condicionalmente independiente\nde sus no descendientes, dados sus padres.",
                    TAM_PEQUENO, alineacion=LEFT),
            parrafo("Regla 2 (manto de Markov): cada nodo es independiente del resto\n"
                    "de la red, dados sus padres, sus hijos y los otros padres de sus hijos.",
                    TAM_PEQUENO, alineacion=LEFT),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        red_destino = red.copy().aplicar_estados(**{k: "normal" for k in red.nodos})
        ajustar(red_destino, alto=ALTO_UTIL - cabecera.height - reglas.height - 1.2)
        red_destino.next_to(cabecera, DOWN, buff=0.5)
        reglas.next_to(red_destino, DOWN, buff=0.5)
        ajustar(reglas)
        self.play(Transform(red, red_destino))
        self.play(FadeIn(reglas[0]))
        self.en(b, "Y hay una versión más fuerte")
        self.play(FadeIn(reglas[1]))
        self.play(red.estados(alarma="activo", robo="evidencia", terremoto="evidencia",
                              camilo="evidencia", isabel="evidencia"))
        manto = titulo("Manto de Markov de Alarma", TAM_SUBTITULO, NODO).move_to(cabecera)
        self.cambiar(cabecera, manto)
        self.en(b, "de-separación")
        self.esperar_hasta(b["fin"])

        # Bloque 6 — IA: la recompensa.
        b = self.iniciar_bloque(6)
        self.limpiar()
        general = texto("n variables, máximo k padres cada una:", TAM_CUERPO, TEXTO_SECUNDARIO)
        comp1 = tabla_formulas([
            [r"\text{Red bayesiana:}", r"n \cdot 2^k"],
            [r"\text{Tabla conjunta:}", r"2^n"],
        ], tam=44, alineacion="rl")
        ejemplo = texto("100 variables, máximo 5 padres:", TAM_CUERPO, TEXTO_SECUNDARIO)
        comp2 = tabla_formulas([
            [r"\text{Red bayesiana:}", r"100 \times 32 = 3.200 \text{ números}"],
            [r"\text{Tabla conjunta:}", r"\approx 1{,}27 \times 10^{30} \text{ números}"],
        ], tam=44, alineacion="rl")
        bloque = VGroup(general, comp1, ejemplo, comp2).arrange(DOWN, buff=0.45)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(general), FadeIn(comp1))
        self.en(b, "Con cien variables")
        self.play(FadeIn(ejemplo), FadeIn(comp2.filas[0]))
        self.play(comp2.filas[0][1].animate.set_color(RESALTADO))
        self.en(b, "Contra un uno")
        self.play(FadeIn(comp2.filas[1]))
        self.esperar_hasta(b["fin"])

        # Bloque 7 — Analista: OR ruidoso.
        b = self.iniciar_bloque(7)
        self.limpiar()
        cabecera = titulo("OR ruidoso (noisy-OR)", TAM_SUBTITULO, RESALTADO)
        causa = texto("Fiebre con tres causas posibles: Resfriado, Gripe, Malaria", TAM_PEQUENO, TEXTO_SECUNDARIO)
        qs = formula(r"q(\text{Resfriado}) = 0{,}6 \qquad q(\text{Gripe}) = 0{,}2 \qquad q(\text{Malaria}) = 0{,}1", 40)
        tabla = tabla_cpt(
            ["Resfriado", "Gripe", "Malaria", "P(¬fiebre)", "P(fiebre)"],
            [
                ["V", "F", "F", "0,6", "0,4"],
                ["V", "V", "F", "0,6 × 0,2 = 0,12", "0,88"],
                ["V", "F", "V", "0,6 × 0,1 = 0,06", "0,94"],
                ["V", "V", "V", "0,6 × 0,2 × 0,1 = 0,012", "0,988"],
                ["F", "F", "F", "1", "0"],
            ],
        )
        bloque = VGroup(cabecera, causa, qs, tabla).arrange(DOWN, buff=0.4)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(cabecera), FadeIn(causa))
        self.en(b, "Cada causa, sola")
        self.play(FadeIn(qs))
        self.en(b, "basta con multiplicarlas")
        self.play(FadeIn(tabla), run_time=1.5)
        self.esperar_hasta(b["fin"])

        # Bloque 8 — IA: la red médica CPCS.
        b = self.iniciar_bloque(8)
        self.limpiar()
        cabecera = titulo("Red médica CPCS (medicina interna)", TAM_SUBTITULO)
        tam = texto("448 nodos · 906 enlaces", TAM_CUERPO, TEXTO_SECUNDARIO)
        numeros = tabla_formulas([
            [r"\text{Con tablas completas:}", r"133.931.430 \text{ parámetros}"],
            [r"\text{Con OR ruidoso y máximo ruidoso:}", r"8.254 \text{ parámetros}"],
        ], tam=44, alineacion="rl")
        bloque = VGroup(cabecera, tam, numeros).arrange(DOWN, buff=0.6)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(cabecera))
        self.en(b, "cuatrocientas cuarenta y ocho")
        self.play(FadeIn(tam))
        self.en(b, "Con tablas completas")
        self.play(FadeIn(numeros.filas[0]))
        self.en(b, "le bastan poco más")
        self.play(FadeIn(numeros.filas[1]))
        self.play(numeros.filas[1].animate.set_color(RESALTADO))
        self.terminar()
