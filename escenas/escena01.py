"""Escena 1 — La alarma."""

from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.style import *


def estudiante() -> VGroup:
    """Estudiante sentado en su pupitre (figura simple)."""
    cabeza = Circle(radius=0.35, color=TEXTO, stroke_width=3)
    cuerpo = RoundedRectangle(width=1.1, height=1.2, corner_radius=0.35, color=TEXTO, stroke_width=3)
    cuerpo.next_to(cabeza, DOWN, buff=0.08)
    mesa = Line(LEFT * 1.4, RIGHT * 1.4, color=TEXTO_SECUNDARIO, stroke_width=5).next_to(cuerpo, DOWN, buff=0)
    patas = VGroup(
        Line(ORIGIN, DOWN * 0.8, color=TEXTO_SECUNDARIO, stroke_width=4).move_to(mesa.get_left() + RIGHT * 0.2 + DOWN * 0.4),
        Line(ORIGIN, DOWN * 0.8, color=TEXTO_SECUNDARIO, stroke_width=4).move_to(mesa.get_right() + LEFT * 0.2 + DOWN * 0.4),
    )
    return VGroup(cabeza, cuerpo, mesa, patas)


def mensaje(quien: str, dice: str, color) -> VGroup:
    nombre = titulo(quien, TAM_PEQUENO, color)
    cita = texto(f"«{dice}»", TAM_PEQUENO)
    contenido = VGroup(nombre, cita).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    marco = SurroundingRectangle(contenido, color=color, buff=0.25, corner_radius=0.15, stroke_width=2)
    return VGroup(marco, contenido)


class Escena01(EscenaNarrada):
    numero = 1

    def construct(self):
        # Bloque 0 — Narrador: la llamada.
        b = self.iniciar_bloque(0)
        clase = nota("Clase de Modelos Estocásticos", TAM_PEQUENO + 2)
        figura = estudiante()
        movil = celular().scale(0.55)
        escena = VGroup(figura, movil).arrange(RIGHT, buff=0.6, aligned_edge=DOWN)
        izquierda = VGroup(clase, escena).arrange(DOWN, buff=0.6).scale(1.1)
        izquierda.to_edge(LEFT, buff=MARGEN + 0.5).shift(DOWN * 0.5)
        self.play(FadeIn(izquierda), run_time=1)

        self.en(b, "te entra una llamada")
        self.play(Wiggle(movil, scale_value=1.2), run_time=1)
        m1 = mensaje("Camilo, tu vecino", "Escuché la alarma de tu casa", NODO)
        m2 = mensaje("Isabel, tu otra vecina", "Yo también oí la alarma", NODO)
        mensajes = VGroup(m1, m2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).scale(1.15)
        mensajes.to_edge(RIGHT, buff=MARGEN + 0.3).shift(DOWN * 0.3)
        self.en(b, "Es Camilo")
        self.play(FadeIn(m1, shift=LEFT * 0.3))
        self.en(b, "¿Alguien entró?")
        dudas = texto("¿Robo?  ¿Accidente?", TAM_CUERPO, RESALTADO).next_to(izquierda, UP, buff=0.4)
        self.play(FadeIn(dudas))
        self.en(b, "Unos segundos después")
        self.play(Wiggle(movil, scale_value=1.2), run_time=1)
        self.en(b, "Es Isabel")
        self.play(FadeIn(m2, shift=LEFT * 0.3))
        self.en(b, "Pero ninguno vio nada")
        aviso = nota("Ninguno vio nada: solo oyeron un ruido.").next_to(mensajes, DOWN, buff=0.5)
        self.play(FadeIn(aviso))
        self.en(b, "¿qué deberías creer")
        self.play(FadeOut(dudas))
        pregunta = titulo("¿Qué deberías creer?", TAM_SUBTITULO, RESALTADO).to_edge(UP, buff=MARGEN)
        self.play(Write(pregunta))
        self.en(b, "¿cómo respondería")
        pregunta2 = titulo("¿Cómo lo respondería una computadora?", TAM_SUBTITULO, RESALTADO).move_to(pregunta)
        self.cambiar(pregunta, pregunta2)
        self.esperar_hasta(b["fin"])

        # Bloque 1 — Estudiante.
        self.iniciar_bloque(1)
        self.limpiar()
        robo = titulo("¿Hubo un robo?", TAM_TITULO)
        self.play(Write(robo), run_time=0.8)

        # Bloque 2 — Profesora: probable no es seguro.
        b = self.iniciar_bloque(2)
        self.play(robo.animate.to_edge(UP, buff=1.0))
        palabras = titulo("probable   ≠   seguro", TAM_TITULO, t2c={"probable": RESALTADO, "seguro": TEXTO_SECUNDARIO})
        probable, distinto, seguro = partes(palabras, "probable", "≠", "seguro")
        self.en(b, '"probable"')
        self.play(FadeIn(probable, scale=1.2))
        self.en(b, 'No dijiste "seguro"')
        self.play(FadeIn(distinto), FadeIn(seguro))
        self.en(b, "Tiene que razonar")
        tareas = texto(
            "•  información incompleta       •  combinar evidencia       •  actualizar lo que cree",
            TAM_CUERPO, t2c={"•": FLECHA},
        )
        ajustar(tareas).next_to(palabras, DOWN, buff=1.2)
        piezas = partes(tareas, "• información incompleta", "• combinar evidencia", "• actualizar lo que cree")
        self.play(LaggedStart(*(FadeIn(p) for p in piezas), lag_ratio=0.5), run_time=2)
        self.esperar_hasta(b["fin"])

        # Bloque 3 — IA: la respuesta es un número.
        b = self.iniciar_bloque(3)
        self.play(FadeOut(palabras, tareas))
        si_no = titulo("¿sí o no?", TAM_TITULO, TEXTO_SECUNDARIO)
        self.play(FadeIn(si_no))
        tachado = Cross(si_no, stroke_color=NEGATIVO, stroke_width=6)
        tachado.permite_solape = True
        self.play(Create(tachado))
        self.en(b, "Debería ser un número")
        numero = formula(r"P(\text{Robo} \mid \text{evidencia}) = \; ?", 64, RESALTADO)
        self.play(FadeOut(si_no, tachado), Write(numero))
        self.esperar_hasta(b["fin"])

        # Bloque 4 — Narrador: título.
        b = self.iniciar_bloque(4)
        self.limpiar()
        cabecera = titulo_seccion("Razonamiento probabilístico", "Capítulo 13").shift(UP * 1.2)
        self.play(FadeIn(cabecera, shift=UP * 0.2))
        self.en(b, "representar la incertidumbre")
        pasos = texto("representar        calcular        distinguir").next_to(cabecera, DOWN, buff=0.9)
        self.play(LaggedStart(*(FadeIn(p) for p in partes(pasos, "representar", "calcular", "distinguir")),
                              lag_ratio=0.6), run_time=2.5)
        self.en(b, "observar que algo ocurrió")
        contraste = titulo(
            "observar que algo ocurrió   ≠   hacer que algo ocurra", TAM_SUBTITULO,
            t2c={"observar que algo ocurrió": NODO, "hacer que algo ocurra": RESALTADO},
        )
        ajustar(contraste).next_to(pasos, DOWN, buff=0.9)
        observar, distinto, hacer = partes(contraste, "observar que algo ocurrió", "≠", "hacer que algo ocurra")
        self.play(FadeIn(observar))
        self.en(b, "de hacer que algo ocurra")
        self.play(FadeIn(distinto), FadeIn(hacer))
        self.terminar()
