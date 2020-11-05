"""
PENDIENTES:
    - Si el grupo de previsualizaciones se queda vacío, cerrar el grupo.
    - Al querer abrir una letra con Ctl+Shift+P, se abre en automático el preview
      y ya no deja seguir escribiendo para encontrar el archivo (corregir el focus)
"""

import sublime
import sublime_plugin

from .common import procesarLetra

class TiempoRealViewEventListener(sublime_plugin.ViewEventListener):
    def on_load_async(self):
        """
        Al abrir una letra, se abre su preview.
        """
        self.view.run_command('abrir_letra_markdown_preview')

    def on_pre_close(self):
        """
        Si hay una vista asociada abierta, la cierra.
        Esto se hace en pre-close, de lo contrario hay error al encontrar la vista.
        """
        if not self.view.settings().has("preview_view_id"):
            return

        vistaPreview = self.__recuperarVistaDePreview()
        vistaPreview.close()

    def on_modified_async(self):
        """
        Este método tiene como objetivo actualizar la vista previa de una letra,
        siempre y cuando se encuentre la vista asociada.
        """
        if not self.view.settings().has("preview_view_id"):
            return

        vistaPreview = self.__recuperarVistaDePreview()
        if vistaPreview:
            # Activar habilidad de escritura
            vistaPreview.set_read_only(False)

            vistaPreview.run_command("select_all")
            vistaPreview.run_command("right_delete")
            vistaPreview.run_command("append", {
                "characters": procesarLetra(self.view)
            })

            # Evitar que se pueda escribir en la vista de visualización.
            vistaPreview.set_read_only(True)

    def __recuperarVistaDePreview(self):
        preview_view_id = self.view.settings().get("preview_view_id")
        for vista in self.view.window().views():
            if vista.id() == preview_view_id:
                return vista

        return None