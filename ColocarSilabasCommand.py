import sublime
import sublime_plugin

from .letrista.linea import Linea

class ColocarSilabasCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Obtener región (o regiones) seleccionadas
        selections = self.view.sel()

        # Mostrar el contenido de cada región
        for i in range(len(selections)):
            result = []
            region = self.view.substr(self.view.line(selections[i]))
            for line in region.split('\n'):
                linea = Linea(line)
                # La línea se vuelve a colocar, con rima y sílabas de ser necesario.
                result.append(linea.texto_con_rima_y_silabas)

            # Reemplazar el contenido de la región completa.
            self.view.replace(edit, self.view.line(selections[i]), '\n'.join(result))

    def is_enabled(self):
        return self.view.match_selector(0, "text.letra")