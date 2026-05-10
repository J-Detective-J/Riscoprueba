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
import sys
from antlr4 import *
from gramaticas.RISCOParser import RISCOParser
from gramaticas.RISCOVisitor import RISCOVisitor
from src.memoria import GestorMemoria

sys.setrecursionlimit(10000)
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
        self.params       = params
        self.cuerpo_expr  = cuerpo_expr
        self.cuerpo_stmts = cuerpo_stmts
        self.closure      = closure


# ──────────────────────────────────────────────────────────────
#  Primitivas matemáticas — implementadas en Python puro
#  (sin importar math ni numpy)
#
#  Estas funciones viven a nivel de módulo (fuera de la clase)
#  porque son algoritmos numéricos puros: no necesitan estado del
#  intérprete y así pueden testearse de forma aislada.
# ──────────────────────────────────────────────────────────────

# Constante ln(2) precalculada con suficiente precisión Float64.
# Se usa en _prim_log para la reducción de rango.
_LN2 = 0.6931471805599453

# Estado global del generador LCG (Linear Congruential Generator).
# Se modifica únicamente a través de _prim_lcg_seed y _prim_lcg_next.
_lcg_semilla = 12345


def _prim_sqrt(x):
    """
    Raíz cuadrada por el método de Newton-Raphson.

    Fórmula de iteración:
        x_(k+1) = (x_k + n / x_k) / 2

    Convergencia cuadrática: cada iteración aproximadamente duplica
    el número de dígitos correctos. En la práctica converge en < 25
    iteraciones para cualquier valor Float64 representable.

    La parada se realiza por tolerancia absoluta (1e-10) en lugar de
    un número fijo de iteraciones, lo que es 2.4× más rápido en promedio.

    Args:
        x (float): Valor del que calcular la raíz.

    Returns:
        float | None: La raíz cuadrada, o None si x < 0 (dominio inválido).
                      El caller convierte None en Err(...) de RISCO.
    """
    if x < 0:
        return None          # RISCO lo convierte en Err(...)
    if x == 0:
        return 0.0
    est = x / 2.0
    for _ in range(1000):
        nueva = 0.5 * (est + x / est)
        if abs(nueva - est) < 1e-10:
            return nueva
        est = nueva
    return est               # convergió al máximo de iteraciones


def _prim_exp(x):
    """
    e^x por reducción de rango y serie de Taylor con parada por tolerancia.

    Estrategia de reducción de rango:
        e^x = e^(n + r) = e^n * e^r,  n = floor(x), r = x - n, r ∈ [0, 1)

    Para x negativo se aplica e^x = 1 / e^(-x).

    Con r ∈ [0, 1) la serie de Taylor converge en ≤ 25 términos para
    precisión Float64, independientemente del valor original de x.
    Esto contrasta con aplicar la serie directamente sobre x grande,
    que requeriría cientos de términos y acumularía error de cancelación.

    Maneja correctamente exp(0) = 1, exp(700) y exp(-700) sin overflow.

    Args:
        x (float): Exponente.

    Returns:
        float: e^x.
    """
    if x < 0:
        return 1.0 / _prim_exp(-x)
    if x == 0:
        return 1.0

    # Reducción de rango: separar parte entera y fraccionaria
    n = int(x)
    r = x - n

    # Serie de Taylor para e^r  (r ∈ [0,1) → converge rápido)
    termino  = 1.0
    resultado = 1.0
    for k in range(1, 100):
        termino  *= r / k
        resultado += termino
        if abs(termino) < 1e-15:
            break

    # e^n = (e^1)^n  usando la constante e con máxima precisión Float64
    E = 2.718281828459045235360287
    potencia = 1.0
    for _ in range(n):
        potencia *= E

    return resultado * potencia


def _prim_log(x):
    """
    Logaritmo natural por reducción de rango con ln(2) y serie arctanh.

    Estrategia de reducción de rango:
        ln(x) = ln(m * 2^k) = ln(m) + k * ln(2)

    Se normaliza m al intervalo [0.5, 1.0).
    En ese rango z = (m - 1) / (m + 1) está en [-0.34, 0),
    y la serie arctanh(z) = Σ z^(2i+1) / (2i+1) converge en ≤ 15 iteraciones.

    Ventaja frente a la propuesta del documento: aplicar la serie
    directamente sobre x grande (ej. ln(1000)) requeriría ~200 términos;
    esta versión siempre usa ≤ 15 independientemente del valor de entrada.

    Args:
        x (float): Argumento del logaritmo.

    Returns:
        float | None: ln(x), o None si x ≤ 0 (dominio inválido).
                      El caller convierte None en Err(...) de RISCO.
    """
    if x <= 0:
        return None          # RISCO lo convierte en Err(...)
    if x == 1.0:
        return 0.0

    # Reducción de rango: x = m * 2^k, m ∈ [0.5, 1.0)
    k = 0
    m = float(x)
    while m >= 1.0:
        m /= 2.0
        k += 1
    while m < 0.5:
        m *= 2.0
        k -= 1

    # arctanh para m ∈ [0.5, 1.0)  →  z ∈ [-0.34, 0)
    z  = (m - 1.0) / (m + 1.0)
    z2 = z * z
    t  = z
    s  = 0.0
    for i in range(60):
        s += t / (2 * i + 1)
        t *= z2
        if abs(t) < 1e-16:
            break

    return 2.0 * s + k * _LN2


def _prim_matmul(A, B):
    """
    Multiplicación de matrices con orden de bucle i→k→j optimizado para caché.

    El orden estándar i→j→k accede a B[k][j] de forma no contigua en
    memoria (salto de fila por cada k). El orden i→k→j precalcula A[i][k]
    una sola vez y reutiliza la fila B[k] completa en el loop interno j,
    que sí es contigua. Esto mejora la localidad de caché especialmente
    en matrices grandes.

    Precondición: columnas(A) == filas(B)

    Args:
        A (list[list]): Matriz de fA × cA.
        B (list[list]): Matriz de fB × cB.

    Returns:
        list[list] | None: Matriz resultado fA × cB, o None si dimensiones
                           incompatibles. El caller convierte None en Err(...).
    """
    fA = len(A);  cA = len(A[0])
    fB = len(B);  cB = len(B[0])
    if cA != fB:
        return None          # RISCO lo convierte en Err(...)
    if fA * cB > 1_000_000:
        return None
    C = [[0.0] * cB for _ in range(fA)]
    for i in range(fA):
        for k in range(cA):
            aik = A[i][k]    # precalculado: se reutiliza cB veces
            for j in range(cB):
                C[i][j] += aik * B[k][j]
    return C


def _prim_matmulT(A, B):
    """
    Calcula A × B^T sin construir explícitamente la transpuesta.

    C[i][j] = Σ_k  A[i][k] * B[j][k]

    Acceder a B[j][k] (fila j de B) es contiguo en memoria, lo que
    evita el coste de trasponer B y mantiene la localidad de caché.

    Precondición: columnas(A) == columnas(B)  (ambas tienen la misma
    dimensión de columnas porque B^T tiene filas = columnas de B).

    Args:
        A (list[list]): Matriz de fA × cA.
        B (list[list]): Matriz de fB × cA (se usa traspuesta implícita).

    Returns:
        list[list] | None: Matriz resultado fA × fB, o None si
                           columnas(A) != columnas(B).
    """
    fA = len(A);  cA = len(A[0])
    fB = len(B)
    if cA != len(B[0]):
        return None
    if fA * fB > 1_000_000:
        return None
    C = [[0.0] * fB for _ in range(fA)]
    for i in range(fA):
        for j in range(fB):
            s = 0.0
            for k in range(cA):
                s += A[i][k] * B[j][k]
            C[i][j] = s
    return C


def _prim_matmulAdd(A, W, b):
    """
    Calcula A × W + b (bias por fila) en un único recorrido de la matriz.

    La suma del bias se integra en el mismo loop que la multiplicación,
    evitando un segundo recorrido de la matriz resultado. En redes
    neuronales esta operación aparece en cada capa densa.

    Precondición: columnas(A) == filas(W)  y  len(b) == columnas(W)

    Args:
        A (list[list]): Activaciones de entrada, fA × cA.
        W (list[list]): Pesos de la capa, fW × cW  (con cA == fW).
        b (list):       Vector de bias de longitud cW.

    Returns:
        list[list] | None: Matriz resultado fA × cW con bias sumado,
                           o None si columnas(A) != filas(W).
    """
    fA = len(A);  cA = len(A[0])
    fW = len(W);  cW = len(W[0])
    if cA != fW:
        return None
    if fA * cW > 1_000_000:
        return None
    C = [[0.0] * cW for _ in range(fA)]
    for i in range(fA):
        for k in range(cA):
            aik = A[i][k]
            for j in range(cW):
                C[i][j] += aik * W[k][j]
        for j in range(cW):
            C[i][j] += b[j]   # suma bias en la misma fila, sin segundo pase
    return C


def _prim_lcg_seed(n):
    """
    Fija la semilla global del generador LCG.

    La semilla se reduce módulo 2^32 para mantenerla en el rango válido
    del LCG. Llamar a esta función con el mismo valor siempre produce
    la misma secuencia en _prim_lcg_next, garantizando reproducibilidad.

    Args:
        n (int): Semilla deseada.
    """
    global _lcg_semilla
    _lcg_semilla = int(n) % (2 ** 32)


def _prim_lcg_next():
    """
    Genera el siguiente número pseudoaleatorio con el LCG interno.

    Parámetros POSIX (Numerical Recipes):
        a = 1664525
        c = 1013904223
        m = 2^32

    Fórmula:
        semilla = (a * semilla + c) mod m

    Returns:
        float: Valor en [0.0, 1.0) obtenido dividiendo la semilla entre m.
    """
    global _lcg_semilla
    _lcg_semilla = (1664525 * _lcg_semilla + 1013904223) % (2 ** 32)
    return _lcg_semilla / (2 ** 32)


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


# ──────────────────────────────────────────────────────────────
#  Visitor principal
# ──────────────────────────────────────────────────────────────

class VisitanteEvaluador(RISCOVisitor):
    """
    Visitor que evalúa el AST de un programa RISCO.

    Mantiene el estado del programa en dos diccionarios:
      - memoria:   variables → valores
      - funciones: nombre → FuncionRISCO

    Los built-ins están registrados en _intentar_builtin y se resuelven
    en visitLlamada_funcion antes de buscar en self.funciones.

    Atributos:
        memoria  (dict): Variables del programa.
        funciones (dict): Funciones definidas por el usuario.
        vals     (set):  Nombres de variables inmutables (val).
        ultimo_resultado: Último valor evaluado (útil para el REPL).
        modo_interactivo (bool): Si True, imprime expresiones sueltas.
    """

    def __init__(self, modo_interactivo=False):
        self.memoria          = {}
        self.funciones        = {}
        self.vals             = set()
        self.ultimo_resultado = None
        self.modo_interactivo = modo_interactivo
        self.gestor_memoria   = GestorMemoria()

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
        valor  = self.visit(ctx.expresion())
        if nombre in self.memoria:
            raise Exception(f"'{nombre}' ya está definida y no puede redeclararse")
        self.memoria[nombre] = valor
        self.gestor_memoria.validar_num_variables(self.memoria)
        if isinstance(valor, list):
            self.gestor_memoria.validar_lista(valor, nombre)
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
        valor  = self.visit(ctx.expresion())
        if nombre not in self.memoria:
            raise Exception(f"Variable '{nombre}' no definida")
        if nombre in self.vals:
            raise Exception(f"'{nombre}' es inmutable (val), no se puede reasignar")
        self.memoria[nombre] = valor
        if isinstance(valor, list):
            self.gestor_memoria.validar_lista(valor, nombre)
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
        iterable   = self.visit(ctx.expresion())
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
        bloques     = self._obtener_bloques_if(ctx)
        condicion   = self.visit(expresiones[0])
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
        bloques       = []
        bloque_actual = []
        for i in range(ctx.getChildCount()):
            hijo  = ctx.getChild(i)
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

        cuerpo_expr  = None
        cuerpo_stmts = None
        if ctx.expresion():
            cuerpo_expr = ctx.expresion()
        else:
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
        Ejecuta una función RISCO con control de memoria.

        Mejora:
        - controla profundidad recursiva
        - crea entorno local controlado
        - restaura memoria siempre
        - limpia entorno local al finalizar
        """

        if len(argumentos) != len(funcion.params):
            raise Exception(
                f"Se esperaban {len(funcion.params)} argumentos, "
                f"se recibieron {len(argumentos)}"
            )

        self.gestor_memoria.entrar_funcion()

        memoria_anterior = self.memoria
        entorno_local = dict(funcion.closure)

        for nombre, valor in zip(funcion.params, argumentos):
            entorno_local[nombre] = valor

        self.memoria = entorno_local

        resultado = None

        try:
            if funcion.cuerpo_expr is not None:
                resultado = self.visit(funcion.cuerpo_expr)
            else:
                for sentencia in funcion.cuerpo_stmts:
                    self.visit(sentencia)

        except _ReturnException as ret:
            resultado = ret.valor
        except RecursionError:
            raise Exception(
                "Límite interno de recursión alcanzado. "
                "El programa requiere demasiadas llamadas anidadas."
            )

        finally:
            self.memoria = memoria_anterior
            entorno_local.clear()
            self.gestor_memoria.salir_funcion()

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
            params = []
            if ctx.lista_params():
                for p in ctx.lista_params().IDENTIFICADOR():
                    params.append(p.getText())
            cuerpo_expr = ctx.expresion()
            closure     = dict(self.memoria)
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
        if op == '==': return izq == der
        if op == '!=': return izq != der

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
            valor    = self.visit(ctx.comparacion(i))
            if operador == '+':
                if isinstance(resultado, bool) or isinstance(valor, bool):
                    raise Exception("Error de tipos: '+' no está definido para Bool")
                if isinstance(resultado, str) and isinstance(valor, str):
                    resultado = resultado + valor
                elif isinstance(resultado, list) and isinstance(valor, list):
                    resultado = resultado + valor
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
            valor    = self.visit(ctx.potencia(i))
            if isinstance(resultado, bool) or isinstance(valor, bool) or \
                    not isinstance(resultado, (int, float)) or \
                    not isinstance(valor, (int, float)):
                raise Exception(
                    f"Error de tipos: '{operador}' solo opera sobre números"
                )
            if operador == '*':
                resultado *= valor
            elif operador == '/':
                if valor == 0: raise Exception("División por cero")
                resultado /= valor
            elif operador == '%':
                if valor == 0: raise Exception("Módulo por cero")
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
            texto    = ctx.STRING().getText()
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
            if nombre in self.memoria:   return self.memoria[nombre]
            # Luego buscar en funciones (para poder pasar funciones como argumentos)
            if nombre in self.funciones: return self.funciones[nombre]
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
          1. Built-ins del lenguaje base (long, range, map, filter, reduce,
             unwrap, free, input) y primitivas mat (mat_sqrt, mat_exp, etc.)
          2. Funciones definidas por el usuario en self.funciones
          3. Funciones almacenadas como variables en memoria
             (parámetros de orden superior)

        La notación módulo mat.X se mapea internamente a mat_X antes
        de buscar en el diccionario de dispatch.

        Raises:
            Exception: Si el nombre no corresponde a ninguna función conocida.
        """
        # Detectar qué tipo de llamada es
        if   ctx.LONG_F():   nombre = 'long'
        elif ctx.RANGE_F():  nombre = 'range'
        elif ctx.MAP_F():    nombre = 'map'
        elif ctx.FILTER_F(): nombre = 'filter'
        elif ctx.REDUCE_F(): nombre = 'reduce'
        elif ctx.UNWRAP_F(): nombre = 'unwrap'
        elif ctx.FREE_F():   nombre = 'free'
        elif ctx.INPUT_F():  nombre = 'input'
        else:
            identificadores = ctx.IDENTIFICADOR()
            if len(identificadores) == 2:
                # Notación de módulo: mat.mul → "mat_mul"
                nombre = identificadores[0].getText() + '_' + identificadores[1].getText()
            else:
                nombre = identificadores[0].getText()

        args_raw = []
        if ctx.lista_args():
            for arg_ctx in ctx.lista_args().argumento():
                args_raw.append(self.visit(arg_ctx.expresion()))

        # 1. Intentar resolver como built-in (base o mat)
        resultado_builtin = self._intentar_builtin(nombre, args_raw)
        if resultado_builtin is not _NO_ES_BUILTIN:
            return resultado_builtin

        # 2. Función definida por el usuario
        if nombre in self.funciones:
            return self._llamar_funcion(self.funciones[nombre], args_raw)

        # 3. Función almacenada como variable (orden superior)
        if nombre in self.memoria:
            func = self.memoria[nombre]
            if isinstance(func, FuncionRISCO):
                return self._llamar_funcion(func, args_raw)
            elif callable(func):
                return func(*args_raw)

        raise Exception(f"Función '{nombre}' no definida")

    # ══════════════════════════════════════════════════════════
    #  BUILT-INS — despacho
    # ══════════════════════════════════════════════════════════

    def _intentar_builtin(self, nombre, args):
        """
        Despacha la llamada a la función built-in correspondiente.

        El diccionario dispatch agrupa los built-ins del lenguaje base
        y las primitivas del módulo mat en un solo lugar para facilitar
        su extensión futura.

        Returns:
            El valor del built-in, o el centinela _NO_ES_BUILTIN si
            el nombre no corresponde a ningún built-in conocido.
        """
        dispatch = {
            # ── Built-ins del lenguaje base ──────────────────
            'long':               self._builtin_long,
            'range':              self._builtin_range,
            'map':                self._builtin_map,
            'filter':             self._builtin_filter,
            'reduce':             self._builtin_reduce,
            'unwrap':             self._builtin_unwrap,
            'free':               self._builtin_free,
            'input':              self._builtin_input,
            'split':              self._builtin_split,
            # ── Primitivas internas de mat.rc ────────────────
            'prim_mat_sqrt':      self._builtin_mat_sqrt,
            'prim_mat_exp':       self._builtin_mat_exp,
            'prim_mat_log':       self._builtin_mat_log,
            'prim_mat_matmul':    self._builtin_mat_mul,
            'prim_mat_matmulT':   self._builtin_mat_mulT,
            'prim_mat_matmulAdd': self._builtin_mat_mulAdd,
            'prim_mat_lcg_next':  self._builtin_prim_lcg_next,
            'prim_mat_lcg_seed':  self._builtin_mat_seed,
             # ── Primitivas internas de file.rc ────────────────
            'prim_file_open':     self._builtin_file_open,
            'prim_file_close':    self._builtin_file_close,
            'prim_file_read':     self._builtin_file_read,
            'prim_file_readLine': self._builtin_file_readLine,
            'prim_file_write':    self._builtin_file_write,
            'prim_file_exists':   self._builtin_file_exists,
            'prim_file_delete':   self._builtin_file_delete,
            'mem_info':           self._builtin_mem_info,
            'memory_info': self._builtin_memory_info,
            'memory_free': self._builtin_memory_free,
        }
        if nombre in dispatch:
            return dispatch[nombre](args)
        return _NO_ES_BUILTIN

    # ── Built-ins base ────────────────────────────────────────

    def _builtin_mem_info(self, args):
        """
        mem_info() → Text

        Devuelve información básica del estado de memoria del intérprete.
        """
        if len(args) != 0:
            raise Exception(f"mem_info() no recibe argumentos, recibió {len(args)}")

        return (
            "variables=" + str(len(self.memoria)) +
            ", recursion=" + str(self.gestor_memoria.profundidad_recursion)
        )
    def _builtin_long(self, args):
        """
        long(lista) → Num

        Devuelve el número de elementos de una lista o el número de
        caracteres de un string.

        Ejemplo:
            long([1, 2, 3])  → 3
            long("hola")     → 4
            long([])         → 0
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
            unwrap(("ok", 42), 0)       → 42
            unwrap(("err", "fallo"), 0) → 0
        """
        if len(args) != 2:
            raise Exception(f"unwrap() requiere 2 argumentos, recibió {len(args)}")
        resultado, defecto = args
        if isinstance(resultado, tuple) and len(resultado) == 2:
            tag, valor = resultado
            if tag == "ok":  return valor
            if tag == "err": return defecto
        # Si no es un Result<T>, devolver el valor tal cual (comportamiento permisivo)
        return resultado

    def _builtin_free(self, args):
        """
        free(x) → null

        Libera referencias al objeto dentro de la memoria del intérprete
        y solicita recolección de basura.
        """
        if len(args) != 1:
            raise Exception(f"free() requiere 1 argumento, recibió {len(args)}")

        valor = args[0]
        self.gestor_memoria.liberar_referencias(
            self.memoria,
            self.vals,
            valor
        )
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
    def _builtin_split(self, args):
        """
        split(texto, separador) → [Text]

        Divide un string usando el separador indicado.

        Ejemplo:
            split("a,b,c", ",")   → ["a", "b", "c"]
            split("x\ny", "\n")   → ["x", "y"]
        """
        if len(args) != 2:
            raise Exception(f"split() requiere 2 argumentos, recibió {len(args)}")
        texto, separador = args

        if not isinstance(texto, str) or not isinstance(separador, str):
            raise Exception("split() requiere dos Text")
    
        return texto.split(separador)

    # ── Primitivas mat ────────────────────────────────────────

    def _builtin_mat_sqrt(self, args):
        """
        mat.sqrt(x) → Result<Decimal>

        Raíz cuadrada por Newton-Raphson con criterio de parada por tolerancia.
        Devuelve Ok(raiz) si x >= 0, o Err(msg) si x < 0.

        Usar con unwrap() para obtener el valor o un fallback:
            val r = unwrap(mat.sqrt(x), 0.0)
        """
        if len(args) != 1:
            raise Exception(f"mat.sqrt() requiere 1 argumento, recibió {len(args)}")
        x = args[0]
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise Exception(f"mat.sqrt() requiere un Decimal, no '{type(x).__name__}'")
        resultado = _prim_sqrt(float(x))
        if resultado is None:
            return ("err", f"mat.sqrt: argumento negativo ({x})")
        return ("ok", resultado)

    def _builtin_mat_exp(self, args):
        """
        mat.exp(x) → Decimal

        e^x por reducción de rango y serie de Taylor con parada por tolerancia.
        Nunca falla — devuelve Decimal directamente (no Result).

        Ejemplo:
            mat.exp(0.0)  → 1.0
            mat.exp(1.0)  → 2.718281828459045
        """
        if len(args) != 1:
            raise Exception(f"mat.exp() requiere 1 argumento, recibió {len(args)}")
        x = args[0]
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise Exception(f"mat.exp() requiere un Decimal, no '{type(x).__name__}'")
        return _prim_exp(float(x))

    def _builtin_mat_log(self, args):
        """
        mat.log(x) → Result<Decimal>

        Logaritmo natural por reducción de rango y serie arctanh.
        Devuelve Ok(ln(x)) si x > 0, o Err(msg) si x <= 0.

        Ejemplo:
            unwrap(mat.log(1.0), 0.0)  → 0.0
            unwrap(mat.log(0.0), 0.0)  → 0.0  (fallback por Err)
        """
        if len(args) != 1:
            raise Exception(f"mat.log() requiere 1 argumento, recibió {len(args)}")
        x = args[0]
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise Exception(f"mat.log() requiere un Decimal, no '{type(x).__name__}'")
        resultado = _prim_log(float(x))
        if resultado is None:
            return ("err", f"mat.log: argumento no positivo ({x})")
        return ("ok", resultado)

    def _builtin_mat_mul(self, args):
        """
        mat.mul(A, B) → Result<[[Decimal]]>

        Multiplicación matricial con orden i→k→j optimizado para caché.
        Devuelve Ok(C) si columnas(A) == filas(B), o Err(msg) si no.

        Ejemplo:
            val C = unwrap(mat.mul([[1,2],[3,4]], [[5],[6]]), [])
            // C == [[17.0], [39.0]]
        """
        if len(args) != 2:
            raise Exception(f"mat.mul() requiere 2 argumentos, recibió {len(args)}")
        A, B = args
        if not isinstance(A, list) or not isinstance(B, list):
            raise Exception("mat.mul() requiere dos matrices ([[Decimal]])")
        self.gestor_memoria.validar_matriz(A, "A")
        self.gestor_memoria.validar_matriz(B, "B")
        resultado = _prim_matmul(A, B)
        if resultado is None:
            cA = len(A[0]) if A and A[0] else 0
            fB = len(B)
            return ("err", f"mat.mul: dimensiones incompatibles (cols A={cA}, filas B={fB})")
        return ("ok", resultado)
    
    def _builtin_mat_mulT(self, args):
        """
        mat.mulT(A, B) → Result<[[Decimal]]>

        Calcula A × B^T sin construir la transpuesta explícita.
        Devuelve Ok(C) si columnas(A) == columnas(B), o Err(msg) si no.

        Útil en backpropagation donde se necesita X × W^T.
        """
        if len(args) != 2:
            raise Exception(f"mat.mulT() requiere 2 argumentos, recibió {len(args)}")
        A, B = args
        if not isinstance(A, list) or not isinstance(B, list):
            raise Exception("mat.mulT() requiere dos matrices ([[Decimal]])")
        self.gestor_memoria.validar_matriz(A, "A")
        self.gestor_memoria.validar_matriz(B, "B")
        resultado = _prim_matmulT(A, B)
        if resultado is None:
            return ("err", "mat.mulT: columnas(A) != columnas(B)")
        return ("ok", resultado)

    def _builtin_mat_mulAdd(self, args):
        """
        mat.mulAdd(A, W, b) → Result<[[Decimal]]>

        Calcula A × W + b (bias sumado por fila) en un único recorrido.
        Devuelve Ok(C) si dimensiones compatibles, o Err(msg) si no.

        Es la operación central de una capa densa en una red neuronal.

        Precondición:
            columnas(A) == filas(W)  y  long(b) == columnas(W)
        """
        if len(args) != 3:
            raise Exception(f"mat.mulAdd() requiere 3 argumentos, recibió {len(args)}")
        A, W, b = args
        if not isinstance(A, list) or not isinstance(W, list) or not isinstance(b, list):
            raise Exception("mat.mulAdd() requiere dos matrices y un vector")
        self.gestor_memoria.validar_matriz(A, "A")
        self.gestor_memoria.validar_matriz(W, "W")
        self.gestor_memoria.validar_matriz(b, "b")
        resultado = _prim_matmulAdd(A, W, b)
        if resultado is None:
            return ("err", "mat.mulAdd: dimensiones incompatibles")
        return ("ok", resultado)

    def _builtin_mat_seed(self, args):
        """
        mat.seed(n) → Null

        Fija la semilla del generador LCG interno para reproducibilidad.
        Llamar con el mismo n antes de mat.random siempre produce la
        misma secuencia de números pseudoaleatorios.

        Ejemplo:
            mat.seed(42)
            val M = mat.random(2, 3)  // siempre la misma matriz
        """
        if len(args) != 1:
            raise Exception(f"mat.seed() requiere 1 argumento, recibió {len(args)}")
        n = args[0]
        if isinstance(n, bool) or not isinstance(n, int):
            raise Exception(f"mat.seed() requiere un Num (entero), no '{type(n).__name__}'")
        _prim_lcg_seed(n)
        return None

    def _builtin_prim_lcg_next(self, args):
        if len(args) != 0:
            raise Exception("prim_mat_lcg_next() no recibe argumentos")
        return _prim_lcg_next()
    
    def _builtin_mat_random(self, args):
        """
        mat.random(f, c) → [[Decimal]]

        Genera una matriz f × c con valores en [0.0, 1.0) usando el LCG
        interno. La semilla se controla con mat.seed(n).

        Devuelve Decimal directamente (no Result) porque la generación
        nunca puede fallar si f y c son enteros positivos.

        Ejemplo:
            mat.seed(0)
            val W = mat.random(3, 4)  // matriz 3×4 reproducible
        """
        if len(args) != 2:
            raise Exception(f"mat.random() requiere 2 argumentos, recibió {len(args)}")
        f, c = args
        if isinstance(f, bool) or not isinstance(f, int) or \
           isinstance(c, bool) or not isinstance(c, int):
            raise Exception("mat.random() requiere dos Num (enteros)")
        if f <= 0 or c <= 0:
            raise Exception("mat.random() requiere filas y columnas positivas")
        return [[_prim_lcg_next() for _ in range(c)] for _ in range(f)]
    
    def _builtin_file_open(self, args):
        try:
            return open(str(args[0]), str(args[1]))
        except:
            return None

    def _builtin_file_close(self, args):
        try:
            args[0].close()
        except:
            pass
        return None

    def _builtin_file_read(self, args):
        try:
            return args[0].read()
        except:
            return None

    def _builtin_file_readLine(self, args):
        try:
            return args[0].readline()
        except:
            return None

    def _builtin_file_write(self, args):
        try:
            args[0].write(str(args[1]))
        except:
            pass
        return None

    def _builtin_file_exists(self, args):
        import os
        return os.path.exists(str(args[0]))

    def _builtin_file_delete(self, args):
        import os
        try:
            if os.path.exists(str(args[0])):
                os.remove(str(args[0]))
                return True
        except:
            pass
        return False

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
        tipo  = ctx.getChild(0).getText()
        if tipo == 'num':     return self._cast_num(valor)
        if tipo == 'decimal': return self._cast_decimal(valor)
        if tipo == 'texto':   return self._a_texto(valor)
        if tipo == 'bool':    return self._cast_bool(valor)
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
        if isinstance(valor, bool): return 1 if valor else 0
        if isinstance(valor, int):  return valor
        if isinstance(valor, float): return int(valor)
        if isinstance(valor, str):
            try:    return int(float(valor))
            except: raise Exception(f"No se puede convertir '{valor}' a Num")
        if valor is None: return 0
        raise Exception(f"No se puede convertir '{type(valor).__name__}' a Num")

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
        if isinstance(valor, bool): return 1.0 if valor else 0.0
        if isinstance(valor, (int, float)): return float(valor)
        if isinstance(valor, str):
            try:    return float(valor)
            except: raise Exception(f"No se puede convertir '{valor}' a Decimal")
        if valor is None: return 0.0
        raise Exception(f"No se puede convertir '{type(valor).__name__}' a Decimal")

    def _cast_bool(self, valor):
        """
        Convierte 'valor' a Bool.

        Valores que producen false: 0, 0.0, "", [], None, false.
        Todos los demás producen true.
        """
        if isinstance(valor, bool): return valor
        if valor is None: return False
        if isinstance(valor, (int, float)): return valor != 0
        if isinstance(valor, str):  return len(valor) > 0
        if isinstance(valor, list): return len(valor) > 0
        return True

    # ══════════════════════════════════════════════════════════
    #  UTILIDADES INTERNAS
    # ══════════════════════════════════════════════════════════

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

    def _a_texto(self, valor):
        """
        Convierte cualquier valor RISCO a su representación textual para print().

        Sigue las convenciones de Python para ser consistente con los tests:
          - None  → "None"
          - True  → "True"
          - False → "False"
          - list  → "[e1, e2, ...]"  (reconstrucción recursiva)
          - float → str() de Python  (ej. 3.14 → "3.14")
          - resto → str()
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
    def _contar_celdas_risco(self, valor):
        if not isinstance(valor, list):
            return 0
        total = 0
        for elem in valor:
            if isinstance(elem, list):
                total += self._contar_celdas_risco(elem)
            else:
                total += 1
        return total


    def _es_matriz_risco(self, valor):
        if not isinstance(valor, list) or len(valor) == 0:
            return False
        if not isinstance(valor[0], list):
            return False

        columnas = len(valor[0])
        for fila in valor:
            if not isinstance(fila, list):
                return False
            if len(fila) != columnas:
                return False

        return True


    def _builtin_memory_info(self, args):
        if len(args) != 0:
            raise Exception("memory_info() no recibe argumentos")

        variables = len(self.memoria)
        listas = 0
        matrices = 0
        celdas = 0

        for valor in self.memoria.values():
            if isinstance(valor, list):
                listas += 1
                celdas += self._contar_celdas_risco(valor)
                if self._es_matriz_risco(valor):
                    matrices += 1

        return (
            "variables=" + str(variables) +
            ", listas=" + str(listas) +
            ", matrices=" + str(matrices) +
            ", celdas=" + str(celdas) +
            ", recursion=" + str(self.gestor_memoria.profundidad_recursion)
        )


    def _builtin_memory_free(self, args):
        if len(args) != 1:
            raise Exception("memory_free() requiere 1 argumento")

        nombre = args[0]

        if not isinstance(nombre, str):
            raise Exception("memory_free() requiere el nombre de la variable como texto")

        if nombre in self.vals:
            raise Exception("memory_free() no puede liberar variables val")

        if nombre in self.memoria:
            del self.memoria[nombre]

        return None