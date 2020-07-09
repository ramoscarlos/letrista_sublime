import sublime
import sublime_plugin

from .common import procesarLetra

class TiempoRealViewEventListener(sublime_plugin.ViewEventListener):
    def on_modified_async(self):
        if not self.view.settings().has("preview_view_id"):
            return

        vistaPreview = self.recuperarVistaDePreview()
        if vistaPreview:
            vistaPreview.run_command("select_all")
            vistaPreview.run_command("right_delete")
            vistaPreview.run_command("append", {
                "characters": procesarLetra(self.view)
            })

    def recuperarVistaDePreview(self):
        preview_view_id = self.view.settings().get("preview_view_id")
        for vista in self.view.window().views():
            if vista.id() == preview_view_id:
                return vista

        return None