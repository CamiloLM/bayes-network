"""Elementos visuales que se repiten entre escenas.

Todo sale de style.py. Las funciones devuelven Mobjects sin animar y centrados
en el origen; cada escena los posiciona y decide cómo animarlos. En pantalla
nada se sobrepone: usa ajustar() y next_to()/arrange() para repartir el espacio.
"""

import numpy as np
from manim import *

from escenas.style import *

# --- Texto -------------------------------------------------------------------


# Manim espacia mal las letras con font_size pequeños: por debajo de este tamaño
# se crea el texto a este tamaño y se escala. (Más grande, Pango parte las líneas.)
_TAM_BASE = 48


def _texto(contenido: str, tam: float, **kwargs) -> Text:
    base = max(tam, _TAM_BASE)
    return Text(contenido, font_size=base, **kwargs).scale(tam / base)


def texto(contenido: str, tam: float = TAM_CUERPO, color=TEXTO, **kwargs) -> Text:
    return _texto(contenido, tam, font=FUENTE_CUERPO, color=color, **kwargs)


def titulo(contenido: str, tam: float = TAM_TITULO, color=TEXTO, **kwargs) -> Text:
    return _texto(contenido, tam, font=FUENTE_TITULO, color=color, weight=BOLD, **kwargs)


def parrafo(contenido: str, tam: float = TAM_CUERPO, color=TEXTO, negrita: bool = False,
            alineacion=None, buff: float = 0.18, **kwargs) -> VGroup:
    """Varias líneas (separadas por salto de línea) centradas, o alineadas con alineacion=LEFT."""
    hacer = titulo if negrita else texto
    lineas = VGroup(*(hacer(l, tam, color, **kwargs) for l in contenido.splitlines()))
    return lineas.arrange(DOWN, buff=buff, aligned_edge=alineacion if alineacion is not None else ORIGIN)


def partes(t: Text, *trozos: str) -> list[VGroup]:
    """Glifos de cada trozo de `t`, en orden, para animarlos por separado.

    Una fila de palabras debe ser un solo Text (así comparte línea base);
    con esto se revela por partes: a, b = partes(t, "probable", "seguro").
    """
    letras = "".join(t.text.split())
    if len(letras) != len(t.submobjects):
        raise ValueError(f"no se pudo mapear glifos de {t.text!r}")
    grupos, desde = [], 0
    for trozo in trozos:
        trozo = "".join(trozo.split())
        i = letras.index(trozo, desde)
        grupos.append(VGroup(*t.submobjects[i:i + len(trozo)]))
        desde = i + len(trozo)
    return grupos


def titulo_seccion(contenido: str, subtitulo: str | None = None) -> VGroup:
    """Título grande de sección ("CASO 1 — OBSERVAR", "Conclusiones...")."""
    grupo = VGroup(titulo(contenido))
    if subtitulo:
        grupo.add(texto(subtitulo, TAM_SUBTITULO, TEXTO_SECUNDARIO))
    return grupo.arrange(DOWN, buff=SEPARACION)


def lista_puntos(items: list[str], numerada: bool = True, tam: int = TAM_CUERPO) -> VGroup:
    """Lista alineada a la izquierda; se revela punto por punto con grupo[i]."""
    lineas = VGroup()
    for i, item in enumerate(items, start=1):
        marca = texto(f"{i}." if numerada else "•", tam, RESALTADO)
        linea = VGroup(marca, texto(item, tam)).arrange(RIGHT, buff=0.2, aligned_edge=UP)
        lineas.add(linea)
    return lineas.arrange(DOWN, buff=SEPARACION, aligned_edge=LEFT)


def bloque_calculo(encabezado: str, lineas: list) -> VGroup:
    """Bloque "Paso N — ..." con líneas de cálculo (str o Mobject, p. ej. MathTex)."""
    cuerpo = VGroup(*(texto(l) if isinstance(l, str) else l for l in lineas))
    cuerpo.arrange(DOWN, buff=SEPARACION, aligned_edge=LEFT)
    return VGroup(titulo(encabezado, TAM_SUBTITULO, RESALTADO), cuerpo).arrange(
        DOWN, buff=SEPARACION * 1.5, aligned_edge=LEFT
    )


def formula(tex: str, tam: float = TAM_FORMULA, color=TEXTO, **kwargs) -> MathTex:
    """Fórmula en LaTeX (decimales con coma: 0{,}95)."""
    return MathTex(tex, font_size=tam, color=color, **kwargs)


def tabla_formulas(filas: list[list[str]], tam: float = TAM_FORMULA - 6, alineacion: str | None = None,
                   buff=(0.5, 0.3)) -> VGroup:
    """Filas de fórmulas alineadas en columnas (celdas vacías permitidas).

    grupo.filas[i] devuelve la fila i como VGroup, para revelarla o resaltarla.
    """
    columnas = max(len(f) for f in filas)
    celdas = VGroup()
    for fila in filas:
        for j in range(columnas):
            tex = fila[j] if j < len(fila) else ""
            celdas.add(formula(tex, tam) if tex else VectorizedPoint())
    celdas.arrange_in_grid(
        rows=len(filas), cols=columnas, buff=buff, col_alignments=alineacion or "l" * columnas
    )
    celdas.filas = [VGroup(*celdas[i * columnas:(i + 1) * columnas]) for i in range(len(filas))]
    return celdas


def nota(contenido: str, tam: float = TAM_PEQUENO) -> Text:
    """Texto secundario pequeño (aclaraciones, fuentes)."""
    return texto(contenido, tam, TEXTO_SECUNDARIO)


def resultado_destacado(contenido: str, tam: int = 56) -> VGroup:
    """Resultado clave enmarcado (p. ej. "P(Robo | Camilo, Isabel) ≈ 28,4 %")."""
    valor = titulo(contenido, tam, RESALTADO)
    marco = SurroundingRectangle(valor, color=RESALTADO, buff=0.3, corner_radius=0.15, stroke_width=3)
    return VGroup(marco, valor)


# --- Disposición -------------------------------------------------------------


def ajustar(mob: Mobject, ancho: float = ANCHO_UTIL, alto: float = ALTO_UTIL) -> Mobject:
    """Reduce `mob` (nunca lo agranda) para que quepa en ancho x alto."""
    factor = min(1.0, ancho / max(mob.width, 1e-6), alto / max(mob.height, 1e-6))
    return mob.scale(factor)


# --- Redes bayesianas --------------------------------------------------------


class Nodo(VGroup):
    """Variable de la red: caja redondeada con el nombre. Estados en ESTILOS_NODO."""

    def __init__(self, nombre: str, estado: str = "normal", **kwargs):
        super().__init__(**kwargs)
        self.nombre = nombre
        self.etiqueta = texto(nombre, NODO_TAM_TEXTO)
        self.caja = RoundedRectangle(
            width=self.etiqueta.width + 2 * NODO_RELLENO_X,
            height=NODO_ALTO,
            corner_radius=NODO_RADIO_ESQUINA,
        )
        self.add(self.caja, self.etiqueta)
        self.estilo(estado)

    def estilo(self, estado: str) -> "Nodo":
        """Aplica un estado; animable con nodo.animate.estilo("activo")."""
        e = ESTILOS_NODO[estado]
        self.estado = estado
        self.caja.set_stroke(e["borde"], width=NODO_GROSOR, opacity=e["opacidad"])
        self.caja.set_fill(e["relleno"], opacity=e["opacidad_relleno"])
        self.etiqueta.set_opacity(e["opacidad"])
        return self

    def borde_hacia(self, punto: np.ndarray) -> np.ndarray:
        """Punto del borde de la caja en dirección a `punto`."""
        centro = self.caja.get_center()
        d = punto - centro
        mitad_x, mitad_y = self.caja.width / 2, self.caja.height / 2
        escalas = [m / abs(c) for m, c in ((mitad_x, d[0]), (mitad_y, d[1])) if abs(c) > 1e-6]
        return centro + d * min(escalas, default=0)


def flecha_entre(origen: Nodo, destino: Nodo, color=FLECHA) -> Arrow:
    inicio = origen.borde_hacia(destino.caja.get_center())
    fin = destino.borde_hacia(origen.caja.get_center())
    return Arrow(
        inicio, fin,
        buff=FLECHA_SEPARACION,
        color=color,
        stroke_width=FLECHA_GROSOR,
        tip_length=FLECHA_PUNTA,
        max_tip_length_to_length_ratio=0.35,
        max_stroke_width_to_length_ratio=20,
    )


class RedBayesiana(VGroup):
    """Grafo dirigido a partir de nodos y aristas.

    nodos:   {id: (nombre visible, (x, y))}
    aristas: [(id_padre, id_hijo), ...]

    red.nodos[id] y red.flechas[(padre, hijo)] dan acceso a cada pieza.
    """

    def __init__(self, nodos: dict[str, tuple[str, tuple[float, float]]], aristas: list[tuple[str, str]], **kwargs):
        super().__init__(**kwargs)
        self.nodos = {}
        for id_, (nombre, (x, y)) in nodos.items():
            self.nodos[id_] = Nodo(nombre).move_to([x, y, 0])
        self.flechas = {(a, b): flecha_entre(self.nodos[a], self.nodos[b]) for a, b in aristas}
        # Flechas primero para que queden por debajo de los nodos.
        self.add(*self.flechas.values(), *self.nodos.values())

    def aparecer(self, lag: float = 0.15) -> Animation:
        """Nodos y luego flechas, en cascada."""
        return Succession(
            LaggedStart(*(FadeIn(n, scale=0.8) for n in self.nodos.values()), lag_ratio=lag),
            LaggedStart(*(GrowArrow(f) for f in self.flechas.values()), lag_ratio=lag),
        )

    def aplicar_estados(self, **estados: str) -> "RedBayesiana":
        """Cambia el estado de varios nodos sin animar. Las flechas que tocan
        un nodo inactivo se atenúan con él."""
        for id_, e in estados.items():
            self.nodos[id_].estilo(e)
        for (a, b), flecha in self.flechas.items():
            opacidad = min(ESTILOS_NODO[self.nodos[a].estado]["opacidad"],
                           ESTILOS_NODO[self.nodos[b].estado]["opacidad"])
            flecha.set_opacity(opacidad)
        return self

    def estados(self, **estados: str):
        """Animación: red.estados(alarma="activo", robo="inactivo").

        Anima la red entera (animar un nodo suelto parte la red en piezas
        dentro de la escena).
        """
        return self.animate.aplicar_estados(**estados)

    def restablecer(self):
        return self.estados(**{id_: "normal" for id_ in self.nodos})

    def aplicar_nombres(self, **nombres: str) -> "RedBayesiana":
        """Cambia nombres visibles sin animar; las flechas se ajustan a las cajas nuevas."""
        for id_, nombre in nombres.items():
            viejo = self.nodos[id_]
            nuevo = Nodo(nombre, viejo.estado).move_to(viejo.get_center())
            viejo.nombre = nombre
            viejo.caja.become(nuevo.caja)
            viejo.etiqueta.become(nuevo.etiqueta)
        for (a, b), flecha in self.flechas.items():
            if a in nombres or b in nombres:
                flecha.become(flecha_entre(self.nodos[a], self.nodos[b]))
        return self.aplicar_estados()  # become() restablece la opacidad de las flechas

    def renombrar(self, **nombres: str):
        """Animación: cambia nombres visibles (escena 10: Robo -> Falla del enlace, ...)."""
        return self.animate.aplicar_nombres(**nombres)


def red_alarma(escala: float = 1.0) -> RedBayesiana:
    """Red de la alarma (AIMA 13.1–13.3)."""
    dx, dy = 2.6 * escala, 1.7 * escala
    return RedBayesiana(
        {
            "robo": ("Robo", (-dx, dy)),
            "terremoto": ("Terremoto", (dx, dy)),
            "alarma": ("Alarma", (0, 0)),
            "camilo": ("Llama Camilo", (-dx, -dy)),
            "isabel": ("Llama Isabel", (dx, -dy)),
        },
        [("robo", "alarma"), ("terremoto", "alarma"), ("alarma", "camilo"), ("alarma", "isabel")],
    )


def red_aspersor(escala: float = 1.0) -> RedBayesiana:
    """Red del aspersor (AIMA 13.4–13.5)."""
    dx, dy = 2.4 * escala, 1.7 * escala
    return RedBayesiana(
        {
            "nublado": ("Nublado", (0, dy)),
            "aspersor": ("Aspersor", (-dx, 0)),
            "lluvia": ("Lluvia", (dx, 0)),
            "cesped": ("Césped mojado", (0, -dy)),
        },
        [("nublado", "aspersor"), ("nublado", "lluvia"), ("aspersor", "cesped"), ("lluvia", "cesped")],
    )


# --- Tablas de probabilidad condicional -------------------------------------


def tabla_cpt(encabezados: list[str], filas: list[list[str]], tam: int = TABLA_TAM_TEXTO) -> Table:
    """CPT con encabezado; tabla.get_rows()[i] permite resaltar filas (0 = encabezado)."""
    return Table(
        filas,
        col_labels=[texto(h, tam, TEXTO_SECUNDARIO) for h in encabezados],
        element_to_mobject=lambda s: texto(s, tam),
        include_outer_lines=False,
        line_config={"stroke_width": 1.5, "color": TABLA_LINEAS},
        h_buff=0.55,
        v_buff=0.28,
    )


def prob_previa(variable: str, valor: str, tam: int = TABLA_TAM_TEXTO + 4) -> Text:
    """Probabilidad de un nodo sin padres: "P(Robo) = 0,001"."""
    return texto(f"P({variable}) = {valor}", tam)


def tablas_alarma() -> dict[str, Mobject]:
    """CPT de la red de la alarma (escena 3), por id de nodo."""
    return {
        "robo": prob_previa("Robo", "0,001"),
        "terremoto": prob_previa("Terremoto", "0,002"),
        "alarma": tabla_cpt(
            ["Robo", "Terremoto", "P(Alarma)"],
            [["V", "V", "0,95"], ["V", "F", "0,94"], ["F", "V", "0,29"], ["F", "F", "0,001"]],
        ),
        "llamadas": tabla_cpt(
            ["Alarma", "P(Llama Camilo)", "P(Llama Isabel)"],
            [["V", "0,90", "0,70"], ["F", "0,05", "0,01"]],
        ),
    }


def tablas_aspersor() -> dict[str, Mobject]:
    """CPT de la red del aspersor (escena 8), por id de nodo."""
    return {
        "nublado": prob_previa("Nublado", "0,5"),
        "aspersor_lluvia": tabla_cpt(
            ["Nublado", "P(Aspersor)", "P(Lluvia)"],
            [["V", "0,10", "0,80"], ["F", "0,50", "0,20"]],
        ),
        "cesped": tabla_cpt(
            ["Aspersor", "Lluvia", "P(Césped mojado)"],
            [["V", "V", "0,99"], ["V", "F", "0,90"], ["F", "V", "0,90"], ["F", "F", "0,00"]],
        ),
    }


def _red_con_tablas(red: RedBayesiana, tablas: dict[str, Mobject], ancho: float, alto: float) -> VGroup:
    columna = VGroup(*tablas.values()).arrange(DOWN, buff=0.45)
    grupo = VGroup(red, columna).arrange(RIGHT, buff=1.0)
    return ajustar(grupo, ancho, alto).move_to(ORIGIN)


def red_alarma_con_tablas(ancho: float = ANCHO_UTIL, alto: float = ALTO_UTIL) -> VGroup:
    """Red de la alarma a la izquierda y sus CPT a la derecha (escenas 3, 4, 6).

    grupo[0] es la RedBayesiana y grupo[1] la columna de tablas. Cabe en
    ancho x alto: si algo más va en pantalla, pásale el espacio que le queda.
    """
    return _red_con_tablas(red_alarma(escala=0.85), tablas_alarma(), ancho, alto)


def red_aspersor_con_tablas(ancho: float = ANCHO_UTIL, alto: float = ALTO_UTIL) -> VGroup:
    """Red del aspersor a la izquierda y sus CPT a la derecha (escenas 8, 9)."""
    return _red_con_tablas(red_aspersor(escala=0.9), tablas_aspersor(), ancho, alto)


# --- Otros -------------------------------------------------------------------


def celular(mensaje: str | None = None) -> VGroup:
    """Celular con llamada entrante opcional ("Camilo llamando...")."""
    cuerpo = RoundedRectangle(width=1.7, height=3.2, corner_radius=0.25, stroke_color=TEXTO, stroke_width=3)
    pantalla = RoundedRectangle(
        width=1.45, height=2.7, corner_radius=0.12, stroke_width=0, fill_color=TEXTO_SECUNDARIO, fill_opacity=0.15
    )
    camara = Dot(radius=0.04, color=TEXTO_SECUNDARIO).move_to(cuerpo.get_top() + DOWN * 0.13)
    grupo = VGroup(cuerpo, pantalla, camara)
    if mensaje:
        # "Camilo llamando..." -> dos líneas para que se lea dentro de la pantalla.
        aviso = parrafo(mensaje.replace(" ", "\n", 1), 24, buff=0.1)
        if aviso.width > pantalla.width - 0.2:
            aviso.scale_to_fit_width(pantalla.width - 0.2)
        grupo.add(aviso.move_to(pantalla))
    return grupo
