"""Escena 7 — No calcules dos veces lo mismo."""

from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.style import *


def arbol_enumeracion() -> tuple[VGroup, list[VGroup]]:
    """Robo -> Terremoto (V/F) -> Alarma (V/F); devuelve el árbol y las hojas."""
    raiz = Nodo("Robo").move_to(UP * 2.6)
    niveles = [("Robo", raiz)]
    lineas = VGroup()
    etiquetas = VGroup()
    hojas = []

    def rama(padre, destino, valor):
        linea = Line(padre.get_bottom(), destino.get_top(), color=FLECHA, stroke_width=3)
        etiqueta = texto(valor, TAM_PEQUENO - 4, TEXTO_SECUNDARIO).next_to(linea.get_center(), LEFT, buff=0.1)
        lineas.add(linea)
        etiquetas.add(etiqueta)

    nodos = VGroup(raiz)
    for i, robo in enumerate("VF"):
        t = Nodo("Terremoto").scale(0.8).move_to([(-3.4 if i == 0 else 3.4), 1.0, 0])
        rama(raiz, t, robo)
        nodos.add(t)
        for j, terr in enumerate("VF"):
            a = Nodo("Alarma").scale(0.8).move_to([t.get_x() + (-1.7 if j == 0 else 1.7), -0.6, 0])
            rama(t, a, terr)
            nodos.add(a)
            for k, alarma in enumerate("VF"):
                valor = "0,63" if alarma == "V" else "0,0005"
                hoja = titulo(valor, TAM_PEQUENO - 2, RESALTADO)
                hoja.move_to([a.get_x() + (-0.8 if k == 0 else 0.8), -2.3, 0])
                marco = SurroundingRectangle(hoja, color=RESALTADO, buff=0.08, corner_radius=0.08, stroke_width=2)
                rama(a, VGroup(marco, hoja), alarma)
                hojas.append(VGroup(marco, hoja))
    arbol = VGroup(lineas, etiquetas, nodos, *hojas)
    # Las piezas del árbol aparecen por separado pero forman un solo diagrama.
    for pieza in (lineas, etiquetas, *hojas):
        pieza.permite_solape = True
    return arbol, hojas


class Escena07(EscenaNarrada):
    numero = 7

    def construct(self):
        # Bloque 0 — Analista: el árbol repite cálculos.
        b = self.iniciar_bloque(0)
        arbol, hojas = arbol_enumeracion()
        contador = texto("0,63 calculado 4 veces  ·  0,0005 calculado 4 veces", TAM_CUERPO, RESALTADO)
        ajustar(arbol, alto=ALTO_UTIL - contador.height - 0.6)
        VGroup(arbol, contador).arrange(DOWN, buff=0.6).move_to(ORIGIN)
        self.play(FadeIn(arbol[2]), Create(arbol[0]), FadeIn(arbol[1]), run_time=2)
        self.en(b, "aparece en cada combinación")
        self.play(LaggedStart(*(FadeIn(h) for h in hojas), lag_ratio=0.2), run_time=2)
        self.en(b, "Lo calculamos cuatro veces")
        self.play(FadeIn(contador))
        self.consolidar(arbol)
        self.esperar_hasta(b["fin"])

        # Bloque 1 — Profesora: eliminación de variables.
        b = self.iniciar_bloque(1)
        self.limpiar()
        cabecera = titulo("Eliminación de variables", TAM_SUBTITULO, RESALTADO)
        pasos = tabla_formulas([
            [r"\text{\textcircled{1} Factor de las llamadas (una sola vez):}",
             r"f_1(\text{Alarma}) = \langle 0{,}63 ;\ 0{,}0005 \rangle"],
            [r"\text{\textcircled{2} Sumar fuera Alarma:}",
             r"f_2(\text{Robo}, \text{Terremoto}) = \langle 0{,}598525 ;\ 0{,}59223 ;\ 0{,}183055 ;\ 0{,}0011295 \rangle"],
            [r"\text{\textcircled{3} Sumar fuera Terremoto:}",
             r"f_3(\text{Robo}) = \langle 0{,}592243 ;\ 0{,}001493 \rangle"],
            [r"\text{\textcircled{4} Multiplicar por } P(\text{Robo}):",
             r"\langle 0{,}00059224 ;\ 0{,}0014919 \rangle"],
            [r"\text{\textcircled{5} Normalizar:}", r"\langle 0{,}284 ;\ 0{,}716 \rangle"],
        ], tam=34, alineacion="rl", buff=(0.4, 0.5))
        bloque = VGroup(cabecera, pasos).arrange(DOWN, buff=0.7)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(cabecera))
        marcas = ["Primero calcula", "Luego elimina la alarma", "Luego elimina el terremoto",
                  "Multiplicamos por la probabilidad", "y llegamos al mismo"]
        for fila, frase in zip(pasos.filas, marcas):
            self.en(b, frase)
            self.play(FadeIn(fila))
        self.play(pasos.filas[4].animate.set_color(RESALTADO))
        self.en(b, "Misma respuesta")
        lema = texto("Misma respuesta. Menos trabajo.", TAM_CUERPO, RESALTADO)
        ajustar(VGroup(bloque, lema).arrange(DOWN, buff=0.5)).move_to(ORIGIN)
        self.play(FadeIn(lema))
        self.esperar_hasta(b["fin"])

        # Bloque 2 — IA (se mantiene el fondo).
        self.iniciar_bloque(2)

        # Bloque 3 — Analista: poliárbol contra red densa.
        b = self.iniciar_bloque(3)
        self.limpiar()
        poliarbol = RedBayesiana(
            {k: (k, p) for k, p in {"A": (-1.2, 1.2), "B": (1.2, 1.2), "C": (0, 0), "D": (-1.2, -1.2),
                                     "E": (1.2, -1.2)}.items()},
            [("A", "C"), ("B", "C"), ("C", "D"), ("C", "E")],
        )
        densa = RedBayesiana(
            {k: (k, p) for k, p in {"A": (-1.2, 1.2), "B": (1.2, 1.2), "C": (0, 0), "D": (-1.2, -1.2),
                                     "E": (1.2, -1.2)}.items()},
            [("A", "C"), ("B", "C"), ("C", "D"), ("C", "E"), ("A", "B"), ("A", "D"), ("B", "E"), ("D", "E")],
        )
        izq = VGroup(poliarbol, parrafo("Poliárbol\n(como máximo un camino entre dos nodos)", TAM_PEQUENO),
                     texto("costo lineal ✓", TAM_CUERPO, POSITIVO)).arrange(DOWN, buff=0.45)
        der = VGroup(densa, parrafo("Red densamente conectada\n(muchos caminos entre nodos)", TAM_PEQUENO),
                     texto("costo que puede explotar ✗", TAM_CUERPO, NEGATIVO)).arrange(DOWN, buff=0.45)
        comparacion = VGroup(izq, der).arrange(RIGHT, buff=2.0, aligned_edge=UP)
        ajustar(comparacion).move_to(ORIGIN)
        self.play(FadeIn(izq))
        self.en(b, "Pero no todas las redes")
        self.play(FadeIn(der))
        self.terminar()
