"""Escena 12 — Referencias bibliográficas (sin voz, 15 s)."""

from manim import *

from escenas.comun import EscenaNarrada
from escenas.components import *
from escenas.style import *

REFERENCIAS = [
    "Russell, S. J., y Norvig, P. (2021). Probabilistic reasoning. En Artificial intelligence: A modern approach\n"
    "(4.ª ed., cap. 13, pp. 412–454). Pearson.",
    "Pearl, J. (1988). Probabilistic reasoning in intelligent systems: Networks of plausible inference.\n"
    "Morgan Kaufmann.",
    "Pearl, J. (2009). Causality: Models, reasoning, and inference (2.ª ed.). Cambridge University Press.",
    "Koller, D., y Friedman, N. (2009). Probabilistic graphical models: Principles and techniques. MIT Press.",
    "McEliece, R. J., MacKay, D. J. C., y Cheng, J.-F. (1998). Turbo decoding as an instance of Pearl's\n"
    "“belief propagation” algorithm. IEEE Journal on Selected Areas in Communications, 16(2), 140–152.",
    "Pradhan, M., Provan, G., Middleton, B., y Henrion, M. (1994). Knowledge engineering for large belief\n"
    "networks. En Proceedings of the Tenth Conference on Uncertainty in Artificial Intelligence (UAI-94).\n"
    "Morgan Kaufmann.",
]


class Escena12(EscenaNarrada):
    numero = 12

    def construct(self):
        cabecera = titulo("REFERENCIAS", TAM_SUBTITULO)
        refs = VGroup(*(parrafo(r, 20, alineacion=LEFT, buff=0.1) for r in REFERENCIAS))
        refs.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        aclaracion = nota("Nota: los ejemplos de diagnóstico de red y de la caché son ilustrativos "
                          "y fueron elaborados por el grupo.", 18)
        bloque = VGroup(cabecera, refs, aclaracion).arrange(DOWN, buff=0.45)
        ajustar(bloque).move_to(ORIGIN)
        self.play(FadeIn(cabecera), run_time=0.8)
        self.play(LaggedStart(*(FadeIn(r) for r in refs), lag_ratio=0.15), run_time=2)
        self.play(FadeIn(aclaracion), run_time=0.6)
        self.esperar_hasta(self.duracion_total - 1)
        self.play(FadeOut(bloque), run_time=1)
        self.terminar()
