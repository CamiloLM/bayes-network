"""Escena 9 — Observar no es lo mismo que intervenir."""

from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.style import *


class Escena09(EscenaNarrada):
    numero = 9

    def red_con_titulo(self, contenido: str, alto_red: float = 3.0) -> tuple[Text, RedBayesiana]:
        cabecera = titulo(contenido, TAM_SUBTITULO, RESALTADO)
        ajustar(cabecera).to_edge(UP, buff=MARGEN)
        red = red_aspersor(escala=0.8).scale_to_fit_height(alto_red).next_to(cabecera, DOWN, buff=0.5)
        return cabecera, red

    def debajo(self, mob: Mobject, arriba: Mobject, buff: float = 0.5) -> Mobject:
        """Ubica `mob` bajo `arriba`, reduciéndolo para que quepa hasta el margen inferior."""
        alto = arriba.get_bottom()[1] - buff - (-config.frame_height / 2 + MARGEN)
        return ajustar(mob, alto=alto).next_to(arriba, DOWN, buff=buff)

    def construct(self):
        # Bloque 0 — Narrador: la red del aspersor.
        self.iniciar_bloque(0)
        grupo = red_aspersor_con_tablas()
        self.play(FadeIn(grupo), run_time=1.2)

        # Bloque 1 — Narrador: caso 1, observar.
        self.iniciar_bloque(1)
        self.limpiar()
        cabecera, red = self.red_con_titulo("CASO 1 — OBSERVAR")
        self.play(FadeIn(cabecera), FadeIn(red))
        self.play(red.estados(aspersor="evidencia"))

        # Bloque 2 — IA: Bayes, la información viaja hacia atrás.
        b = self.iniciar_bloque(2)
        calculos = tabla_formulas([
            [r"P(\text{Aspersor})", r"= 0{,}5 \times 0{,}10 + 0{,}5 \times 0{,}50 = 0{,}30", ""],
            [r"P(\text{Nublado} \mid \text{Aspersor})", r"= (0{,}10 \times 0{,}5) / 0{,}30 \approx 0{,}167",
             r"\rightarrow 16{,}7\,\%"],
            [r"P(\text{Lluvia} \mid \text{Aspersor})", r"= 0{,}80 \times 0{,}167 + 0{,}20 \times 0{,}833 = 0{,}30",
             r"\rightarrow 30\,\%"],
            [r"P(\text{Césped} \mid \text{Aspersor})", r"= 0{,}99 \times 0{,}30 + 0{,}90 \times 0{,}70 = 0{,}927",
             r"\rightarrow 92{,}7\,\%"],
        ], tam=34, alineacion="rll", buff=(0.25, 0.3))
        self.debajo(calculos, red)
        # Pulso de información: de Aspersor hacia Nublado (contra la flecha) y de Nublado a Lluvia.
        pulso = Dot(radius=0.12, color=RESALTADO)
        pulso.permite_solape = True
        atras = Line(red.nodos["aspersor"].get_center(), red.nodos["nublado"].get_center())
        adelante = Line(red.nodos["nublado"].get_center(), red.nodos["lluvia"].get_center())
        self.play(FadeIn(calculos.filas[0]))
        self.en(b, "verlo encendido es una pista")
        pulso.move_to(atras.get_start())
        self.add(pulso)
        self.play(MoveAlongPath(pulso, atras), run_time=1.2)
        self.play(FadeIn(calculos.filas[1]), red.estados(nublado="activo"))
        self.en(b, "Y como en los días despejados")
        self.play(MoveAlongPath(pulso, adelante), run_time=1.2)
        self.play(FadeIn(calculos.filas[2]), red.estados(lluvia="activo"))
        self.remove(pulso)
        self.en(b, "El mismo treinta por ciento")
        self.play(Indicate(calculos.filas[2], color=RESALTADO))
        self.en(b, "La información viajó")
        self.play(FadeIn(calculos.filas[3]))
        self.esperar_hasta(b["fin"])

        # Bloque 3 — Narrador: caso 2, intervenir.
        self.iniciar_bloque(3)
        self.limpiar()
        cabecera, red = self.red_con_titulo("CASO 2 — INTERVENIR:  do(Aspersor = encendido)")
        self.play(FadeIn(cabecera), FadeIn(red))

        # Bloque 4 — Estudiante (se mantiene).
        self.iniciar_bloque(4)

        # Bloque 5 — Analista: tijeras y grafo mutilado.
        b = self.iniciar_bloque(5)
        original = MathTex(r"P(n, a, l, c) = P(n)\, ", r"P(a \mid n)", r"\, P(l \mid n)\, P(c \mid a, l)",
                           font_size=40, color=TEXTO)
        mutilado = MathTex(r"P(n, l, c \mid do(a)) = P(n)\, ", r"P(a \mid n)", r"\, P(l \mid n)\, P(c \mid a, l)",
                           font_size=40, color=TEXTO)
        formulas = VGroup(
            VGroup(texto("Distribución original:", TAM_PEQUENO, TEXTO_SECUNDARIO), original).arrange(RIGHT, buff=0.3),
            VGroup(texto("Grafo mutilado:", TAM_PEQUENO, TEXTO_SECUNDARIO), mutilado).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        self.debajo(formulas, red)
        self.en(b, "Esta es una red causal")
        self.play(red.estados(aspersor="evidencia"))
        self.en(b, "Tomamos la misma factorización")
        self.play(FadeIn(formulas[0]))
        self.en(b, "cortamos la flecha")
        flecha = red.flechas[("nublado", "aspersor")]
        corte = Line(LEFT * 0.35, RIGHT * 0.35, color=NEGATIVO, stroke_width=6).rotate(PI / 4).move_to(flecha)
        corte.permite_solape = True
        tijeras = texto("✂", TAM_SUBTITULO, NEGATIVO).next_to(flecha, LEFT, buff=0.15)
        tijeras.permite_solape = True
        self.play(FadeIn(tijeras), Create(corte))
        self.play(FadeOut(tijeras), FadeOut(corte), flecha.animate.set_opacity(0.12))
        self.consolidar(red)
        self.en(b, "En la fórmula")
        self.play(FadeIn(formulas[1]))
        tachon = Cross(mutilado[1], stroke_color=NEGATIVO, stroke_width=5)
        tachon.permite_solape = True
        self.play(Create(tachon))
        self.en(b, "A esto se le llama")
        self.play(FadeOut(tachon), mutilado[1].animate.set_opacity(0.15))
        self.esperar_hasta(b["fin"])

        # Bloque 6 — IA: recalcular con el grafo cortado.
        b = self.iniciar_bloque(6)
        calculos = tabla_formulas([
            [r"P(\text{Nublado} \mid do(\text{Aspersor}))", r"= 0{,}5", r"\rightarrow 50\,\%"],
            [r"P(\text{Lluvia} \mid do(\text{Aspersor}))", r"= 0{,}5 \times 0{,}80 + 0{,}5 \times 0{,}20 = 0{,}50",
             r"\rightarrow 50\,\%"],
            [r"P(\text{Césped} \mid do(\text{Aspersor}))", r"= 0{,}99 \times 0{,}50 + 0{,}90 \times 0{,}50 = 0{,}945",
             r"\rightarrow 94{,}5\,\%"],
        ], tam=34, alineacion="rll", buff=(0.25, 0.3))
        self.debajo(calculos, red)
        self.play(FadeOut(formulas))
        self.revelar(calculos.filas, b["inicio"] + 1, self.momento(b, "Encender el aspersor"))
        self.esperar_hasta(b["fin"])

        # Bloque 7 — Narrador: observar contra intervenir.
        b = self.iniciar_bloque(7)
        self.limpiar()
        tabla = tabla_cpt(
            ["", "OBSERVAR", "INTERVENIR"],
            [["", "(veo el aspersor)", "(lo enciendo yo)"],
             ["Nublado", "16,7 %", "50 %"], ["Lluvia", "30 %", "50 %"], ["Césped mojado", "92,7 %", "94,5 %"]],
            tam=32,
        )
        tabla.scale(1.3)
        ajustar(tabla).move_to(UP * 0.4)
        self.play(FadeIn(tabla), run_time=1.2)
        self.en(b, "La diferencia no está")
        lema = texto("La diferencia está en cómo llegó el mundo a ese estado.", TAM_CUERPO, RESALTADO)
        lema.next_to(tabla, DOWN, buff=0.6)
        self.play(FadeIn(lema))
        self.esperar_hasta(b["fin"])

        # Bloque 8 — Analista: solo cambian los descendientes.
        b = self.iniciar_bloque(8)
        self.limpiar()
        red = red_aspersor(escala=0.9)
        red.aplicar_estados(aspersor="evidencia")
        red.flechas[("nublado", "aspersor")].set_opacity(0.12)
        cambios = VGroup(
            texto("Nublado  →  no cambia (50 %)", TAM_CUERPO, TEXTO_SECUNDARIO),
            texto("Lluvia  →  no cambia (50 %)", TAM_CUERPO, TEXTO_SECUNDARIO),
            texto("Césped  →  cambia (94,5 %)", TAM_CUERPO, RESALTADO),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        cabecera = titulo("Solo cambian los descendientes del aspersor", TAM_SUBTITULO)
        cuerpo = VGroup(red, cambios).arrange(RIGHT, buff=1.2)
        todo = VGroup(cabecera, cuerpo).arrange(DOWN, buff=0.8)
        ajustar(todo).move_to(ORIGIN)
        self.play(FadeIn(cabecera), FadeIn(red))
        self.play(FadeIn(cambios[0]), FadeIn(cambios[1]))
        self.play(FadeIn(cambios[2]), red.estados(cesped="activo"))
        self.esperar_hasta(b["fin"])

        # Bloque 9 — Profesora: fórmula de ajuste.
        b = self.iniciar_bloque(9)
        self.limpiar()
        cabecera = parrafo("Fórmula de ajuste (ecuación 13.20 del libro)\npromediar sobre los padres del aspersor",
                           TAM_CUERPO, RESALTADO)
        lineas = tabla_formulas([
            [r"P(\text{Césped} \mid do(\text{Aspersor}))", r"= \textstyle\sum_n P(\text{Césped} \mid \text{Aspersor}, n)\, P(n)"],
            [r"P(\text{Césped} \mid \text{Aspersor}, \text{nublado})", r"= 0{,}99 \times 0{,}80 + 0{,}90 \times 0{,}20 = 0{,}972"],
            [r"P(\text{Césped} \mid \text{Aspersor}, \text{despejado})", r"= 0{,}99 \times 0{,}20 + 0{,}90 \times 0{,}80 = 0{,}918"],
            ["", r"0{,}5 \times 0{,}972 + 0{,}5 \times 0{,}918 = 0{,}945 \;\checkmark"],
        ], tam=34, alineacion="rl", buff=(0.2, 0.4))
        bloque = VGroup(cabecera, lineas).arrange(DOWN, buff=0.7)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(cabecera))
        self.en(b, "Con una fórmula de ajuste")
        self.play(FadeIn(lineas.filas[0]))
        self.en(b, "Separamos días nublados")
        self.play(FadeIn(lineas.filas[1]), FadeIn(lineas.filas[2]))
        self.en(b, "Resultado")
        self.play(FadeIn(lineas.filas[3]), lineas.filas[3].animate.set_color(RESALTADO))
        self.esperar_hasta(b["fin"])

        # Bloque 10 — Estudiante (se mantiene).
        self.iniciar_bloque(10)

        # Bloque 11 — Analista: criterio de la puerta trasera.
        b = self.iniciar_bloque(11)
        self.limpiar()
        cabecera = titulo("Criterio de la puerta trasera (ecuación 13.21)", TAM_SUBTITULO, RESALTADO)
        camino = texto("Camino trasero:  Aspersor ← Nublado → Lluvia → Césped", TAM_CUERPO)
        cierre = texto("Si conocemos Lluvia, esa puerta queda cerrada.", TAM_CUERPO, NODO)
        lineas = tabla_formulas([
            [r"P(\text{Césped} \mid do(\text{Aspersor}))", r"= \textstyle\sum_l P(\text{Césped} \mid \text{Aspersor}, l)\, P(l)"],
            ["", r"= 0{,}99 \times 0{,}5 + 0{,}90 \times 0{,}5 = 0{,}945 \;\checkmark"],
        ], tam=36, alineacion="rl", buff=(0.2, 0.4))
        bloque = VGroup(cabecera, camino, cierre, lineas).arrange(DOWN, buff=0.6)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(cabecera))
        self.en(b, "hay una puerta trasera")
        self.play(FadeIn(camino))
        self.en(b, "basta con condicionar")
        self.play(FadeIn(cierre))
        self.en(b, "Promediamos")
        self.play(FadeIn(lineas.filas[0]))
        self.play(FadeIn(lineas.filas[1]), lineas.filas[1].animate.set_color(RESALTADO))
        self.esperar_hasta(b["fin"])

        # Bloque 12 — Profesora: un siglo de dogma.
        b = self.iniciar_bloque(12)
        self.limpiar()
        dogma = parrafo("La puerta trasera cuestiona un siglo de dogma estadístico:\n"
                        "«solo un ensayo controlado aleatorizado da información causal»", TAM_CUERPO, TEXTO_SECUNDARIO)
        dogma.shift(UP * 1.2)
        self.play(FadeIn(dogma))
        self.en(b, "Correlación no es causalidad")
        frase = titulo("Correlación no es causalidad.", TAM_TITULO - 8, RESALTADO).next_to(dogma, DOWN, buff=0.9)
        self.play(Write(frase))
        self.en(b, "Pero un buen modelo")
        remate = parrafo("Pero un buen modelo nos dice\ncuándo podemos pasar de una a la otra.", TAM_CUERPO)
        remate.next_to(frase, DOWN, buff=0.5)
        self.play(FadeIn(remate))
        self.terminar()
