"""Escena 10 — Análisis y aplicación: computación y comunicaciones."""

import numpy as np
from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.style import *


def centro_operaciones() -> VGroup:
    """Tres pantallas con tráfico, routers conectados y alertas."""
    rng = np.random.default_rng(4)
    pantallas = VGroup()
    for _ in range(3):
        marco = RoundedRectangle(width=3.0, height=1.9, corner_radius=0.12, color=TEXTO, stroke_width=2)
        xs = np.linspace(-1.3, 1.3, 14)
        ys = rng.uniform(-0.6, 0.6, 14)
        trafico = VMobject(color=FLECHA, stroke_width=2).set_points_as_corners([[x, y, 0] for x, y in zip(xs, ys)])
        pantallas.add(VGroup(marco, trafico.move_to(marco)))
    pantallas.arrange(RIGHT, buff=0.5)
    routers = VGroup(*(RoundedRectangle(width=0.9, height=0.45, corner_radius=0.1, color=NODO, stroke_width=2,
                                        fill_color=NODO, fill_opacity=0.15) for _ in range(4)))
    routers.arrange(RIGHT, buff=1.4).next_to(pantallas, DOWN, buff=1.0)
    enlaces = VGroup(*(Line(a.get_right(), b.get_left(), color=FLECHA, stroke_width=2)
                       for a, b in zip(routers, routers[1:])))
    alertas = VGroup(*(Dot(radius=0.1, color=NEGATIVO).next_to(p[0], UP, buff=0.12).align_to(p[0], RIGHT)
                       for p in pantallas))
    return VGroup(pantallas, routers, enlaces, alertas)


def grafo_codigo() -> tuple[VGroup, list[Line]]:
    """Grafo de un código: nodos de bits (círculos) y de paridad (cuadrados)."""
    bits = VGroup(*(Circle(radius=0.22, color=NODO, stroke_width=2.5) for _ in range(6))).arrange(RIGHT, buff=0.6)
    paridad = VGroup(*(Square(0.42, color=RESALTADO, stroke_width=2.5) for _ in range(3))).arrange(RIGHT, buff=1.5)
    paridad.next_to(bits, UP, buff=1.2)
    conexiones = [(0, 0), (0, 1), (0, 3), (1, 1), (1, 2), (1, 4), (2, 3), (2, 4), (2, 5)]
    aristas = [Line(paridad[p].get_bottom(), bits[b].get_top(), color=TEXTO_SECUNDARIO, stroke_width=1.5)
               for p, b in conexiones]
    return VGroup(VGroup(*aristas), bits, paridad), aristas


class Escena10(EscenaNarrada):
    numero = 10

    def construct(self):
        # Bloque 0 — Narrador: título y centro de operaciones.
        self.iniciar_bloque(0)
        cabecera = titulo("Análisis y aplicación", TAM_TITULO).to_edge(UP, buff=MARGEN)
        noc = centro_operaciones()
        ajustar(noc, alto=ALTO_UTIL - cabecera.height - 0.8).next_to(cabecera, DOWN, buff=0.8)
        self.play(FadeIn(cabecera), FadeIn(noc), run_time=1.2)
        self.play(Flash(noc[3][0], color=NEGATIVO), Flash(noc[3][2], color=NEGATIVO), run_time=1)
        self.play(Flash(noc[3][1], color=NEGATIVO), run_time=1)

        # Bloque 1 — Analista: la red de la alarma se transforma.
        b = self.iniciar_bloque(1)
        self.limpiar()
        cabecera = titulo("Aplicación 1 — Diagnóstico de fallas en una red", TAM_SUBTITULO, RESALTADO)
        ajustar(cabecera).to_edge(UP, buff=MARGEN)
        pie = nota("Mismas tablas, mismos números (ejemplo ilustrativo)").to_edge(DOWN, buff=MARGEN)
        red = red_alarma(escala=1.15)
        self.play(FadeIn(cabecera), FadeIn(red))
        cambios = [("El robo se vuelve", {"robo": "Falla del enlace"}),
                   ("El terremoto se vuelve", {"terremoto": "Pico de tráfico"}),
                   ("La alarma es", {"alarma": "Pérdida de paquetes"}),
                   ("Y Camilo e Isabel", {"camilo": "Alerta del monitor 1", "isabel": "Alerta del monitor 2"})]
        for frase, nombres in cambios:
            self.en(b, frase)
            self.play(red.renombrar(**nombres))
        self.play(FadeIn(pie))
        self.esperar_hasta(b["fin"])

        # Bloque 2 — IA: la matemática es idéntica.
        b = self.iniciar_bloque(2)
        resultados = tabla_formulas([
            [r"P(\text{Falla} \mid \text{Alerta 1}, \text{Alerta 2})", r"\approx 28{,}4\,\%"],
            [r"P(\text{Falla} \mid \text{Alerta 1}, \text{Alerta 2}, \text{Pico de tráfico})", r"\approx 0{,}33\,\%"],
        ], tam=38, alineacion="ll")
        recomendacion = texto("→ Recomendación automática: revisar el tráfico antes de enviar un técnico",
                              TAM_PEQUENO + 2, RESALTADO)
        abajo = VGroup(resultados, recomendacion).arrange(DOWN, buff=0.4)
        ajustar(abajo)
        destino = red.copy()
        destino.scale_to_fit_height(ALTO_UTIL - cabecera.height - abajo.height - 1.4)
        destino.next_to(cabecera, DOWN, buff=0.5)
        abajo.next_to(destino, DOWN, buff=0.5)
        self.play(FadeOut(pie), Transform(red, destino))
        self.en(b, "Con las dos alertas")
        self.play(FadeIn(resultados.filas[0]),
                  red.estados(camilo="evidencia", isabel="evidencia", robo="activo"))
        self.en(b, "Pero si sé que hubo")
        self.play(FadeIn(resultados.filas[1]), red.estados(terremoto="evidencia", robo="inactivo"))
        self.en(b, "Es la explicación alternativa")
        self.play(FadeIn(recomendacion))
        self.esperar_hasta(b["fin"])

        # Bloque 3 — Profesora: decodificación en comunicaciones.
        b = self.iniciar_bloque(3)
        self.limpiar()
        cabecera = titulo("Aplicación 2 — Decodificación en comunicaciones", TAM_SUBTITULO, RESALTADO)
        ajustar(cabecera).to_edge(UP, buff=MARGEN)
        canal = texto("bits enviados  1 0 1 1 0   →   ruido   →   bits recibidos  1 0 0 1 0",
                      TAM_CUERPO, t2c={"ruido": NEGATIVO})
        grafo, aristas = grafo_codigo()
        codigos = texto("Códigos turbo (redes 4G)  ·  Códigos LDPC (redes 5G y Wi-Fi)", TAM_PEQUENO + 2, NODO)
        cita = nota("McEliece, MacKay y Cheng (1998): la decodificación turbo es un caso "
                    "de la propagación de creencias de Pearl")
        cuerpo = VGroup(canal, grafo, codigos, cita).arrange(DOWN, buff=0.5)
        ajustar(cuerpo, alto=ALTO_UTIL - cabecera.height - 0.5).next_to(cabecera, DOWN, buff=0.5)
        self.play(FadeIn(cabecera))
        self.en(b, "los bits llegan contaminados")
        self.play(FadeIn(canal))
        self.en(b, "tratan cada bit")
        self.play(FadeIn(grafo), run_time=1.2)
        self.en(b, "pasando probabilidades")
        mensajes = [Dot(radius=0.07, color=RESALTADO).move_to(a.get_start()) for a in aristas]
        for m in mensajes:
            m.permite_solape = True
        self.play(*(MoveAlongPath(m, a) for m, a in zip(mensajes, aristas)), run_time=1.5)
        self.play(*(MoveAlongPath(m, Line(a.get_end(), a.get_start())) for m, a in zip(mensajes, aristas)),
                  run_time=1.5)
        self.remove(*mensajes)
        self.play(FadeIn(codigos))
        self.en(b, "En mil novecientos noventa y ocho")
        self.play(FadeIn(cita))
        self.esperar_hasta(b["fin"])

        # Bloque 4 — Analista: ¿la caché reduce la latencia?
        b = self.iniciar_bloque(4)
        self.limpiar()
        cabecera = VGroup(
            titulo("Aplicación 3 — ¿La caché reduce la latencia?", TAM_SUBTITULO, RESALTADO),
            nota("(ejemplo ilustrativo, valores inventados)"),
        ).arrange(DOWN, buff=0.2)
        ajustar(cabecera).to_edge(UP, buff=MARGEN)
        red = RedBayesiana(
            {"carga": ("Carga del servidor", (0, 1.4)), "cache": ("Caché activada", (-2.2, -0.6)),
             "latencia": ("Latencia alta", (2.2, -0.6))},
            [("carga", "cache"), ("carga", "latencia"), ("cache", "latencia")],
        )
        tablas = VGroup(
            prob_previa("Carga alta", "0,5"),
            texto("P(Caché | carga alta) = 0,8     P(Caché | carga baja) = 0,2", TABLA_TAM_TEXTO),
            tabla_cpt(["P(Latencia alta | ·)", "Carga alta", "Carga baja"],
                      [["Con caché", "0,5", "0,1"], ["Sin caché", "0,8", "0,2"]]),
        ).arrange(DOWN, buff=0.4)
        cuerpo = VGroup(red, tablas).arrange(RIGHT, buff=0.9)
        ajustar(cuerpo, alto=ALTO_UTIL - cabecera.height - 0.6).next_to(cabecera, DOWN, buff=0.6)
        self.play(FadeIn(cabecera), FadeIn(red))
        self.en(b, "sobre todo en los que tienen más carga")
        self.play(FadeIn(tablas), run_time=1.2)
        self.esperar_hasta(b["fin"])

        # Bloque 5 — IA: observar contra intervenir.
        b = self.iniciar_bloque(5)
        self.limpiar()
        observar = VGroup(
            titulo("OBSERVAR (datos tal cual)", TAM_CUERPO, TEXTO_SECUNDARIO),
            tabla_formulas([
                [r"P(\text{Latencia alta} \mid \text{con caché})", r"= 0{,}8 \times 0{,}5 + 0{,}2 \times 0{,}1 = 0{,}42"],
                [r"P(\text{Latencia alta} \mid \text{sin caché})", r"= 0{,}2 \times 0{,}8 + 0{,}8 \times 0{,}2 = 0{,}32"],
            ], tam=34, alineacion="rl", buff=(0.2, 0.3)),
            texto("→ «La caché empeora la latencia»  ✗", TAM_PEQUENO + 2, NEGATIVO),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        intervenir = VGroup(
            titulo("INTERVENIR (ajuste por la carga: puerta trasera cerrada)", TAM_CUERPO, TEXTO_SECUNDARIO),
            tabla_formulas([
                [r"P(\text{Latencia alta} \mid do(\text{con caché}))", r"= 0{,}5 \times 0{,}5 + 0{,}5 \times 0{,}1 = 0{,}30"],
                [r"P(\text{Latencia alta} \mid do(\text{sin caché}))", r"= 0{,}5 \times 0{,}8 + 0{,}5 \times 0{,}2 = 0{,}50"],
            ], tam=34, alineacion="rl", buff=(0.2, 0.3)),
            texto("→ La caché reduce la latencia alta del 50 % al 30 %  ✓", TAM_PEQUENO + 2, POSITIVO),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        bloque = VGroup(observar, intervenir).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(observar[0]), FadeIn(observar[1]))
        self.en(b, "Parecería que la caché")
        self.play(FadeIn(observar[2]))
        self.en(b, "Si cierro la puerta trasera")
        self.play(FadeIn(intervenir[0]), FadeIn(intervenir[1]))
        self.en(b, "activar la caché baja")
        self.play(FadeIn(intervenir[2]))
        self.terminar()
