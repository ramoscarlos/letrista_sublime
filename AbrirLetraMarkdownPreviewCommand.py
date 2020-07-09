import sublime
import sublime_plugin

from .common import copiarTextoDeVista, setTwoColumnLayout, procesarLetra

class AbrirLetraMarkdownPreviewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Crear nueva vista sin líneas eliminadas
        ventana = self.view.window()
        # Crear distribución de dos columnas.
        setTwoColumnLayout(ventana)
        # Foco en columna derecha.
        ventana.focus_group(1)

        # Todo lo demás de crear vista e insertar contenido se mantiene.
        vistaPreview = ventana.new_file()
        vistaPreview.set_name('Preview de letra')
        vistaPreview.set_scratch(True)

        # Ajustes necesarios para determinar la función de procesamiento.
        self.view.settings().set("preview_view_id", vistaPreview.id())
        self.view.settings().set("letra_procesamiento", "markdown")

        # Estas dos cosas dependen del procesamiento.
        vistaPreview.set_syntax_file("Packages/Markdown/Markdown.sublime-syntax")
        vistaPreview.run_command('append', {
            "characters": procesarLetra(self.view),
        })


    def is_enabled(self):
        return self.view.match_selector(0, "text.letra")