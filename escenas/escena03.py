"""Escena 3 — Construyendo una red bayesiana."""

from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.style import *


class Escena03(EscenaNarrada):
    numero = 3

    def construct(self):
        # Bloque 0 — Profesora: se construye el grafo.
        b = self.iniciar_bloque(0)
        red = red_alarma(escala=1.1)
        n, f = red.nodos, red.flechas
        self.en(b, "Un robo puede")
        self.play(FadeIn(n["robo"], scale=0.8), FadeIn(n["alarma"], scale=0.8))
        self.en(b, "Un terremoto también")
        self.play(FadeIn(n["terremoto"], scale=0.8))
        self.en(b, "flecha de Robo hacia Alarma")
        self.play(GrowArrow(f[("robo", "alarma")]))
        self.en(b, "y otra de Terremoto")
        self.play(GrowArrow(f[("terremoto", "alarma")]))
        self.en(b, "Si la alarma suena")
        self.play(FadeIn(n["camilo"], scale=0.8), FadeIn(n["isabel"], scale=0.8))
        self.en(b, "Así que dibujamos")
        self.play(GrowArrow(f[("alarma", "camilo")]), GrowArrow(f[("alarma", "isabel")]))
        self.consolidar(red)
        self.en(b, "no hay flecha del robo")
        falsa = DashedLine(
            n["robo"].borde_hacia(n["camilo"].get_center()), n["camilo"].borde_hacia(n["robo"].get_center()),
            color=NEGATIVO, stroke_width=4, buff=0.1,
        )
        tachon = Cross(scale_factor=0.25, stroke_color=NEGATIVO, stroke_width=6).move_to(falsa)
        sin_flecha = VGroup(falsa, tachon)
        falsa.permite_solape = tachon.permite_solape = True  # se dibujan a propósito sobre la red
        self.play(Create(falsa))
        self.play(Create(tachon))
        self.en(b, "Camilo solo oye la alarma")
        self.play(FadeOut(sin_flecha))
        self.esperar_hasta(b["fin"])

        # Bloque 1 — Analista: definición formal y el ciclo prohibido.
        b = self.iniciar_bloque(1)
        definicion = parrafo(
            "Red bayesiana = grafo dirigido acíclico\n+ una tabla de probabilidad condicional en cada nodo",
        ).to_edge(UP, buff=MARGEN)
        self.play(red.animate.scale(0.85).next_to(definicion, DOWN, buff=0.7), FadeIn(definicion))
        self.en(b, "Y no puede haber ciclos")
        # Flecha Isabel -> Robo que cerraría un ciclo (curva por la derecha de la red).
        ciclo = CurvedArrow(
            n["isabel"].get_right() + RIGHT * 0.15, n["robo"].get_top() + UP * 0.15,
            angle=PI * 0.75, color=NEGATIVO, stroke_width=4,
        )
        ciclo.permite_solape = True
        self.play(Create(ciclo), run_time=1.2)
        x = Cross(scale_factor=0.35, stroke_color=NEGATIVO, stroke_width=8).move_to(ciclo.point_from_proportion(0.5))
        x.permite_solape = True
        self.play(Create(x))
        self.wait(1)
        self.play(FadeOut(ciclo, x))
        self.esperar_hasta(b["fin"])

        # Bloque 2 — Estudiante. Bloque 3 — Profesora: flecha no es causa.
        self.iniciar_bloque(2)
        b = self.iniciar_bloque(3)
        self.en(b, "una flecha representa")
        aclaracion = parrafo(
            "Flecha = dependencia probabilística directa\n(no necesariamente una causa)", color=RESALTADO,
        ).move_to(definicion)
        self.cambiar(definicion, aclaracion)
        self.esperar_hasta(b["fin"])

        # Bloque 4 — IA: las tablas de cada nodo.
        b = self.iniciar_bloque(4)
        grupo = red_alarma_con_tablas()
        red_final, tablas = grupo[0], grupo[1]
        self.play(FadeOut(aclaracion), ReplacementTransform(red, red_final), run_time=1.2)
        red = red_final
        piezas = tablas_orden = list(tablas)  # P(Robo), P(Terremoto), alarma, llamadas
        self.en(b, "Robo y Terremoto no tienen padres")
        self.play(FadeIn(piezas[0]), red.estados(robo="activo"))
        self.en(b, "Un terremoto")
        self.play(FadeIn(piezas[1]), red.estados(robo="normal", terremoto="activo"))
        self.en(b, "La alarma depende de ambos")
        self.play(FadeIn(piezas[2]), red.estados(terremoto="normal", alarma="activo"))
        self.en(b, "Camilo oye la alarma")
        self.play(FadeIn(piezas[3]), red.estados(alarma="normal", camilo="activo", isabel="activo"))
        self.esperar_hasta(b["fin"])
        self.play(red.restablecer())

        # Bloque 5 — Profesora: lo que no modelamos va en los números.
        b = self.iniciar_bloque(5)
        filas_llamadas = tablas_orden[3].get_rows()
        marco = SurroundingRectangle(VGroup(*filas_llamadas[1:]), color=RESALTADO, buff=0.1)
        marco.permite_solape = True
        self.play(Create(marco), red.estados(camilo="activo", isabel="activo"))
        self.esperar_hasta(b["fin"])
        self.play(FadeOut(marco), red.restablecer())

        # Bloque 6 — Analista: 10 números contra 31.
        b = self.iniciar_bloque(6)
        cuenta = tabla_formulas([
            [r"\text{Red bayesiana:}", r"1 + 1 + 4 + 2 + 2 = 10 \text{ números}"],
            [r"\text{Tabla conjunta:}", r"31 \text{ números}"],
        ], tam=44, alineacion="rl")
        espacio = ALTO_UTIL - cuenta.height - SEPARACION * 2
        destino = grupo.copy()
        ajustar(destino, alto=espacio).to_edge(UP, buff=MARGEN)
        cuenta.next_to(destino, DOWN, buff=SEPARACION * 2)
        self.play(
            Transform(red, destino[0]),
            *(Transform(pieza, meta) for pieza, meta in zip(piezas, destino[1])),
        )
        self.play(FadeIn(cuenta.filas[0]))
        self.play(cuenta.filas[0][1].animate.set_color(RESALTADO))
        self.en(b, "La tabla completa")
        self.play(FadeIn(cuenta.filas[1]))
        self.terminar()
