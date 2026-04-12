"""
risco.py
========
Punto de entrada del intérprete RISCO.

Este módulo contiene la clase principal RISCO que orquesta el proceso
completo de interpretación: lectura del código fuente, tokenización
(lexer), análisis sintáctico (parser) y evaluación (visitor).

Modos de uso:
    - Archivo: python src/risco.py ejemplos/programa.rc
    - Interactivo (REPL): python src/risco.py

Flujo de interpretación:
    código fuente (.rc)
        → InputStream        (ANTLR: convierte texto a stream de caracteres)
        → RISCOLexer         (tokenización: texto → tokens)
        → CommonTokenStream  (buffer de tokens)
        → RISCOParser        (análisis sintáctico: tokens → AST)
        → VisitanteEvaluador (evaluación: recorre el AST y ejecuta la lógica)
"""

import sys
import os

# Permite importar módulos desde el directorio raíz del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from antlr4 import *
from gramaticas.RISCOLexer import RISCOLexer
from gramaticas.RISCOParser import RISCOParser
from src.visitante_evaluador import VisitanteEvaluador


class RISCO:
    """
    Intérprete principal del lenguaje RISCO.

    Coordina el pipeline completo de interpretación: desde el código
    fuente hasta la ejecución, pasando por lexer, parser y visitor.

    El visitor mantiene el estado del programa (variables) entre
    llamadas, lo que permite que el modo interactivo recuerde
    variables declaradas en líneas anteriores.

    Attributes:
        visitante (VisitanteEvaluador): Instancia del visitor que evalúa
            el AST y mantiene la memoria del programa.
    """

    def __init__(self,modo_interactivo=False):
        self.visitante = VisitanteEvaluador(modo_interactivo=modo_interactivo)

    def ejecutar_archivo(self, ruta_archivo: str) -> None:
        """
        Lee y ejecuta un archivo de código RISCO (.rc).

        Args:
            ruta_archivo (str): Ruta al archivo .rc a ejecutar.

        Raises:
            SystemExit: Si el archivo no existe o ocurre un error de lectura.
        """
        if not ruta_archivo.endswith('.rc'):
            print(f"Error: '{ruta_archivo}' no tiene extensión .rc")
            sys.exit(1)
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                codigo = f.read()
            self._ejecutar_codigo(codigo)
        except FileNotFoundError:
            print(f"Error: No se encuentra el archivo '{ruta_archivo}'")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    def _ejecutar_codigo(self, codigo: str) -> None:
        """
        Ejecuta una cadena de código RISCO directamente.

        Método interno usado tanto por ejecutar_archivo() como por
        el modo interactivo. Garantiza que el código termine en
        salto de línea (requerido por la gramática).

        Pasos:
            1. Asegura que el código termina con '\\n'.
            2. Crea un InputStream con el código.
            3. Tokeniza con RISCOLexer.
            4. Parsea con RISCOParser obteniendo el AST.
            5. Evalúa el AST con VisitanteEvaluador.

        Args:
            codigo (str): Código fuente RISCO a ejecutar.
        """
        if not codigo.endswith('\n'):
            codigo += '\n'

        entrada = InputStream(codigo)
        lexer = RISCOLexer(entrada)
        tokens = CommonTokenStream(lexer)
        parser = RISCOParser(tokens)

        try:
            arbol = parser.programa()
        except Exception as e:
            print(f"Error durante el parseo: {e}")
            return

        try:
            self.visitante.visit(arbol)
        except Exception as e:
            print(f"Error en evaluación: {e}")

    def modo_interactivo(self) -> None:
        """
        Inicia el modo REPL (Read-Eval-Print Loop) interactivo.

        Permite ejecutar expresiones RISCO línea a línea. El estado
        del programa (variables declaradas) persiste entre líneas
        porque se reutiliza la misma instancia del visitor.

        Comandos especiales:
            salir / exit / quit → termina el REPL
            Ctrl+C              → termina el REPL

        Limitación:
            Solo soporta expresiones de una línea. Para bloques
            multilínea (for, if, while) usar archivos .rc.
        """
        print("RISCO v1.0 - Modo interactivo")
        print("Escribe expresiones o 'salir' para terminar")
        print("-" * 50)

        while True:
            try:
                linea = input("risco> ").strip()

                if not linea:
                    continue

                if linea.lower() in ('salir', 'exit', 'quit'):
                    break

                self._ejecutar_codigo(linea + '\n')

            except KeyboardInterrupt:
                print("\n¡Hasta luego!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """
    Función principal. Determina el modo de ejecución según los argumentos:
      - Con argumento: ejecuta el archivo indicado.
      - Sin argumento: inicia el modo interactivo.

    Uso:
        python src/risco.py                        # modo interactivo
        python src/risco.py ejemplos/programa.rc   # ejecutar archivo
    """
    if len(sys.argv) > 1:
        lenguaje = RISCO(modo_interactivo=False)
        lenguaje.ejecutar_archivo(sys.argv[1])
    else:
        lenguaje = RISCO(modo_interactivo=True)
        lenguaje.modo_interactivo()


if __name__ == "__main__":
    main()