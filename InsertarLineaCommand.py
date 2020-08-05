import sublime
import sublime_plugin

class InsertarLineaCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		selections = self.view.sel()
		for i in range(len(selections)):
			region = self.view.line(selections[i])
			self.view.insert(edit, region.b, "\nX 00 ")

			cursorPos = sublime.Region(region.b + 6, region.b + 6)

			# Remover región actual, a partir de la cual creamos nueva línea.
			selections.subtract(selections[i])
			# Agregar nueva posición en nueva línea.
			selections.add(cursorPos)