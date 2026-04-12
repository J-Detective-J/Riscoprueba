"""
manejador_errores.py
====================
Manejador personalizado de errores sintácticos para RISCO.

ANTLR por defecto imprime errores de sintaxis en stderr con un formato
genérico en inglés. Este módulo reemplaza ese comportamiento con mensajes
en español y un mecanismo para detectar si hubo errores.

Uso en el pipeline:
    El ManejadorErrores se registra en el lexer y/o el parser antes de
    parsear. Si ocurre un error de sintaxis, ANTLR llama a syntaxError()
    en lugar de su handler por defecto.

Ejemplo de integración (pendiente de conectar en risco.py):
    manejador = ManejadorErrores()
    lexer.removeErrorListeners()
    lexer.addErrorListener(manejador)
    parser.removeErrorListeners()
    parser.addErrorListener(manejador)

    arbol = parser.programa()

    if manejador.tiene_error:
        print("El programa contiene errores sintácticos.")
"""

import sys
from antlr4.error.ErrorListener import ErrorListener


class ManejadorErrores(ErrorListener):
    """
    Listener de errores personalizado para el lexer y parser de RISCO.

    Hereda de ErrorListener de ANTLR e intercepta los errores de sintaxis
    para mostrarlos en español y registrar si ocurrió algún error.

    Attributes:
        tiene_error (bool): True si se detectó al menos un error sintáctico
                            durante el análisis. Útil para abortar la
                            evaluación si el código es inválido.
    """

    def __init__(self):
        super().__init__()
        self.tiene_error = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """
        Se invoca automáticamente cuando ANTLR detecta un error de sintaxis.

        Marca tiene_error como True e imprime el error en stderr con
        formato localizado en español.

        Args:
            recognizer:      El lexer o parser que encontró el error.
            offendingSymbol: El token que causó el error (puede ser None en el lexer).
            line (int):      Número de línea donde ocurrió el error.
            column (int):    Columna donde ocurrió el error.
            msg (str):       Descripción del error generada por ANTLR.
            e:               La excepción de reconocimiento original (puede ser None).
        """
        self.tiene_error = True
        mensaje = f"Error sintáctico línea {line}:{column} - {msg}"
        print(mensaje, file=sys.stderr)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        """
        Llamado cuando ANTLR detecta ambigüedad en la gramática.
        Se ignora intencionalmente para no generar ruido en el output.
        """
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        """
        Llamado cuando ANTLR intenta el análisis con contexto completo
        por una posible ambigüedad. Se ignora intencionalmente.
        """
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        """
        Llamado cuando ANTLR detecta sensibilidad al contexto.
        Se ignora intencionalmente.
        """
        pass