import sublime
import sublime_plugin

class BorradorTextoPlanoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Seleccionar todo el texto.
        region = sublime.Region(0, self.view.size())
        file_content = self.view.substr(region)

        # Eliminar líneas con un "-" en la segunda posición
        result = []
        for line in file_content.split('\n'):
            if not (len(line) >= 2 and line[1] == '-'):
                result.append(line)

        # Crear nueva vista sin líneas eliminadas
        ventana = self.view.window()
        # Crear distribución de dos columnas.
        ventana.run_command(
            "set_layout",
            {
                "cols": [0.0, 0.5, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
            },
        )
        # Foco en columna derecha.
        ventana.focus_group(1)

        # Todo lo demás de crear vista e insertar contenido se mantiene.
        letraProcesadaFile = ventana.new_file()
        letraProcesadaFile.set_syntax_file(self.view.settings().get('syntax'))
        letraProcesadaFile.run_command('append', {
            "characters": '\n'.join(result),
        })


    def is_enabled(self):
        return self.view.match_selector(0, "text.letra")