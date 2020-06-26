import sublime
import sublime_plugin

class LetraPreviewEventListener(sublime_plugin.ViewEventListener):
    def on_modified(self):
        print("hola")