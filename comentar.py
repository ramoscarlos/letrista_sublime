import sublime
import sublime_plugin

class ComentarCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Obtener región (o regiones) seleccionadas
        regions = self.view.sel()

        # Mostrar el contenido de cada región
        for i in range(len(regions)):
            result = []
            region = self.view.substr(self.view.line(regions[i]))
            for line in region.split('\n'):
                if len(line) >= 2:
                    if line[1] == ' ':
                        line = line[0] + '-' + line[2:]
                # La línea se vuelve a colocar, igual o comentada.
                result.append(line)

            # Reemplazar el contenido de la región completa.
            self.view.replace(edit, self.view.line(regions[i]), '\n'.join(result))

    def is_enabled(self):
        return self.view.match_selector(0, "text.letra")