"""Sistema de diseño del video: colores, tipografía, tamaños y estilo de grafos.

Todas las escenas importan de aquí; no se escriben colores ni tamaños sueltos.
La resolución (1920x1080, 30 fps) está en manim.cfg, en la raíz del repo.
"""

from pathlib import Path

from manim import config

RAIZ = Path(__file__).resolve().parents[1]
DIR_ASSETS = RAIZ / "assets"
LOGO_UNAL = DIR_ASSETS / "logo_unal.png"

# --- Paleta ------------------------------------------------------------------

FONDO = "#0E1117"
TEXTO = "#ECEFF4"
TEXTO_SECUNDARIO = "#8B93A1"

# Acentos
NODO = "#58C4DD"        # azul: nodos de las redes
FLECHA = "#5CD0B3"      # verde azulado: flechas / aristas
RESALTADO = "#F4D35E"   # amarillo: énfasis, resultados, nodo activo

# Semánticos (✓ / ✗, rechazos, cortes)
POSITIVO = "#83C167"
NEGATIVO = "#FC6255"

config.background_color = FONDO

# --- Tipografía --------------------------------------------------------------

FUENTE_TITULO = "Segoe UI"
FUENTE_CUERPO = "Segoe UI"
# Las fórmulas usan MathTex (Computer Modern, vía LaTeX).

# Tamaños (font_size de Manim a 1080p)
TAM_TITULO = 60
TAM_SUBTITULO = 40
TAM_CUERPO = 32
TAM_PEQUENO = 24
TAM_FORMULA = 40

# --- Espaciado ---------------------------------------------------------------

MARGEN = 0.5            # distancia a los bordes del cuadro
ANCHO_UTIL = config.frame_width - 2 * MARGEN   # área de contenido
ALTO_UTIL = config.frame_height - 2 * MARGEN
SEPARACION = 0.35       # entre líneas / elementos relacionados

# --- Grafos ------------------------------------------------------------------

NODO_ALTO = 0.75
NODO_RELLENO_X = 0.35   # margen horizontal entre el nombre y el borde
NODO_RADIO_ESQUINA = 0.18
NODO_TAM_TEXTO = 26
NODO_GROSOR = 3

FLECHA_GROSOR = 4
FLECHA_PUNTA = 0.2
FLECHA_SEPARACION = 0.08  # hueco entre la flecha y el borde del nodo

# Variantes visuales de un nodo. "evidencia" = variable observada.
ESTILOS_NODO = {
    "normal": {"borde": NODO, "relleno": NODO, "opacidad_relleno": 0.12, "opacidad": 1.0},
    "activo": {"borde": RESALTADO, "relleno": RESALTADO, "opacidad_relleno": 0.25, "opacidad": 1.0},
    "evidencia": {"borde": NODO, "relleno": NODO, "opacidad_relleno": 0.55, "opacidad": 1.0},
    "inactivo": {"borde": NODO, "relleno": NODO, "opacidad_relleno": 0.05, "opacidad": 0.3},
}

# --- Tablas ------------------------------------------------------------------

TABLA_TAM_TEXTO = 24
TABLA_LINEAS = TEXTO_SECUNDARIO
