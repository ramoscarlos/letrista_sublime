import sublime
import sublime_plugin

from .common import copiarTextoDeVista
from .letrista.letra import LetraEnMarkdown

class ContarPalabrasCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        contenidoArchivo = copiarTextoDeVista(self.view)
        letra = LetraEnMarkdown(contenidoArchivo)

        print(letra.cantidad_de_palabras)

    def is_enabled(self):
        return self.view.match_selector(0, "text.letra")