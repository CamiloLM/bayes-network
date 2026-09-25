"""Escena 8 — Cuando la red es gigante: inferencia aproximada."""

import numpy as np
from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.style import *


def red_gigante(n: int = 60, semilla: int = 7) -> VGroup:
    """Muchos nodos pequeños con conexiones cruzadas (decorativo)."""
    rng = np.random.default_rng(semilla)
    puntos = [np.array([x, y, 0]) for x, y in zip(rng.uniform(-3.2, 3.2, n), rng.uniform(-2.4, 2.4, n))]
    lineas = VGroup()
    for i, p in enumerate(puntos):
        cercanos = sorted(range(n), key=lambda j: np.linalg.norm(puntos[j] - p))[1:4]
        for j in cercanos:
            lineas.add(Line(p, puntos[j], color=FLECHA, stroke_width=1.5, stroke_opacity=0.6))
    nodos = VGroup(*(Dot(p, radius=0.07, color=NODO) for p in puntos))
    lineas.permite_solape = True  # aparecen por separado, pero son la misma red
    return VGroup(lineas, nodos)


def reloj_arena() -> VGroup:
    arriba = Polygon([-0.8, 1.2, 0], [0.8, 1.2, 0], [0, 0, 0], color=TEXTO, stroke_width=3)
    abajo = Polygon([-0.8, -1.2, 0], [0.8, -1.2, 0], [0, 0, 0], color=TEXTO, stroke_width=3)
    arena = Polygon([-0.5, 0.95, 0], [0.5, 0.95, 0], [0, 0.2, 0], stroke_width=0, fill_color=RESALTADO,
                    fill_opacity=0.8)
    return VGroup(arriba, abajo, arena)


def fichas(n: int, columnas: int, lado: float = 0.32) -> VGroup:
    grupo = VGroup(*(Square(lado, stroke_width=1.5, stroke_color=TEXTO_SECUNDARIO, fill_color=NODO,
                            fill_opacity=0.5) for _ in range(n)))
    return grupo.arrange_in_grid(cols=columnas, buff=0.08)


class Escena08(EscenaNarrada):
    numero = 8

    def construct(self):
        # Bloque 0 — Narrador: red gigante, problema NP-difícil.
        b = self.iniciar_bloque(0)
        gigante = red_gigante()
        reloj = reloj_arena()
        VGroup(gigante, reloj).arrange(RIGHT, buff=1.5).shift(UP * 0.4)
        self.play(Create(gigante[0]), FadeIn(gigante[1]), run_time=2)
        self.consolidar(gigante)
        self.play(FadeIn(reloj))
        self.en(b, "NP difícil")
        np_dificil = titulo("Inferencia exacta: NP-difícil", TAM_SUBTITULO, NEGATIVO).next_to(gigante, DOWN, buff=0.5)
        np_dificil.set_x(0)
        self.play(FadeIn(np_dificil), Rotate(reloj, PI, run_time=1.5))
        self.en(b, "Si no podemos calcular")
        simular = titulo("Si no podemos calcular… simulamos.", TAM_SUBTITULO, RESALTADO).move_to(np_dificil)
        self.cambiar(np_dificil, simular)
        self.esperar_hasta(b["fin"])

        # Bloque 1 — Analista: la red del aspersor.
        b = self.iniciar_bloque(1)
        self.limpiar()
        grupo = red_aspersor_con_tablas()
        red = grupo[0]
        self.play(FadeIn(grupo), run_time=1.2)
        self.en(b, "Cuando el día está nublado")
        self.play(red.estados(nublado="activo", aspersor="activo"))
        self.en(b, "Los días nublados llueve")
        self.play(red.estados(aspersor="normal", lluvia="activo"))
        self.en(b, "Y el césped se moja")
        self.play(red.estados(nublado="normal", lluvia="normal", cesped="activo"))
        self.esperar_hasta(b["fin"])
        self.play(red.restablecer())

        # Bloque 2 — IA: muestreo directo.
        b = self.iniciar_bloque(2)
        self.limpiar()
        cabecera = titulo("Muestreo directo — de padres a hijos", TAM_SUBTITULO, RESALTADO).to_edge(UP, buff=MARGEN)
        red = red_aspersor(escala=0.8)
        pasos = VGroup(
            texto("1. Nublado: sorteo con 0,5  →  V", TAM_PEQUENO),
            texto("2. Aspersor: sorteo con P(Aspersor | Nublado) = 0,10  →  F", TAM_PEQUENO),
            texto("3. Lluvia: sorteo con P(Lluvia | Nublado) = 0,80  →  V", TAM_PEQUENO),
            texto("4. Césped: sorteo con P(Césped | ¬A, L) = 0,90  →  V", TAM_PEQUENO),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        muestra = texto("Muestra: [Nublado = V, Aspersor = F, Lluvia = V, Césped = V]", TAM_PEQUENO + 2, RESALTADO)
        cuerpo = VGroup(red, pasos).arrange(RIGHT, buff=0.8)
        contenido = VGroup(cuerpo, muestra).arrange(DOWN, buff=0.6)
        ajustar(contenido, alto=ALTO_UTIL - cabecera.height - 0.6).next_to(cabecera, DOWN, buff=0.6)
        self.play(FadeIn(cabecera), FadeIn(red))
        sorteos = [("Sale nublado", "nublado", "activo"), ("sale apagado", "aspersor", "inactivo"),
                   ("Sorteo la lluvia", "lluvia", "activo"), ("Y sorteo el césped", "cesped", "activo")]
        for paso, (frase, nodo, estado) in zip(pasos, sorteos):
            self.en(b, frase)
            self.play(FadeIn(paso), red.estados(**{nodo: estado}))
        self.en(b, "Esa es una muestra")
        self.play(FadeIn(muestra))
        self.en(b, "Si genero miles")
        muchas = fichas(60, 12, 0.3)
        muchas.move_to(pasos)
        self.play(FadeOut(pasos), FadeOut(muestra))
        self.play(LaggedStart(*(FadeIn(f, shift=DOWN * 0.4) for f in muchas), lag_ratio=0.04), run_time=3)
        self.esperar_hasta(b["fin"])

        # Bloque 3 — Estudiante (se mantiene).
        self.iniciar_bloque(3)

        # Bloque 4 — Analista: muestreo por rechazo.
        b = self.iniciar_bloque(4)
        self.limpiar()
        cabecera = titulo("Muestreo por rechazo — P(Lluvia | Aspersor = V)", TAM_SUBTITULO, RESALTADO)
        ajustar(cabecera).to_edge(UP, buff=MARGEN)
        cien = fichas(100, 10, 0.34)
        datos = VGroup(
            texto("100 muestras generadas", TAM_PEQUENO),
            texto("73 con el aspersor apagado  →  rechazadas ✗", TAM_PEQUENO, NEGATIVO),
            texto("27 con el aspersor encendido  →  aceptadas ✓", TAM_PEQUENO, POSITIVO),
            texto("de esas 27:  8 con lluvia · 19 sin lluvia", TAM_PEQUENO, NODO),
            formula(r"\text{Estimación: } 8/27 \approx 0{,}296", 36, RESALTADO),
            formula(r"\text{Valor exacto: } 0{,}30", 36),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        cuerpo = VGroup(cien, datos).arrange(RIGHT, buff=1.0)
        ajustar(cuerpo, alto=ALTO_UTIL - cabecera.height - 0.6).next_to(cabecera, DOWN, buff=0.6)
        orden = np.random.default_rng(3).permutation(100)
        rechazadas = [cien[i] for i in orden[:73]]
        con_lluvia = [cien[i] for i in orden[73:81]]
        self.play(FadeIn(cabecera), FadeIn(cien), FadeIn(datos[0]))
        self.en(b, "descarto los que no coinciden")
        self.play(*(f.animate.set_fill(NEGATIVO, 0.15).set_stroke(NEGATIVO, opacity=0.3) for f in rechazadas),
                  FadeIn(datos[1]), run_time=1.5)
        self.consolidar(cien)
        self.en(b, "Quedan veintisiete")
        self.play(FadeIn(datos[2]))
        self.en(b, "En ocho de ellas llueve")
        self.play(*(f.animate.set_fill(RESALTADO, 0.9) for f in con_lluvia), FadeIn(datos[3]))
        self.consolidar(cien)
        self.en(b, "Ocho de veintisiete")
        self.play(FadeIn(datos[4]))
        self.en(b, "El valor exacto")
        self.play(FadeIn(datos[5]))
        self.esperar_hasta(b["fin"])

        # Bloque 5 — Profesora: el desperdicio.
        b = self.iniciar_bloque(5)
        desperdicio = VGroup(
            parrafo("Evidencia con probabilidad 0,001\n→ se desechan 999 de cada 1.000 muestras", TAM_PEQUENO,
                    alineacion=LEFT),
            parrafo("Cada variable de evidencia adicional\n→ la fracción útil cae exponencialmente", TAM_PEQUENO,
                    NEGATIVO, alineacion=LEFT),
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(datos, aligned_edge=LEFT)
        self.play(FadeOut(datos))
        self.en(b, "Y si la evidencia fuera rara")
        self.play(FadeIn(desperdicio[0]))
        self.en(b, "Con cada variable")
        self.play(FadeIn(desperdicio[1]))
        self.esperar_hasta(b["fin"])

        # Bloque 6 — Analista: más muestras, mejor estimación.
        b = self.iniciar_bloque(6)
        self.limpiar()
        cabecera = parrafo("Simulación de ejemplo — muestreo por rechazo\nP(Lluvia | Aspersor = V), valor exacto 0,30",
                           TAM_CUERPO, TEXTO_SECUNDARIO)
        tabla = tabla_cpt(
            ["Muestras generadas", "Aceptadas", "Con lluvia", "Estimación"],
            [["100", "33", "11", "0,333"], ["1.000", "314", "93", "0,296"], ["10.000", "3.031", "894", "0,295"]],
            tam=30,
        )
        error = VGroup(
            VGroup(texto("El error típico se reduce en proporción a", TAM_CUERPO),
                   formula(r"1/\sqrt{n}", 44, RESALTADO)).arrange(RIGHT, buff=0.25),
            nota("(100 veces más muestras → error 10 veces menor)", TAM_CUERPO - 4),
        ).arrange(DOWN, buff=0.3)
        bloque = VGroup(cabecera, tabla, error).arrange(DOWN, buff=0.6)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(cabecera), FadeIn(tabla))
        self.en(b, "El error baja")
        self.play(FadeIn(error))
        self.esperar_hasta(b["fin"])

        # Bloque 7 — IA: ponderación por verosimilitud.
        b = self.iniciar_bloque(7)
        self.limpiar()
        cabecera = titulo("Ponderación por verosimilitud", TAM_SUBTITULO, RESALTADO)
        consulta = formula(r"P(\text{Lluvia} \mid \text{Nublado} = V,\ \text{Césped} = V)", 36, TEXTO_SECUNDARIO)
        encabezado = VGroup(cabecera, consulta).arrange(DOWN, buff=0.25).to_edge(UP, buff=MARGEN)
        red = red_aspersor(escala=0.75)
        pasos = VGroup(
            texto("Peso inicial: w = 1", TAM_PEQUENO),
            texto("1. Nublado es evidencia → no se sortea:  w = 1 × 0,5 = 0,5", TAM_PEQUENO),
            texto("2. Aspersor: se sortea con 0,10  →  F", TAM_PEQUENO),
            texto("3. Lluvia: se sortea con 0,80  →  V", TAM_PEQUENO),
            texto("4. Césped es evidencia → no se sortea:  w = 0,5 × 0,90 = 0,45", TAM_PEQUENO),
            texto("Esta muestra vale 0,45 votos a favor de «Lluvia = V».", TAM_PEQUENO, RESALTADO),
            texto("Ninguna muestra se desecha.", TAM_PEQUENO, POSITIVO),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        cuerpo = VGroup(red, pasos).arrange(RIGHT, buff=0.8)
        ajustar(cuerpo, alto=ALTO_UTIL - encabezado.height - 1.6).next_to(encabezado, DOWN, buff=0.6)
        self.play(FadeIn(encabezado), FadeIn(red))
        self.en(b, "La idea es no sortear")
        self.play(red.estados(nublado="evidencia", cesped="evidencia"), FadeIn(pasos[0]))
        marcas = ["Nublado es evidencia", "Sorteo el aspersor", "Sorteo la lluvia", "El césped es evidencia",
                  "Esta muestra cuenta", "Y no boté ninguna"]
        for linea, frase in zip(pasos[1:], marcas):
            self.en(b, frase)
            self.play(FadeIn(linea))
        self.esperar_hasta(b["fin"])

        # Bloque 8 — Analista: el punto débil.
        b = self.iniciar_bloque(8)
        debil = texto("Punto débil: evidencia muy abajo en la red → muchas muestras con pesos minúsculos",
                      TAM_PEQUENO, NEGATIVO)
        ajustar(debil).to_edge(DOWN, buff=MARGEN)
        self.play(FadeIn(debil))
        self.esperar_hasta(b["fin"])

        # Bloque 9 — Profesora: muestreo de Gibbs.
        b = self.iniciar_bloque(9)
        self.limpiar()
        cabecera = parrafo("Muestreo de Gibbs\n(cadena de Markov Monte Carlo)", TAM_SUBTITULO, RESALTADO, negrita=True)
        lineas = VGroup(
            formula(r"\text{Consulta: } P(\text{Lluvia} \mid \text{Aspersor} = V,\ \text{Césped} = V)", 34),
            texto("Evidencia fija:  Aspersor = V, Césped = V", TAM_PEQUENO, NODO),
            texto("Estado inicial al azar:  [Nublado = V, Aspersor = V, Lluvia = F, Césped = V]", TAM_PEQUENO),
            texto("→ Re-sortear Nublado dado su manto de Markov  →  F    [F, V, F, V]", TAM_PEQUENO),
            texto("→ Re-sortear Lluvia dado su manto de Markov  →  V    [F, V, V, V]", TAM_PEQUENO),
            texto("→ … repetir miles de veces …", TAM_PEQUENO, TEXTO_SECUNDARIO),
            texto("P(Lluvia | evidencia) ≈ proporción de estados visitados con Lluvia = V", TAM_PEQUENO, RESALTADO),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        bloque = VGroup(cabecera, lineas).arrange(DOWN, buff=0.6)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(cabecera))
        marcas = ["En lugar de generar", "En lugar de generar", "parte de un mundo cualquiera",
                  "Cada variable se vuelve", "Les dije que iba a volver", "Después de miles de pasos",
                  "la fracción del tiempo"]
        for linea, frase in zip(lineas, marcas):
            self.en(b, frase)
            self.play(FadeIn(linea), run_time=0.6)
        self.esperar_hasta(b["fin"])

        # Bloque 10 — IA: dos caminos.
        b = self.iniciar_bloque(10)
        self.limpiar()
        caminos = tabla_formulas([
            [r"\text{Inferencia exacta}", r"\rightarrow", r"\text{respuesta precisa, costo que puede explotar}"],
            [r"\text{Inferencia aproximada}", r"\rightarrow", r"\text{estimación que mejora con más muestras}"],
        ], tam=40, alineacion="rcl", buff=(0.4, 0.8))
        ajustar(caminos).move_to(ORIGIN)
        self.play(FadeIn(caminos.filas[0]))
        self.play(FadeIn(caminos.filas[1]))
        self.terminar()
