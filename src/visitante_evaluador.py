"""
visitante_evaluador.py
======================
Implementa el patrón Visitor sobre el árbol de sintaxis (AST) generado
por ANTLR para el lenguaje RISCO.

El visitor recorre el árbol nodo por nodo y ejecuta la lógica de cada
construcción del lenguaje: declaraciones, asignaciones, expresiones,
bucles, llamadas a función, built-ins, casteo e indexación.
"""

import gc
from functools import reduce as py_reduce
from antlr4 import *
from gramaticas.RISCOParser import RISCOParser
from gramaticas.RISCOVisitor import RISCOVisitor


# ──────────────────────────────────────────────────────────────
#  Excepción de control para implementar 'return'
# ──────────────────────────────────────────────────────────────

class _ReturnException(Exception):
    """
    Excepción de control interna que implementa el flujo de 'return'.

    Se lanza cuando el visitor encuentra una sentencia return_stmt y
    es capturada por visitDeclaracion_funcion al terminar la ejecución
    del cuerpo de la función.

    Atributos:
        valor: El valor que devuelve la función.
    """
    def __init__(self, valor):
        self.valor = valor


# ──────────────────────────────────────────────────────────────
#  Representación interna de una función RISCO
# ──────────────────────────────────────────────────────────────

class FuncionRISCO:
    """
    Representa una función definida por el usuario en RISCO.

    Almacena los parámetros formales, el cuerpo (como nodos del AST)
    y una referencia al visitor para poder ejecutar el cuerpo.

    Atributos:
        params (list[str]): Nombres de los parámetros formales.
        cuerpo_expr:  Nodo AST de la expresión (forma corta) o None.
        cuerpo_stmts: Lista de nodos AST de sentencias (forma larga) o None.
        closure (dict): Copia de la memoria en el momento de la definición,
                        usada para capturar variables del entorno (closure).
    """
    def __init__(self, params, cuerpo_expr, cuerpo_stmts, closure):
        self.params = params          # list[str]
        self.cuerpo_expr = cuerpo_expr    # nodo AST expresion | None
        self.cuerpo_stmts = cuerpo_stmts  # list de nodos sentencia | None
        self.closure = closure        # dict de variables capturadas


# ──────────────────────────────────────────────────────────────
#  Visitor principal
# ──────────────────────────────────────────────────────────────

class VisitanteEvaluador(RISCOVisitor):
    """
    Visitor que evalúa el AST de un programa RISCO.

    Mantiene el estado del programa en dos diccionarios:
      - memoria:   variables → valores
      - funciones: nombre → FuncionRISCO

    Los built-ins están registrados en self._builtins y se resuelven
    en visitLlamada_funcion antes de buscar en self.funciones.

    Atributos:
        memoria  (dict): Variables del programa.
        funciones (dict): Funciones definidas por el usuario.
        vals     (set):  Nombres de variables inmutables (val).
        ultimo_resultado: Último valor evaluado (útil para el REPL).
        modo_interactivo (bool): Si True, imprime expresiones sueltas.
    """

    def __init__(self, modo_interactivo=False):
        self.memoria = {}
        self.funciones = {}
        self.vals = set()
        self.ultimo_resultado = None
        self.modo_interactivo = modo_interactivo

    # ══════════════════════════════════════════════════════════
    #  PROGRAMA
    # ══════════════════════════════════════════════════════════

    def visitPrograma(self, ctx: RISCOParser.ProgramaContext):
        """
        Punto de entrada del visitor.

        Recorre todas las sentencias del programa en orden.
        Los errores en una sentencia se capturan e imprimen sin detener
        la ejecución de las sentencias siguientes.

        Returns:
            El último resultado evaluado (útil en modo interactivo).
        """
        for sentencia in ctx.sentencia():
            try:
                resultado = self.visit(sentencia)
                if resultado is not None:
                    self.ultimo_resultado = resultado
            except Exception as e:
                print(f"Error: {e}")
        return self.ultimo_resultado

    # ══════════════════════════════════════════════════════════
    #  SENTENCIAS
    # ══════════════════════════════════════════════════════════

    def visitDeclaracion_variable(self, ctx: RISCOParser.Declaracion_variableContext):
        """
        Declara una nueva variable en memoria.

        - val: inmutable. Error si se intenta redeclarar.
        - var: mutable. Puede reasignarse con visitAsignacion.
        """
        nombre = ctx.IDENTIFICADOR().getText()
        valor = self.visit(ctx.expresion())

        if nombre in self.memoria:
            raise Exception(f"'{nombre}' ya está definida y no puede redeclararse")

        self.memoria[nombre] = valor
        if ctx.VAL() is not None:
            self.vals.add(nombre)
        return None

    def visitAsignacion(self, ctx: RISCOParser.AsignacionContext):
        """
        Reasigna el valor de una variable var existente.

        Raises:
            Exception: Si la variable no existe o es val (inmutable).
        """
        nombre = ctx.IDENTIFICADOR().getText()
        valor = self.visit(ctx.expresion())

        if nombre not in self.memoria:
            raise Exception(f"Variable '{nombre}' no definida")
        if nombre in self.vals:
            raise Exception(f"'{nombre}' es inmutable (val), no se puede reasignar")
        self.memoria[nombre] = valor
        return valor

    def visitExpresion_stmt(self, ctx: RISCOParser.Expresion_stmtContext):
        """
        Evalúa una expresión suelta.

        En modo interactivo imprime el resultado con el prefijo '>'.
        """
        resultado = self.visit(ctx.expresion())
        if self.modo_interactivo and resultado is not None:
            print(f"> {resultado}")
        return resultado

    def visitPrint_stmt(self, ctx: RISCOParser.Print_stmtContext):
        """
        Ejecuta la sentencia print(expr).

        Convierte el valor con _a_texto(), que sigue convenciones de Python:
          - None  → "None"
          - bool  → "True" / "False"
          - list  → "[e1, e2, ...]"
          - resto → str() de Python
        """
        valor = self.visit(ctx.expresion())
        print(self._a_texto(valor))
        return None

    # ── Bucles ────────────────────────────────────────────────

    def visitFor_stmt(self, ctx: RISCOParser.For_stmtContext):
        """
        Ejecuta un bucle for sobre un iterable (lista o string).

        La variable de iteración existe solo dentro del bloque y se
        elimina al salir para respetar el scope.
        """
        nombre_var = ctx.IDENTIFICADOR().getText()
        iterable = self.visit(ctx.expresion())

        if not isinstance(iterable, (list, str)):
            raise Exception(f"'{iterable}' no es iterable en for")

        for elemento in iterable:
            self.memoria[nombre_var] = elemento
            for sentencia in ctx.sentencia():
                try:
                    self.visit(sentencia)
                except _ReturnException:
                    raise  # propagar return hacia arriba
                except Exception as e:
                    print(f"Error en for: {e}")

        if nombre_var in self.memoria:
            del self.memoria[nombre_var]
        return None

    def visitWhile_stmt(self, ctx: RISCOParser.While_stmtContext):
        """
        Ejecuta un bucle while.

        Evalúa la condición antes de cada iteración.
        """
        while True:
            condicion = self.visit(ctx.expresion())
            if not isinstance(condicion, bool):
                raise Exception(
                    f"Error de tipos: la condición del 'while' debe ser Bool, "
                    f"no '{type(condicion).__name__}'"
                )
            if not condicion:
                break
            for sentencia in ctx.sentencia():
                self.visit(sentencia)
        return None

    # ── Condicional ───────────────────────────────────────────

    def visitIf_stmt(self, ctx: RISCOParser.If_stmtContext):
        """
        Evalúa un condicional if / elif* / else?.

        Evalúa la condición del if; si es true ejecuta su bloque y termina.
        Si no, evalúa cada elif en orden. Si ninguno aplica y hay else,
        ejecuta ese bloque.
        """
        expresiones = ctx.expresion()
        bloques = self._obtener_bloques_if(ctx)

        # Bloque if
        condicion = self.visit(expresiones[0])
        if not isinstance(condicion, bool):
            raise Exception(
                f"Error de tipos: la condición del 'if' debe ser Bool, "
                f"no '{type(condicion).__name__}'"
            )
        if condicion:
            for s in bloques[0]:
                self.visit(s)
            return None

        # Bloques elif
        num_elif = len(expresiones) - 1
        for i in range(num_elif):
            condicion = self.visit(expresiones[i + 1])
            if not isinstance(condicion, bool):
                raise Exception(
                    f"La condición del 'elif' debe ser Bool, "
                    f"no '{type(condicion).__name__}'"
                )
            if condicion:
                for s in bloques[i + 1]:
                    self.visit(s)
                return None

        # Bloque else
        if ctx.ELSE() is not None:
            for s in bloques[-1]:
                self.visit(s)

        return None

    def _obtener_bloques_if(self, ctx: RISCOParser.If_stmtContext):
        """
        Separa las sentencias del if_stmt en bloques según IF/ELIF/ELSE/END.

        Returns:
            list[list]: Índice 0 = bloque if, siguientes = elif, último = else.
        """
        bloques = []
        bloque_actual = []

        for i in range(ctx.getChildCount()):
            hijo = ctx.getChild(i)
            texto = hijo.getText()

            if texto in ('if', 'elif', 'else', 'end'):
                if texto in ('elif', 'else', 'end') and bloque_actual is not None:
                    bloques.append(bloque_actual)
                    bloque_actual = []
                if texto == 'end':
                    bloque_actual = None
            elif hasattr(hijo, 'getRuleIndex'):
                if bloque_actual is not None:
                    bloque_actual.append(hijo)

        return bloques

    # ── Funciones definidas por el usuario ───────────────────

    def visitDeclaracion_funcion(self, ctx: RISCOParser.Declaracion_funcionContext):
        """
        Registra una función definida por el usuario en self.funciones.

        Soporta dos formas:
          - Corta:  nombre(p1, p2) => expresion
          - Larga:  nombre(p1, p2) =>
                        sentencias*
                    end

        El closure captura una copia de la memoria actual para que la
        función pueda acceder a las variables del entorno donde fue
        definida (scoping léxico simplificado).
        """
        nombre = ctx.IDENTIFICADOR().getText()
        params = []
        if ctx.lista_params():
            for p in ctx.lista_params().IDENTIFICADOR():
                params.append(p.getText())

        # Detectar forma corta vs. larga buscando si hay expresion directa
        cuerpo_expr = None
        cuerpo_stmts = None

        if ctx.expresion():
            # forma corta
            cuerpo_expr = ctx.expresion()
        else:
            # forma larga — recoger todas las sentencias
            cuerpo_stmts = list(ctx.sentencia())

        closure = dict(self.memoria)  # captura léxica
        self.funciones[nombre] = FuncionRISCO(params, cuerpo_expr, cuerpo_stmts, closure)
        return None

    def visitReturn_stmt(self, ctx: RISCOParser.Return_stmtContext):
        """
        Ejecuta una sentencia return.

        Lanza _ReturnException para saltar fuera del cuerpo de la función.
        """
        valor = self.visit(ctx.expresion())
        raise _ReturnException(valor)

    def _llamar_funcion(self, funcion, argumentos):
        """
        Ejecuta el cuerpo de una FuncionRISCO con los argumentos dados.

        Crea un entorno local combinando el closure con los parámetros
        reales. Restaura la memoria global al terminar.

        Args:
            funcion (FuncionRISCO): La función a ejecutar.
            argumentos (list): Lista de valores para los parámetros.

        Returns:
            El valor devuelto por la función (último resultado o return).

        Raises:
            Exception: Si el número de argumentos no coincide.
        """
        if len(argumentos) != len(funcion.params):
            raise Exception(
                f"Se esperaban {len(funcion.params)} argumentos, "
                f"se recibieron {len(argumentos)}"
            )

        # Guardar memoria global y crear entorno local
        memoria_anterior = self.memoria
        entorno_local = dict(funcion.closure)
        for nombre, valor in zip(funcion.params, argumentos):
            entorno_local[nombre] = valor
        self.memoria = entorno_local

        resultado = None
        try:
            if funcion.cuerpo_expr is not None:
                # Forma corta: evaluar la expresión directamente
                resultado = self.visit(funcion.cuerpo_expr)
            else:
                # Forma larga: ejecutar sentencias hasta el final o return
                for sentencia in funcion.cuerpo_stmts:
                    self.visit(sentencia)
        except _ReturnException as ret:
            resultado = ret.valor
        finally:
            self.memoria = memoria_anterior

        return resultado

    # ══════════════════════════════════════════════════════════
    #  EXPRESIONES
    # ══════════════════════════════════════════════════════════

    def visitExpresion(self, ctx: RISCOParser.ExpresionContext):
        """
        Punto de entrada de la jerarquía de expresiones.

        Si la expresión es una lambda anónima `(p1, p2) => cuerpo`,
        crea y devuelve un FuncionRISCO con closure actual.
        En caso contrario delega a or_logico.
        """
        # Detectar lambda: primer hijo es '('
        if ctx.getChildCount() >= 3 and ctx.getChild(0).getText() == '(':
            # Recoger parámetros
            params = []
            if ctx.lista_params():
                for p in ctx.lista_params().IDENTIFICADOR():
                    params.append(p.getText())
            cuerpo_expr = ctx.expresion()
            closure = dict(self.memoria)
            return FuncionRISCO(params, cuerpo_expr, None, closure)

        return self.visit(ctx.or_logico())

    def visitOr_logico(self, ctx: RISCOParser.Or_logicoContext):
        """Evalúa el operador lógico OR (||), cortocircuito."""
        resultado = self.visit(ctx.and_logico(0))
        for i in range(1, len(ctx.and_logico())):
            if not isinstance(resultado, bool):
                raise Exception(
                    f"Error de tipos: '||' solo opera sobre Bool, no sobre '{type(resultado).__name__}'"
                )
            if resultado:          # cortocircuito
                return True
            valor = self.visit(ctx.and_logico(i))
            if not isinstance(valor, bool):
                raise Exception(
                    f"Error de tipos: '||' solo opera sobre Bool, no sobre '{type(valor).__name__}'"
                )
            resultado = resultado or valor
        return resultado

    def visitAnd_logico(self, ctx: RISCOParser.And_logicoContext):
        """Evalúa el operador lógico AND (&&), cortocircuito."""
        resultado = self.visit(ctx.igualdad(0))
        for i in range(1, len(ctx.igualdad())):
            if not isinstance(resultado, bool):
                raise Exception(
                    f"Error de tipos: '&&' solo opera sobre Bool, no sobre '{type(resultado).__name__}'"
                )
            if not resultado:      # cortocircuito
                return False
            valor = self.visit(ctx.igualdad(i))
            if not isinstance(valor, bool):
                raise Exception(
                    f"Error de tipos: '&&' solo opera sobre Bool, no sobre '{type(valor).__name__}'"
                )
            resultado = resultado and valor
        return resultado

    def visitIgualdad(self, ctx: RISCOParser.IgualdadContext):
        """
        Evalúa igualdad (==) y desigualdad (!=).

        RISCO requiere que ambos operandos sean del mismo tipo.
        Excepción: null puede compararse con cualquier tipo.
        """
        if ctx.getChildCount() == 1:
            return self.visit(ctx.relacional(0))
        izq = self.visit(ctx.relacional(0))
        op  = ctx.getChild(1).getText()
        der = self.visit(ctx.relacional(1))

        # Permitir comparación con null independientemente del tipo
        if izq is not None and der is not None and type(izq) != type(der):
            raise Exception(
                f"Error de tipos: '{op}' no puede comparar "
                f"'{type(izq).__name__}' y '{type(der).__name__}'"
            )
        if op == '==':
            return izq == der
        if op == '!=':
            return izq != der

    def visitRelacional(self, ctx: RISCOParser.RelacionalContext):
        """Evalúa >, <, >=, <= sobre números (no Bool)."""
        if ctx.getChildCount() == 1:
            return self.visit(ctx.suma(0))
        izq = self.visit(ctx.suma(0))
        op  = ctx.getChild(1).getText()
        der = self.visit(ctx.suma(1))

        if isinstance(izq, bool) or isinstance(der, bool) or \
                not isinstance(izq, (int, float)) or not isinstance(der, (int, float)):
            raise Exception(
                f"Error de tipos: '{op}' solo opera sobre números, "
                f"no sobre '{type(izq).__name__}' y '{type(der).__name__}'"
            )
        if op == '>':  return izq > der
        if op == '<':  return izq < der
        if op == '>=': return izq >= der
        if op == '<=': return izq <= der

    def visitSuma(self, ctx: RISCOParser.SumaContext):
        """
        Evalúa suma (+) y resta (-).

        El operador '+' soporta exactamente tres combinaciones de tipos:
          - Num/Decimal + Num/Decimal → suma aritmética
          - str + str                 → concatenación de strings
          - list + list               → concatenación de listas
        Cualquier otra combinación (str+num, num+str, null+num, bool+any…)
        lanza "Error de tipos".

        El operador '-' solo opera sobre números (no Bool, no str, no None).
        """
        if ctx.getChildCount() == 1:
            return self.visit(ctx.comparacion(0))

        resultado = self.visit(ctx.comparacion(0))
        for i in range(1, len(ctx.comparacion())):
            operador = ctx.getChild(2 * i - 1).getText()
            valor = self.visit(ctx.comparacion(i))

            if operador == '+':
                if isinstance(resultado, bool) or isinstance(valor, bool):
                    raise Exception("Error de tipos: '+' no está definido para Bool")
                # str + str → concatenación
                if isinstance(resultado, str) and isinstance(valor, str):
                    resultado = resultado + valor
                # list + list → concatenación
                elif isinstance(resultado, list) and isinstance(valor, list):
                    resultado = resultado + valor
                # num + num → suma aritmética (int y float, pero no bool)
                elif isinstance(resultado, (int, float)) and isinstance(valor, (int, float)):
                    resultado = resultado + valor
                else:
                    raise Exception(
                        f"Error de tipos: '+' no puede operar "
                        f"'{type(resultado).__name__}' y '{type(valor).__name__}'"
                    )
            elif operador == '-':
                if isinstance(resultado, bool) or isinstance(valor, bool) or \
                        not isinstance(resultado, (int, float)) or \
                        not isinstance(valor, (int, float)):
                    raise Exception("Error de tipos: '-' solo opera sobre números")
                resultado = resultado - valor

        return resultado

    def visitComparacion(self, ctx: RISCOParser.ComparacionContext):
        """Evalúa el operador de pertenencia 'in'."""
        izquierda = self.visit(ctx.termino(0))
        if ctx.getChildCount() == 1:
            return izquierda
        derecha = self.visit(ctx.termino(1))
        if not isinstance(derecha, (list, str)):
            raise Exception("'in' requiere una lista o string a la derecha")
        return izquierda in derecha

    def visitTermino(self, ctx: RISCOParser.TerminoContext):
        """Evalúa *, / y % sobre números."""
        if ctx.getChildCount() == 1:
            return self.visit(ctx.potencia(0))

        resultado = self.visit(ctx.potencia(0))
        for i in range(1, len(ctx.potencia())):
            operador = ctx.getChild(2 * i - 1).getText()
            valor = self.visit(ctx.potencia(i))

            if isinstance(resultado, bool) or isinstance(valor, bool) or \
                    not isinstance(resultado, (int, float)) or \
                    not isinstance(valor, (int, float)):
                raise Exception(
                    f"Error de tipos: '{operador}' solo opera sobre números"
                )
            if operador == '*':
                resultado *= valor
            elif operador == '/':
                if valor == 0:
                    raise Exception("División por cero")
                resultado /= valor
            elif operador == '%':
                if valor == 0:
                    raise Exception("Módulo por cero")
                resultado %= valor
        return resultado

    def visitPotencia(self, ctx: RISCOParser.PotenciaContext):
        """
        Evalúa potencia (^) con asociatividad derecha.
        2 ^ 3 ^ 2  →  2 ^ (3^2)  =  2^9  =  512.
        """
        if ctx.getChildCount() == 1:
            return self.visit(ctx.acceso())

        base = self.visit(ctx.acceso())
        exp  = self.visit(ctx.potencia())

        if isinstance(base, bool) or isinstance(exp, bool) or \
                not isinstance(base, (int, float)) or not isinstance(exp, (int, float)):
            raise Exception("Error de tipos: '^' solo opera sobre números")

        return base ** exp

    def visitAcceso(self, ctx: RISCOParser.AccesoContext):
        """
        Evalúa indexación de listas y strings: lista[i], lista[i][j], etc.

        Soporta índices negativos (lista[-1] → último elemento).
        El primario se evalúa primero; luego cada par de corchetes aplica
        una indexación adicional sobre el resultado anterior.

        Raises:
            Exception: Si el índice está fuera de rango o el valor no es indexable.
        """
        resultado = self.visit(ctx.primario())

        # ctx.expresion() devuelve la lista de todas las expresiones de índice
        for expr_indice in ctx.expresion():
            indice = self.visit(expr_indice)

            if not isinstance(indice, int) or isinstance(indice, bool):
                raise Exception(
                    f"El índice debe ser Num (entero), no '{type(indice).__name__}'"
                )
            if not isinstance(resultado, (list, str)):
                raise Exception(
                    f"No se puede indexar un valor de tipo '{type(resultado).__name__}'"
                )
            if indice < -len(resultado) or indice >= len(resultado):
                raise Exception(
                    f"Índice {indice} fuera de rango para una colección "
                    f"de longitud {len(resultado)}"
                )
            resultado = resultado[indice]

        return resultado

    def visitPrimario(self, ctx: RISCOParser.PrimarioContext):
        """
        Evalúa valores primarios: literales, identificadores,
        llamadas a función, casteos, expresiones agrupadas y unarios.
        """
        if ctx.NUMERO():
            return int(ctx.NUMERO().getText())

        if ctx.DECIMAL():
            return float(ctx.DECIMAL().getText())

        if ctx.STRING():
            texto = ctx.STRING().getText()
            # Quitar comillas y procesar secuencias de escape
            interior = texto[1:-1]
            interior = interior.replace('\\"', '"')
            interior = interior.replace('\\n', '\n')
            interior = interior.replace('\\t', '\t')
            interior = interior.replace('\\\\', '\\')
            return interior

        if ctx.BOOLEANO():
            return ctx.BOOLEANO().getText() == 'true'

        if ctx.NULL():
            return None

        if ctx.lista():
            return self.visit(ctx.lista())

        if ctx.llamada_funcion():
            return self.visit(ctx.llamada_funcion())

        if ctx.casteo():
            return self.visit(ctx.casteo())

        if ctx.IDENTIFICADOR():
            nombre = ctx.IDENTIFICADOR().getText()
            # Primero buscar en variables
            if nombre in self.memoria:
                return self.memoria[nombre]
            # Luego buscar en funciones (para poder pasar funciones como argumentos)
            if nombre in self.funciones:
                return self.funciones[nombre]
            raise Exception(f"'{nombre}' no definida")

        # Expresión agrupada: ( expresion )
        if ctx.getChildCount() == 3 and ctx.getChild(0).getText() == '(':
            return self.visit(ctx.expresion())

        # Negación unaria: -primario
        if ctx.getChild(0).getText() == '-':
            val = self.visit(ctx.primario())
            if isinstance(val, bool) or not isinstance(val, (int, float)):
                raise Exception("Error de tipos: '-' unario solo opera sobre números")
            return -val

        # Negación lógica: !primario
        if ctx.getChild(0).getText() == '!':
            val = self.visit(ctx.primario())
            if not isinstance(val, bool):
                raise Exception(
                    f"Error de tipos: '!' solo opera sobre Bool, no sobre '{type(val).__name__}'"
                )
            return not val

        return None

    # ══════════════════════════════════════════════════════════
    #  COLECCIONES
    # ══════════════════════════════════════════════════════════

    def visitLista(self, ctx: RISCOParser.ListaContext):
        """Evalúa una lista literal [e1, e2, ...]."""
        return [self.visit(expr) for expr in ctx.expresion()]

    # ══════════════════════════════════════════════════════════
    #  LLAMADAS A FUNCIÓN
    # ══════════════════════════════════════════════════════════

    def visitLlamada_funcion(self, ctx: RISCOParser.Llamada_funcionContext):
        """
        Resuelve y ejecuta una llamada a función.

        Orden de resolución:
          1. Built-ins del lenguaje (long, range, map, filter, reduce, unwrap, free)
          2. Funciones definidas por el usuario en self.funciones
          3. Funciones almacenadas como variables en memoria (parámetros de orden superior)

        Raises:
            Exception: Si el nombre no corresponde a ninguna función conocida.
        """
        # Detectar qué tipo de llamada es
        if ctx.LONG_F():
            nombre = 'long'
        elif ctx.RANGE_F():
            nombre = 'range'
        elif ctx.MAP_F():
            nombre = 'map'
        elif ctx.FILTER_F():
            nombre = 'filter'
        elif ctx.REDUCE_F():
            nombre = 'reduce'
        elif ctx.UNWRAP_F():
            nombre = 'unwrap'
        elif ctx.FREE_F():
            nombre = 'free'
        elif ctx.INPUT_F():
            nombre = 'input'
        else:
            # Puede ser llamada simple nombre(args) o módulo.función(args)
            identificadores = ctx.IDENTIFICADOR()
            if len(identificadores) == 2:
                # notación de módulo: mat.mul → "mat_mul"
                nombre = identificadores[0].getText() + '_' + identificadores[1].getText()
            else:
                nombre = identificadores[0].getText()
        
        args_raw = []
        if ctx.lista_args():
            for arg_ctx in ctx.lista_args().argumento():
                args_raw.append(self.visit(arg_ctx.expresion()))

        # 1. Intentar resolver como built-in
        resultado_builtin = self._intentar_builtin(nombre, args_raw)
        if resultado_builtin is not _NO_ES_BUILTIN:
            return resultado_builtin

        # 2. Función definida por el usuario (en self.funciones)
        if nombre in self.funciones:
            return self._llamar_funcion(self.funciones[nombre], args_raw)
        
        # 3. Función almacenada como variable en memoria (ej: parámetros de orden superior)
        if nombre in self.memoria:
            func = self.memoria[nombre]
            if isinstance(func, FuncionRISCO):
                return self._llamar_funcion(func, args_raw)
            elif callable(func):
                return func(*args_raw)

        raise Exception(f"Función '{nombre}' no definida")

    # ══════════════════════════════════════════════════════════
    #  BUILT-INS
    # ══════════════════════════════════════════════════════════

    def _intentar_builtin(self, nombre, args):
        """
        Despacha la llamada a la función built-in correspondiente.

        Returns:
            El valor del built-in, o el centinela _NO_ES_BUILTIN si
            el nombre no corresponde a ningún built-in.
        """
        dispatch = {
            'long':   self._builtin_long,
            'range':  self._builtin_range,
            'map':    self._builtin_map,
            'filter': self._builtin_filter,
            'reduce': self._builtin_reduce,
            'unwrap': self._builtin_unwrap,
            'free':   self._builtin_free,
            'input':  self._builtin_input,
        }
        if nombre in dispatch:
            return dispatch[nombre](args)
        return _NO_ES_BUILTIN

    def _builtin_long(self, args):
        """
        long(lista) → Num

        Devuelve el número de elementos de una lista o el número de
        caracteres de un string.

        Ejemplo:
            long([1, 2, 3])   → 3
            long("hola")      → 4
            long([])          → 0
        """
        if len(args) != 1:
            raise Exception(f"long() requiere 1 argumento, recibió {len(args)}")
        valor = args[0]
        if not isinstance(valor, (list, str)):
            raise Exception(
                f"long() requiere una lista o string, no '{type(valor).__name__}'"
            )
        return len(valor)

    def _builtin_range(self, args):
        """
        range(inicio, fin) → [Num]

        Genera la lista de enteros desde 'inicio' (inclusivo) hasta
        'fin' (exclusivo), equivalente a list(range(a, b)) de Python.

        Ejemplo:
            range(0, 5)  → [0, 1, 2, 3, 4]
            range(3, 3)  → []
        """
        if len(args) != 2:
            raise Exception(f"range() requiere 2 argumentos, recibió {len(args)}")
        inicio, fin = args
        if not isinstance(inicio, int) or isinstance(inicio, bool) or \
                not isinstance(fin, int) or isinstance(fin, bool):
            raise Exception("range() requiere dos Num (enteros)")
        return list(range(inicio, fin))

    def _builtin_map(self, args):
        """
        map(lista, f) → [T]

        Aplica la función f a cada elemento de lista y devuelve una
        nueva lista con los resultados. No modifica la lista original.

        f puede ser una FuncionRISCO (definida por el usuario o lambda)
        o cualquier callable de Python interno.

        Ejemplo:
            map([1, 2, 3], (x) => x * 2)  → [2, 4, 6]
        """
        if len(args) != 2:
            raise Exception(f"map() requiere 2 argumentos, recibió {len(args)}")
        lista, func = args
        if not isinstance(lista, list):
            raise Exception(
                f"map() requiere una lista como primer argumento, "
                f"no '{type(lista).__name__}'"
            )
        return [self._aplicar_funcion(func, [elem]) for elem in lista]

    def _builtin_filter(self, args):
        """
        filter(lista, pred) → [T]

        Devuelve una nueva lista con los elementos de lista para los
        cuales pred devuelve true.

        Ejemplo:
            filter([1, 2, 3, 4], (x) => x > 2)  → [3, 4]
        """
        if len(args) != 2:
            raise Exception(f"filter() requiere 2 argumentos, recibió {len(args)}")
        lista, pred = args
        if not isinstance(lista, list):
            raise Exception(
                f"filter() requiere una lista como primer argumento, "
                f"no '{type(lista).__name__}'"
            )
        resultado = []
        for elem in lista:
            valor = self._aplicar_funcion(pred, [elem])
            if not isinstance(valor, bool):
                raise Exception(
                    f"El predicado de filter() debe devolver Bool, "
                    f"no '{type(valor).__name__}'"
                )
            if valor:
                resultado.append(elem)
        return resultado

    def _builtin_reduce(self, args):
        """
        reduce(lista, f) → T

        Combina todos los elementos de lista aplicando f acumulativamente
        de izquierda a derecha.

        Ejemplo:
            reduce([1, 2, 3, 4], (a, b) => a + b)  → 10
            reduce([5], (a, b) => a + b)            → 5

        Raises:
            Exception: Si la lista está vacía.
        """
        if len(args) != 2:
            raise Exception(f"reduce() requiere 2 argumentos, recibió {len(args)}")
        lista, func = args
        if not isinstance(lista, list):
            raise Exception(
                f"reduce() requiere una lista como primer argumento, "
                f"no '{type(lista).__name__}'"
            )
        if len(lista) == 0:
            raise Exception("reduce() no puede operar sobre una lista vacía")
        acum = lista[0]
        for elem in lista[1:]:
            acum = self._aplicar_funcion(func, [acum, elem])
        return acum

    def _builtin_unwrap(self, args):
        """
        unwrap(resultado, defecto) → T

        Extrae el valor de Ok(v) devolviendo v. Si el resultado es
        Err(...), devuelve 'defecto' sin lanzar excepción.

        Los valores Result<T> se representan internamente como tuplas:
            Ok(v)    →  ("ok",  v)
            Err(msg) →  ("err", msg)

        Ejemplo:
            unwrap(("ok", 42), 0)      → 42
            unwrap(("err", "fallo"), 0) → 0
        """
        if len(args) != 2:
            raise Exception(f"unwrap() requiere 2 argumentos, recibió {len(args)}")
        resultado, defecto = args
        if isinstance(resultado, tuple) and len(resultado) == 2:
            tag, valor = resultado
            if tag == "ok":
                return valor
            if tag == "err":
                return defecto
        # Si no es un Result<T>, devolver el valor tal cual (comportamiento permisivo)
        return resultado

    def _builtin_free(self, args):
        """
        free(x) → null

        Libera explícitamente la variable x de la memoria del intérprete
        y solicita al recolector de basura de Python que libere la memoria.
        """
        if len(args) != 1:
            raise Exception(f"free() requiere 1 argumento, recibió {len(args)}")
        valor_a_liberar = args[0]
        nombres_a_borrar = [
            nombre for nombre, val in self.memoria.items()
            if val is valor_a_liberar
        ]
        for nombre in nombres_a_borrar:
            if nombre not in self.vals:
                del self.memoria[nombre]
        gc.collect()
        return None

    def _builtin_input(self, args):
        """
        input(prompt) → Text

        Muestra el prompt en consola y espera que el usuario escriba
        una línea. Siempre devuelve Text — nunca falla.
        Para obtener un número, convertir con num() o decimal() después.

        Ejemplo:
            val nombre = input("¿Cómo te llamas? ")
            val edad   = num(input("¿Cuántos años tienes? "))
        """
        if len(args) > 1:
            raise Exception(f"input() recibe 0 o 1 argumento, recibió {len(args)}")
        prompt = str(args[0]) if args else ""
        try:
            return input(prompt)
        except EOFError:
            return ""

    def _aplicar_funcion(self, func, argumentos):
        """
        Aplica una función a una lista de argumentos.

        Soporta:
          - FuncionRISCO (definidas por el usuario y lambdas)
          - Funciones Python nativas (callable)

        Args:
            func: Una FuncionRISCO o callable Python.
            argumentos (list): Valores de los argumentos.

        Returns:
            El resultado de aplicar la función.

        Raises:
            Exception: Si func no es callable.
        """
        if isinstance(func, FuncionRISCO):
            return self._llamar_funcion(func, argumentos)
        if callable(func):
            return func(*argumentos)
        raise Exception(
            f"Se esperaba una función, no '{type(func).__name__}'"
        )

    # ══════════════════════════════════════════════════════════
    #  CASTEO EXPLÍCITO
    # ══════════════════════════════════════════════════════════

    def visitCasteo(self, ctx: RISCOParser.CasteoContext):
        """
        Convierte un valor a otro tipo de forma explícita.

        Formas soportadas:
          num(x)      → int    Trunca decimales. "42" → 42. true → 1.
          decimal(x)  → float  "3.14" → 3.14. 5 → 5.0. true → 1.0.
          texto(x)    → str    Cualquier valor → representación textual.
          bool(x)     → bool   0/null/""/[] → false; resto → true.

        Raises:
            Exception: Si la conversión no es posible (ej. num("hola")).
        """
        valor = self.visit(ctx.expresion())
        tipo = ctx.getChild(0).getText()

        if tipo == 'num':
            return self._cast_num(valor)
        if tipo == 'decimal':
            return self._cast_decimal(valor)
        if tipo == 'texto':
            return self._a_texto(valor)
        if tipo == 'bool':
            return self._cast_bool(valor)

        raise Exception(f"Tipo de casteo desconocido: '{tipo}'")

    def _cast_num(self, valor):
        """
        Convierte 'valor' a entero (Num).

        Reglas:
          - int   → sin cambio
          - float → trunca hacia cero (int())
          - bool  → 1 si true, 0 si false
          - str   → int(str) si contiene un número entero o decimal
          - None  → 0
          - list  → Error
        """
        if isinstance(valor, bool):
            return 1 if valor else 0
        if isinstance(valor, int):
            return valor
        if isinstance(valor, float):
            return int(valor)
        if isinstance(valor, str):
            try:
                return int(float(valor))
            except ValueError:
                raise Exception(f"No se puede convertir '{valor}' a Num")
        if valor is None:
            return 0
        raise Exception(
            f"No se puede convertir '{type(valor).__name__}' a Num"
        )

    def _cast_decimal(self, valor):
        """
        Convierte 'valor' a flotante (Decimal).

        Reglas:
          - float → sin cambio
          - int   → float(int)
          - bool  → 1.0 si true, 0.0 si false
          - str   → float(str) si contiene un número
          - None  → 0.0
          - list  → Error
        """
        if isinstance(valor, bool):
            return 1.0 if valor else 0.0
        if isinstance(valor, (int, float)):
            return float(valor)
        if isinstance(valor, str):
            try:
                return float(valor)
            except ValueError:
                raise Exception(f"No se puede convertir '{valor}' a Decimal")
        if valor is None:
            return 0.0
        raise Exception(
            f"No se puede convertir '{type(valor).__name__}' a Decimal"
        )

    def _cast_bool(self, valor):
        """
        Convierte 'valor' a Bool.

        Valores que producen false: 0, 0.0, "", [], None, false.
        Todos los demás producen true.
        """
        if isinstance(valor, bool):
            return valor
        if valor is None:
            return False
        if isinstance(valor, (int, float)):
            return valor != 0
        if isinstance(valor, str):
            return len(valor) > 0
        if isinstance(valor, list):
            return len(valor) > 0
        return True

    # ══════════════════════════════════════════════════════════
    #  UTILIDADES INTERNAS
    # ══════════════════════════════════════════════════════════

    def _a_texto(self, valor):
        """
        Convierte cualquier valor RISCO a su representación textual para print().

        Sigue las convenciones de Python para ser consistente con los tests:
          - None  → "None"
          - True  → "True"
          - False → "False"
          - list  → "[e1, e2, ...]"  (str() de Python sobre la lista)
          - float → str() de Python  (ej. 3.14 → "3.14")
          - resto → str()

        Nota: el prefijo "> " del modo interactivo (expresion_stmt) usa
        directamente str() de Python sobre el valor, que produce el mismo
        resultado para bool, None, int y float.
        """
        if valor is None:
            return "None"
        if isinstance(valor, bool):
            return "True" if valor else "False"
        if isinstance(valor, list):
            # Reconstruir manualmente para que elementos internos también
            # usen las convenciones de Python (True, False, None, etc.)
            elementos = ", ".join(self._a_texto(e) for e in valor)
            return f"[{elementos}]"
        if isinstance(valor, float):
            return str(valor)
        return str(valor)


# ──────────────────────────────────────────────────────────────
#  Centinela interno para distinguir "no es un built-in"
# ──────────────────────────────────────────────────────────────

class _Centinela:
    """Objeto centinela único para indicar que una función no es built-in."""
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

_NO_ES_BUILTIN = _Centinela()