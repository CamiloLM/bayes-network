"""Escena 6 — Inferencia exacta: de dónde sale el 28,4 %."""

from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.style import *


def radio() -> VGroup:
    cuerpo = RoundedRectangle(width=3.2, height=1.9, corner_radius=0.2, color=TEXTO, stroke_width=3)
    parlante = VGroup(*(Circle(radius=r, color=TEXTO_SECUNDARIO, stroke_width=2) for r in (0.55, 0.35, 0.15)))
    parlante.move_to(cuerpo.get_left() + RIGHT * 0.9)
    dial = VGroup(*(Line(UP * 0.25, DOWN * 0.25, color=TEXTO_SECUNDARIO, stroke_width=2).shift(RIGHT * 0.15 * i)
                    for i in range(8))).move_to(cuerpo.get_right() + LEFT * 0.95 + UP * 0.2)
    perilla = Circle(radius=0.15, color=TEXTO, stroke_width=2).move_to(cuerpo.get_right() + LEFT * 0.95 + DOWN * 0.45)
    antena = Line(cuerpo.get_top() + RIGHT * 0.9, cuerpo.get_top() + RIGHT * 1.5 + UP * 1.0, color=TEXTO, stroke_width=3)
    return VGroup(cuerpo, parlante, dial, perilla, antena)


class Escena06(EscenaNarrada):
    numero = 6

    def construct(self):
        # Bloque 0 — Narrador: diez números.
        b = self.iniciar_bloque(0)
        grupo = red_alarma_con_tablas()
        red, tablas = grupo[0], grupo[1]
        self.play(FadeIn(grupo), run_time=1.2)
        self.en(b, "Diez números")
        self.play(Indicate(tablas, color=RESALTADO, scale_factor=1.03))
        self.esperar_hasta(b["fin"])

        # Bloque 1 — Profesora: consulta, evidencia y ocultas.
        b = self.iniciar_bloque(1)
        panel = VGroup(
            texto("Consulta:  Robo", TAM_CUERPO, RESALTADO, t2c={"Consulta:": TEXTO_SECUNDARIO}),
            texto("Evidencia:  Llama Camilo = V, Llama Isabel = V", TAM_CUERPO, NODO,
                  t2c={"Evidencia:": TEXTO_SECUNDARIO}),
            texto("Variables ocultas:  Terremoto, Alarma", TAM_CUERPO, TEXTO,
                  t2c={"Variables ocultas:": TEXTO_SECUNDARIO}),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        red_destino = red.copy().scale_to_fit_height(ALTO_UTIL - panel.height - 0.8)
        VGroup(red_destino, panel).arrange(DOWN, buff=0.8)
        ajustar(VGroup(red_destino, panel)).move_to(ORIGIN)
        self.play(FadeOut(tablas), Transform(red, red_destino))
        self.consolidar(red)
        self.en(b, "Lo que queremos saber")
        self.play(FadeIn(panel[0]), red.estados(robo="activo"))
        self.en(b, "Lo que sabemos")
        self.play(FadeIn(panel[1]), red.estados(camilo="evidencia", isabel="evidencia"))
        self.en(b, "Y lo que no sabemos")
        self.play(FadeIn(panel[2]), red.estados(terremoto="inactivo", alarma="inactivo"))
        self.esperar_hasta(b["fin"])

        # Bloque 2 — Analista: la fórmula de enumeración.
        b = self.iniciar_bloque(2)
        self.limpiar()
        enumeracion = MathTex(
            r"P(\text{Robo} \mid c, i) =", r"\alpha", r"\, P(\text{Robo})", r"\sum_t", r"P(t)", r"\sum_a",
            r"P(a \mid \text{Robo}, t)\, P(c \mid a)\, P(i \mid a)",
            font_size=48, color=TEXTO,
        )
        enumeracion[1].set_color(NODO)
        enumeracion[3].set_color(RESALTADO)
        enumeracion[5].set_color(RESALTADO)
        leyenda = VGroup(
            VGroup(formula(r"\Sigma", 40, RESALTADO), texto("= sumar sobre lo que no sabemos", TAM_CUERPO)),
            VGroup(formula(r"\alpha", 40, NODO), texto("= normalizar al final para que todo sume 1", TAM_CUERPO)),
        )
        for fila in leyenda:
            fila.arrange(RIGHT, buff=0.25)
        leyenda.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        bloque = VGroup(enumeracion, leyenda).arrange(DOWN, buff=1.0)
        ajustar(bloque).move_to(ORIGIN)
        self.play(Write(enumeracion), run_time=2)
        self.en(b, "sumamos sobre todas")
        self.play(FadeIn(leyenda[0]))
        self.en(b, "Al final, normalizamos")
        self.play(FadeIn(leyenda[1]))
        self.esperar_hasta(b["fin"])

        # Bloque 3 — IA: paso 1.
        b = self.iniciar_bloque(3)
        self.limpiar()
        paso1 = bloque_calculo("Paso 1 — ¿Qué tan probable es que llamen los dos?", [
            tabla_formulas([
                [r"\text{Si la alarma sonó:}", r"0{,}90 \times 0{,}70 = 0{,}63"],
                [r"\text{Si la alarma no sonó:}", r"0{,}05 \times 0{,}01 = 0{,}0005"],
            ], tam=44),
        ])
        ajustar(paso1).move_to(ORIGIN)
        filas = paso1[1][0].filas
        self.play(FadeIn(paso1[0]))
        self.play(FadeIn(filas[0]))
        self.en(b, "Si no sonó")
        self.play(FadeIn(filas[1]))
        self.esperar_hasta(b["fin"])

        # Bloques 4 y 5 — IA: pasos 2 y 3 (mundo con y sin robo).
        mundos = [
            ("Paso 2 — Mundo «SÍ hubo robo»", [
                [r"\text{Con terremoto:}", r"0{,}95 \times 0{,}63 + 0{,}05 \times 0{,}0005 = 0{,}598525",
                 r"\times\, 0{,}002", r"\rightarrow 0{,}0011971"],
                [r"\text{Sin terremoto:}", r"0{,}94 \times 0{,}63 + 0{,}06 \times 0{,}0005 = 0{,}59223",
                 r"\times\, 0{,}998", r"\rightarrow 0{,}5910455"],
                ["", "", r"\text{Suma}", r"= 0{,}5922426"],
                ["", "", r"\times P(\text{Robo}) = 0{,}001", r"\rightarrow 0{,}00059224"],
            ]),
            ("Paso 3 — Mundo «NO hubo robo»", [
                [r"\text{Con terremoto:}", r"0{,}29 \times 0{,}63 + 0{,}71 \times 0{,}0005 = 0{,}183055",
                 r"\times\, 0{,}002", r"\rightarrow 0{,}0003661"],
                [r"\text{Sin terremoto:}", r"0{,}001 \times 0{,}63 + 0{,}999 \times 0{,}0005 = 0{,}0011295",
                 r"\times\, 0{,}998", r"\rightarrow 0{,}0011272"],
                ["", "", r"\text{Suma}", r"= 0{,}0014934"],
                ["", "", r"\times P(\neg\text{Robo}) = 0{,}999", r"\rightarrow 0{,}0014919"],
            ]),
        ]
        for i, (encabezado, filas_tex) in enumerate(mundos):
            b = self.iniciar_bloque(4 + i)
            self.limpiar()
            tabla = tabla_formulas(filas_tex, tam=36, alineacion="rlrl", buff=(0.35, 0.4))
            paso = bloque_calculo(encabezado, [tabla])
            ajustar(paso).move_to(ORIGIN)
            self.play(FadeIn(paso[0]))
            if i == 0:
                self.revelar(tabla.filas[:3], self.momento(b, "Considero"), self.momento(b, "Multiplico, sumo"))
                self.en(b, "multiplico por la probabilidad previa")
                self.play(FadeIn(tabla.filas[3]))
            else:
                self.revelar(tabla.filas, b["inicio"] + 0.8, b["fin"])
            self.play(tabla.filas[3][3].animate.set_color(RESALTADO))
            self.esperar_hasta(b["fin"])

        # Bloque 6 — Analista: paso 4, normalizar.
        b = self.iniciar_bloque(6)
        self.limpiar()
        tabla = tabla_formulas([
            [r"\text{Robo:}", r"0{,}00059224"],
            [r"\text{No robo:}", r"0{,}0014919"],
            [r"\text{Total:}", r"0{,}0020841"],
        ], tam=40, alineacion="rl")
        resultado = tabla_formulas([
            [r"P(\text{Robo} \mid c, i)", r"= 0{,}00059224 / 0{,}0020841 \approx 0{,}284", r"\rightarrow 28{,}4\,\%"],
            [r"P(\neg\text{Robo} \mid c, i)", r"\approx 0{,}716", r"\rightarrow 71{,}6\,\%"],
        ], tam=40, alineacion="rll")
        paso = bloque_calculo("Paso 4 — Normalizar", [tabla, resultado])
        ajustar(paso).move_to(ORIGIN)
        self.play(FadeIn(paso[0]), FadeIn(tabla))
        self.en(b, "Así que los dividimos")
        self.play(FadeIn(resultado.filas[0]))
        self.play(resultado.filas[0].animate.set_color(RESALTADO))
        self.en(b, "Setenta y uno")
        self.play(FadeIn(resultado.filas[1]))
        self.esperar_hasta(b["fin"])

        # Bloque 7 — Estudiante. Bloque 8 — IA: solo Camilo.
        self.iniciar_bloque(7)
        b = self.iniciar_bloque(8)
        self.limpiar()
        explicacion = texto("Solo evidencia de Camilo: el término de Isabel suma 1 y desaparece.",
                            TAM_CUERPO, TEXTO_SECUNDARIO)
        comparacion = tabla_formulas([
            [r"P(\text{Robo} \mid c)", r"\approx 0{,}016", r"\rightarrow 1{,}6\,\%"],
            [r"P(\text{Robo} \mid c, i)", r"\approx 0{,}284", r"\rightarrow 28{,}4\,\%"],
        ], tam=52, alineacion="lll", buff=(0.5, 0.6))
        multiplica = titulo("× más de 17", TAM_SUBTITULO, RESALTADO)
        bloque = VGroup(explicacion, comparacion, multiplica).arrange(DOWN, buff=0.8)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(explicacion))
        self.en(b, "Resultado: uno coma seis")
        self.play(FadeIn(comparacion.filas[0]))
        self.en(b, "Pero cuando dos testigos")
        self.play(FadeIn(comparacion.filas[1]))
        self.play(FadeIn(multiplica, scale=1.2))
        self.esperar_hasta(b["fin"])

        # Bloque 9 — Narrador: la radio.
        b = self.iniciar_bloque(9)
        self.limpiar()
        aparato = radio()
        noticia = texto("«Última hora: pequeño temblor en tu barrio.»", TAM_CUERPO, RESALTADO)
        VGroup(aparato, noticia).arrange(DOWN, buff=0.8).move_to(ORIGIN)
        self.play(FadeIn(aparato))
        self.play(Wiggle(aparato))
        self.en(b, "Hubo un pequeño temblor")
        self.play(Write(noticia))
        self.esperar_hasta(b["fin"])

        # Bloque 10 — IA: con el terremoto como evidencia.
        b = self.iniciar_bloque(10)
        self.limpiar()
        red = red_alarma()
        red.aplicar_estados(camilo="evidencia", isabel="evidencia", terremoto="evidencia")
        filas = tabla_formulas([
            [r"P(\text{Alarma sonó} \mid c, i)", r"\approx 76\,\%"],
            [r"P(\text{Robo} \mid c, i)", r"\approx 28{,}4\,\%"],
            [r"P(\text{Robo} \mid c, i, \text{Terremoto})", r"\approx 0{,}33\,\%"],
        ], tam=40, alineacion="ll", buff=(0.4, 0.45))
        compiten = texto("Robo y Terremoto compiten por explicar la misma alarma.", TAM_CUERPO, RESALTADO)
        arriba = VGroup(red, filas).arrange(RIGHT, buff=1.0)
        ajustar(arriba, alto=ALTO_UTIL - compiten.height - 0.8)
        todo = VGroup(arriba, compiten).arrange(DOWN, buff=0.8)
        ajustar(todo).move_to(ORIGIN)
        self.play(FadeIn(red), FadeIn(filas.filas[0]))
        self.en(b, "Pero la probabilidad de robo")
        self.play(FadeIn(filas.filas[1]))
        self.play(FadeIn(filas.filas[2]), red.estados(robo="inactivo"))
        self.play(filas.filas[2].animate.set_color(RESALTADO))
        self.en(b, "El temblor ya explica")
        self.play(FadeIn(compiten))
        self.esperar_hasta(b["fin"])

        # Bloque 11 — Profesora: explicación alternativa.
        b = self.iniciar_bloque(11)
        nombre = titulo("Explicación alternativa (explaining away)", TAM_SUBTITULO, RESALTADO).move_to(compiten)
        ajustar(nombre)
        self.cambiar(compiten, nombre)
        self.terminar()
