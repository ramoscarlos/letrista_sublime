import sublime
import sublime_plugin

class ComentarLetraToggleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Obtener región (o regiones) seleccionadas
        selections = self.view.sel()
        # Bandera para saber si vamos a comentar o descomentar.
        comentar = None

        # Mostrar el contenido de cada región
        for i in range(len(selections)):
            result = []
            region = self.view.substr(self.view.line(selections[i]))
            for line in region.split('\n'):
                if len(line) >= 2:
                    # Determinar si se debe comentar o no en base a la
                    # primer línea con contenido.
                    if comentar == None:
                        if line[1] == ' ':
                            comentar = True
                        else:
                            comentar = False

                    # Realizar la sustitución en base a la función escogida.
                    if comentar == True and line[1] == ' ':
                        line = line[0] + '-' + line[2:]
                    elif comentar == False and line[1] == '-':
                        line = line[0] + ' ' + line[2:]

                # La línea se vuelve a colocar, igual o comentada.
                result.append(line)

            # Reemplazar el contenido de la región completa.
            self.view.replace(edit, self.view.line(selections[i]), '\n'.join(result))

    def is_enabled(self):
        return self.view.match_selector(0, "text.letra")