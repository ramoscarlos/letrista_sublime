import sublime
import sublime_plugin

from .letrista.letra import LetraEnMarkdown


def copiarTextoDeVista(view):
    """
    Esta función se encarga de obtener el texto completo
    de la vista, y regresarlo.

    Returns:
        Cadena de texto completo de la vista
    """
    region = sublime.Region(0, view.size())
    contenidoArchivo = view.substr(region)

    return contenidoArchivo

def procesarLetra(view):
    contenidoArchivo = copiarTextoDeVista(view)

    # Aquí se debe verificar primero el tipo de procesamiento a realizar.
    letra = LetraEnMarkdown(contenidoArchivo)
    textoProcesado = '\n'.join(letra.formatear())

    return textoProcesado

def setTwoColumnLayout(window):
    """
    Se encarga de correr el comando de set_layout para crear
    un formato de dos columnas, del 50% cada una.
    """
    window.run_command(
        "set_layout",
        {
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
        },
    )