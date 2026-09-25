"""Escena 2 — La explosión de datos."""

from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.style import *

VARIABLES = ["Robo", "Terremoto", "Alarma", "Llama Camilo", "Llama Isabel"]


class Escena02(EscenaNarrada):
    numero = 2

    def construct(self):
        # Bloque 0 — Analista: cinco variables V/F.
        b = self.iniciar_bloque(0)
        cabecera = titulo("Intentemos resolverlo a lo bruto", TAM_SUBTITULO).to_edge(UP, buff=MARGEN + 0.3)
        self.play(FadeIn(cabecera))
        columnas = VGroup()
        for nombre in VARIABLES:
            columnas.add(VGroup(Nodo(nombre), texto("V / F", TAM_CUERPO, TEXTO_SECUNDARIO)).arrange(DOWN, buff=0.35))
        columnas.arrange(RIGHT, buff=0.45)
        ajustar(columnas).move_to(ORIGIN)
        self.en(b, "cinco variables")
        self.revelar(list(columnas), self.momento(b, "Robo, Terremoto"), self.momento(b, "Cada una puede"))
        self.en(b, "distribución conjunta completa")
        nombre = titulo("Distribución conjunta completa", TAM_SUBTITULO, RESALTADO).next_to(columnas, DOWN, buff=1.0)
        self.play(Write(nombre))
        self.esperar_hasta(b["fin"])

        # Bloque 1 — IA: 32 filas.
        b = self.iniciar_bloque(1)
        self.limpiar()
        filas = [
            ["V", "V", "V", "V", "V", "…"],
            ["V", "V", "V", "V", "F", "…"],
            ["V", "V", "V", "F", "V", "…"],
            ["⋮", "⋮", "⋮", "⋮", "⋮", "⋮"],
            ["F", "F", "F", "F", "F", "…"],
        ]
        tabla = tabla_cpt(["Robo", "Terremoto", "Alarma", "Camilo", "Isabel", "Probabilidad"], filas)
        tabla.scale(1.5)
        contador = formula(r"2^5 = 32 \text{ filas}", 56, RESALTADO)
        VGroup(tabla, contador).arrange(DOWN, buff=0.7)
        ajustar(VGroup(tabla, contador)).move_to(ORIGIN)
        self.play(FadeIn(tabla, shift=DOWN * 0.3), run_time=1.2)
        self.en(b, "Dos elevado a la cinco")
        self.play(Write(contador))
        self.esperar_hasta(b["fin"])

        # Bloque 2 — Estudiante (se mantiene el fondo).
        self.iniciar_bloque(2)

        # Bloque 3 — Analista: el contador sube.
        b = self.iniciar_bloque(3)
        self.limpiar()
        crecimiento = tabla_formulas([
            [r"5 \text{ variables}", r"\rightarrow", r"2^{5} = 32"],
            [r"20 \text{ variables}", r"\rightarrow", r"2^{20} \approx 1 \text{ millón}"],
            [r"50 \text{ variables}", r"\rightarrow", r"2^{50} \approx 10^{15}"],
            [r"100 \text{ variables}", r"\rightarrow", r"2^{100} \approx 1{,}27 \times 10^{30}"],
        ], tam=48, alineacion="rcl", buff=(0.5, 0.45))
        self.play(FadeIn(crecimiento.filas[0]))
        self.en(b, "Un sistema de diagnóstico")
        self.play(FadeIn(crecimiento.filas[1]))
        self.play(FadeIn(crecimiento.filas[2]))
        self.en(b, "Pongamos cien variables")
        self.play(FadeIn(crecimiento.filas[3]))
        self.play(crecimiento.filas[3].animate.set_color(RESALTADO))
        self.esperar_hasta(b["fin"])

        # Bloque 4 — IA: más que la edad del universo.
        b = self.iniciar_bloque(4)
        self.limpiar()
        encabezado = texto("Escribiendo 1.000.000.000 de filas por segundo:", TAM_CUERPO, TEXTO_SECUNDARIO)
        calculo = tabla_formulas([
            [r"1{,}27 \times 10^{30} \text{ filas}", r"\rightarrow", r"\approx 40 \text{ billones de años}"],
            [r"\text{Edad del universo}", r"\approx", r"13.800 \text{ millones de años}"],
        ], tam=44, alineacion="rcl")
        conclusion = titulo("→ casi 3.000 veces la edad del universo", TAM_SUBTITULO, RESALTADO)
        bloque = VGroup(encabezado, calculo, conclusion).arrange(DOWN, buff=0.7)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(encabezado))
        self.play(FadeIn(calculo.filas[0]))
        self.en(b, "Casi tres mil veces")
        self.play(FadeIn(calculo.filas[1]))
        self.play(Write(conclusion))
        self.esperar_hasta(b["fin"])

        # Bloque 5 — Narrador: la pregunta y la respuesta.
        b = self.iniciar_bloque(5)
        self.limpiar()
        pregunta = parrafo("¿Cómo razona una IA con incertidumbre\nsin que le explote la memoria?", 48, negrita=True)
        pregunta.shift(UP * 1.2)
        self.play(Write(pregunta), run_time=2)
        self.en(b, "las redes bayesianas")
        respuesta = titulo("Redes bayesianas", TAM_TITULO, NODO).next_to(pregunta, DOWN, buff=1.0)
        self.play(FadeIn(respuesta, scale=1.2))
        self.en(b, "no todo depende de todo")
        truco = texto("No todo depende de todo.", TAM_SUBTITULO, RESALTADO).next_to(respuesta, DOWN, buff=0.6)
        self.play(FadeIn(truco))
        self.terminar()
