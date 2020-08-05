import sublime
import sublime_plugin

class ClonarComentarLineaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
    	selections = self.view.sel()

    	for i in range(len(selections)):
    		region = self.view.substr(self.view.line(selections[i]))
    		self.view.run_command('duplicate_line')
    		self.view.run_command('comentar_letra_toggle')