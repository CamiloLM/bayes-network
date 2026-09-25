"""Escena 11 — Conclusiones y recomendaciones."""

from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.style import *


def pilar(numero: str, nombre: str, detalle: Mobject) -> VGroup:
    cabecera = titulo(f"{numero}. {nombre}", TAM_CUERPO, RESALTADO)
    contenido = VGroup(cabecera, detalle).arrange(DOWN, buff=0.4)
    marco = RoundedRectangle(width=3.9, height=3.0, corner_radius=0.2, color=NODO, stroke_width=2.5,
                             fill_color=NODO, fill_opacity=0.06)
    ajustar(contenido, ancho=marco.width - 0.5, alto=marco.height - 0.5)
    return VGroup(marco, contenido.move_to(marco))


class Escena11(EscenaNarrada):
    numero = 11

    def construct(self):
        # Bloque 0 — Narrador: tres pilares.
        b = self.iniciar_bloque(0)
        cabecera = titulo("Conclusiones y recomendaciones", TAM_SUBTITULO + 4).to_edge(UP, buff=MARGEN)
        pilares = VGroup(
            pilar("1", "REPRESENTAR", VGroup(texto("red bayesiana", TAM_PEQUENO),
                                             formula(r"2^n \;\rightarrow\; n \cdot 2^k", 40)).arrange(DOWN, buff=0.3)),
            pilar("2", "INFERIR", parrafo("enumeración,\neliminación de variables,\nmuestreo", TAM_PEQUENO)),
            pilar("3", "INTERVENIR", parrafo("operador do\ny grafo mutilado", TAM_PEQUENO)),
        ).arrange(RIGHT, buff=0.5)
        pilares.scale_to_fit_width(ANCHO_UTIL)
        ajustar(pilares, alto=ALTO_UTIL - cabecera.height - 1.0).move_to(DOWN * 0.4)
        self.play(FadeIn(cabecera))
        for p, frase in zip(pilares, ["Representar:", "Inferir:", "Intervenir:"]):
            self.en(b, frase)
            self.play(FadeIn(p, shift=UP * 0.2))
        self.esperar_hasta(b["fin"])

        # Bloque 1 — Estudiante (se mantiene).
        self.iniciar_bloque(1)

        # Bloque 2 — IA: cada dato nuevo mueve el número.
        b = self.iniciar_bloque(2)
        self.play(FadeOut(pilares))
        numeros = VGroup(*(
            VGroup(titulo(valor, TAM_TITULO, RESALTADO), texto(etiqueta, TAM_PEQUENO, TEXTO_SECUNDARIO))
            .arrange(DOWN, buff=0.3)
            for valor, etiqueta in [("1,6 %", "una llamada"), ("28,4 %", "dos llamadas"),
                                    ("0,33 %", "dos llamadas + temblor")]
        )).arrange(RIGHT, buff=1.4)
        ajustar(numeros).move_to(ORIGIN)
        for n, frase in zip(numeros, ["Uno coma seis", "Veintiocho con dos", "Un tercio"]):
            self.en(b, frase)
            self.play(FadeIn(n, scale=1.1))
        self.en(b, "Cada dato nuevo")
        lema = texto("Cada dato nuevo mueve el número.", TAM_CUERPO).next_to(numeros, DOWN, buff=0.9)
        self.play(FadeIn(lema))
        self.esperar_hasta(b["fin"])

        # Bloque 3 — Profesora: recomendaciones.
        b = self.iniciar_bloque(3)
        self.limpiar()
        cabecera = titulo("Recomendaciones", TAM_SUBTITULO, RESALTADO)
        lista = lista_puntos([
            "Construir la red en orden causal: de causas a efectos.",
            "Estimar las tablas con datos, validarlas con expertos y actualizarlas.",
            "Elegir el algoritmo según la estructura: exacto en redes pequeñas\n"
            "o poliárboles; muestreo en redes grandes.",
            "Antes de actuar, preguntar: ¿es una observación o una intervención?",
            "Comunicar probabilidades, no certezas.",
        ], tam=TAM_PEQUENO + 2)
        cierre = texto("No se trata de tener certeza, sino de decidir mejor con lo que sabemos hoy.",
                       TAM_PEQUENO + 2, NODO)
        bloque = VGroup(cabecera, lista, cierre).arrange(DOWN, buff=0.6)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(cabecera))
        marcas = ["Construyan la red", "Estimen las tablas", "Elijan el algoritmo", "Antes de tomar",
                  "Y comuniquen probabilidades"]
        for linea, frase in zip(lista, marcas):
            self.en(b, frase)
            self.play(FadeIn(linea))
        self.en(b, "No se trata de tener certeza")
        self.play(FadeIn(cierre))
        self.esperar_hasta(b["fin"])

        # Bloques 4 y 5 — IA y Estudiante: las dos llamadas.
        self.iniciar_bloque(4)
        self.limpiar()
        izquierda = VGroup(celular("Camilo llamando..."),
                           formula(r"P(\text{Robo} \mid \text{Camilo}) = 1{,}6\,\%", 44)).arrange(DOWN, buff=0.6)
        derecha = VGroup(celular("Isabel llamando..."),
                         formula(r"P(\text{Robo} \mid \text{Camilo}, \text{Isabel}) = 28{,}4\,\%", 44, RESALTADO)
                         ).arrange(DOWN, buff=0.6)
        ajustar(VGroup(izquierda, derecha).arrange(RIGHT, buff=1.5)).move_to(ORIGIN)
        self.play(FadeIn(izquierda[0]), run_time=0.6)
        self.play(Wiggle(izquierda[0]), FadeIn(izquierda[1]), run_time=1)
        self.iniciar_bloque(5)
        self.play(FadeIn(derecha[0]), FadeIn(derecha[1]), run_time=0.6)
        self.play(Wiggle(derecha[0]), run_time=0.8)

        # Bloque 6 — Narrador: el cierre.
        b = self.iniciar_bloque(6)
        self.limpiar()
        cierre = texto("Representar · Inferir · Actualizar · Intervenir", TAM_SUBTITULO)
        ajustar(cierre)
        self.play(FadeIn(cierre), run_time=2.5)
        self.terminar(1.0)
        self.play(FadeOut(cierre), run_time=1)
