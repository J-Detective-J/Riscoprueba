import pytest
import sys
import os
import math
from io import StringIO
from unittest.mock import patch

# Para que encuentre los módulos de src y gramaticas
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.risco import RISCO
from src.visitante_evaluador import (
    _prim_sqrt,
    _prim_exp,
    _prim_log,
    _prim_matmul,
    _prim_matmulT,
    _prim_matmulAdd,
    _prim_lcg_seed,
    _prim_lcg_next,
    _LN2,
)


# ──────────────────────────────────────────────────────────────
#  Helpers compartidos
# ──────────────────────────────────────────────────────────────

def ejecutar(codigo):
    """Ejecuta código RISCO y captura lo que imprime."""
    captura = StringIO()
    sys.stdout = captura
    interprete = RISCO(modo_interactivo=True)
    interprete._ejecutar_codigo(codigo)
    sys.stdout = sys.__stdout__
    return [l.strip() for l in captura.getvalue().strip().splitlines() if l.strip()]


def ejecutar_con_input(codigo, entradas):
    """
    Igual que ejecutar() pero simula respuestas del usuario.
    entradas: lista de strings, uno por cada input() que aparezca en el código.
    """
    captura = StringIO()
    sys.stdout = captura
    with patch('builtins.input', side_effect=entradas):
        interprete = RISCO(modo_interactivo=True)
        interprete._ejecutar_codigo(codigo)
    sys.stdout = sys.__stdout__
    return [l.strip() for l in captura.getvalue().strip().splitlines() if l.strip()]


def cerca(a, b, rel=1e-9, abs_=1e-12):
    """Igualdad aproximada con tolerancia mixta absoluta/relativa."""
    return abs(a - b) <= max(abs_, rel * abs(b))


def matrices_iguales(A, B, rel=1e-9):
    """Comprueba dimensiones y valores de dos matrices."""
    if len(A) != len(B):
        return False
    for fila_a, fila_b in zip(A, B):
        if len(fila_a) != len(fila_b):
            return False
        for a, b in zip(fila_a, fila_b):
            if not cerca(a, b, rel=rel):
                return False
    return True


# ══════════════════════════════════════════════════════════════
#  LENGUAJE RISCO — tests de integración vía el intérprete
# ══════════════════════════════════════════════════════════════

# ── Operaciones básicas ───────────────────────────────────────

def test_suma():
    assert ejecutar("val x = 5\nval y = 3\nx + y\n") == ["> 8"]

def test_resta():
    assert ejecutar("val x = 5\nval y = 3\nx - y\n") == ["> 2"]

def test_multiplicacion():
    assert ejecutar("val x = 5\nval y = 3\nx * y\n") == ["> 15"]

def test_division():
    assert ejecutar("val x = 5\nval y = 3\nx / y\n") == ["> 1.6666666666666667"]

def test_division_por_cero():
    resultado = ejecutar("1 / 0\n")
    assert any("División por cero" in r for r in resultado)

def test_modulo():
    assert ejecutar("10 % 3\n") == ["> 1"]

def test_potencia():
    assert ejecutar("2 ^ 3\n") == ["> 8"]

def test_potencia_asociatividad_derecha():
    assert ejecutar('2 ^ 3 ^ 2\n') == ["> 512"]

# ── Precedencia ───────────────────────────────────────────────

def test_precedencia_suma_multiplicacion():
    assert ejecutar("2 + 3 * 4\n") == ["> 14"]

def test_precedencia_parentesis():
    assert ejecutar("(2 + 3) * 4\n") == ["> 20"]

def test_negativo_unario():
    assert ejecutar("-5\n") == ["> -5"]

def test_precedencia_aritmetica_no_mezcla_logica_error():
    resultado = ejecutar('5 + true\n')
    assert any("Error de tipos" in r for r in resultado)

def test_precedencia_comparacion_con_aritmetica():
    assert ejecutar('2 + 3 > 4\n') == ["> True"]

def test_precedencia_logica_con_comparacion():
    assert ejecutar('3 > 2 && 1 < 5\n') == ["> True"]

# ── Variables ─────────────────────────────────────────────────

def test_val_inmutable():
    assert ejecutar("val x = 10\nx\n") == ["> 10"]

def test_val_no_reasignable():
    resultado = ejecutar("val x = 1\nval x = 2\n")
    assert any("redeclararse" in r for r in resultado)

def test_var_mutable():
    assert ejecutar("var x = 0\nx = x + 1\nx = x + 1\nx\n") == ["> 2"]

def test_variable_no_definida():
    resultado = ejecutar("z\n")
    assert any("no definida" in r for r in resultado)

def test_var_no_redeclarable():
    resultado = ejecutar('var x = 1\nvar x = 2\n')
    assert any("redeclararse" in r for r in resultado)

def test_val_y_var_mismo_nombre_error():
    resultado = ejecutar('val x = 1\nvar x = 2\n')
    assert any("redeclararse" in r for r in resultado)

def test_val_no_reasignable_con_asignacion():
    resultado = ejecutar('val x = 1\nx = 5\n')
    assert any("inmutable" in r for r in resultado)

def test_var_si_reasignable():
    assert ejecutar('var x = 1\nx = 5\nprint(x)\n') == ["5"]

# ── Strings ───────────────────────────────────────────────────

def test_string():
    assert ejecutar('"hola"\n') == ['> hola']

def test_string_concatenacion():
    assert ejecutar('"hola" + " risco"\n') == ['> hola risco']

# ── Booleanos ─────────────────────────────────────────────────

def test_booleano_true():
    assert ejecutar("true\n") == ["> True"]

def test_booleano_false():
    assert ejecutar("false\n") == ["> False"]

def test_not_logico():
    assert ejecutar("!true\n") == ["> False"]

# ── Listas ────────────────────────────────────────────────────

def test_lista():
    assert ejecutar("[1, 2, 3]\n") == ["> [1, 2, 3]"]

def test_lista_vacia():
    assert ejecutar("[]\n") == ["> []"]

# ── For ───────────────────────────────────────────────────────

def test_for_lista():
    codigo = "val nums = [1, 2, 3]\nfor n in nums:\n    n\nend\n"
    assert ejecutar(codigo) == ["> 1", "> 2", "> 3"]

def test_for_string():
    codigo = 'val p = "ab"\nfor c in p:\n    c\nend\n'
    assert ejecutar(codigo) == ["> a", "> b"]

def test_for_variable_no_existe_fuera():
    codigo = "val nums = [1]\nfor n in nums:\n    n\nend\nn\n"
    lineas = ejecutar(codigo)
    assert "> 1" in lineas
    assert lineas[-1] != "> 1"

def test_for_anidado():
    codigo = 'val a = [1, 2]\nval b = [3, 4]\nfor x in a:\n    for y in b:\n        print(x + y)\n    end\nend\n'
    assert ejecutar(codigo) == ["4", "5", "5", "6"]

# ── In como expresión ─────────────────────────────────────────

def test_in_verdadero():
    codigo = 'val frutas = ["pera", "uva"]\n"pera" in frutas\n'
    assert ejecutar(codigo) == ["> True"]

def test_in_falso():
    codigo = 'val frutas = ["pera", "uva"]\n"mango" in frutas\n'
    assert ejecutar(codigo) == ["> False"]

def test_in_numero():
    codigo = "val nums = [1, 2, 3]\n2 in nums\n"
    assert ejecutar(codigo) == ["> True"]

# ── Print ─────────────────────────────────────────────────────

def test_print_string():
    assert ejecutar('print("hola")\n') == ["hola"]

def test_print_numero():
    assert ejecutar('print(42)\n') == ["42"]

def test_print_decimal():
    assert ejecutar('print(3.14)\n') == ["3.14"]

def test_print_booleano():
    assert ejecutar('print(true)\n') == ["True"]

def test_print_lista():
    assert ejecutar('print([1, 2, 3])\n') == ["[1, 2, 3]"]

def test_print_null():
    assert ejecutar('print(null)\n') == ["None"]

def test_print_expresion():
    assert ejecutar('print(2 + 3)\n') == ["5"]

def test_print_variable():
    assert ejecutar('val x = 10\nprint(x)\n') == ["10"]

# ── Errores de tipos ──────────────────────────────────────────

def test_suma_string_numero_error():
    assert any("Error de tipos" in r for r in ejecutar('"hola" + 3\n'))

def test_suma_numero_string_error():
    assert any("Error de tipos" in r for r in ejecutar('3 + "hola"\n'))

def test_resta_strings_error():
    assert any("Error de tipos" in r for r in ejecutar('"hola" - "h"\n'))

def test_multiplicacion_string_numero_error():
    assert any("Error de tipos" in r for r in ejecutar('"hola" * 3\n'))

def test_division_string_error():
    assert any("Error de tipos" in r for r in ejecutar('"hola" / 2\n'))

def test_modulo_string_error():
    assert any("Error de tipos" in r for r in ejecutar('"hola" % 2\n'))

def test_not_sobre_numero_error():
    assert any("Error de tipos" in r for r in ejecutar('!5\n'))

def test_not_sobre_string_error():
    assert any("Error de tipos" in r for r in ejecutar('!"hola"\n'))

def test_potencia_booleano_error():
    assert any("Error de tipos" in r for r in ejecutar('true ^ 2\n'))

def test_potencia_string_error():
    assert any("Error de tipos" in r for r in ejecutar('"hola" ^ 2\n'))

def test_suma_con_null_error():
    assert any("Error de tipos" in r for r in ejecutar('null + 1\n'))

def test_suma_booleanos_error():
    assert any("no está definido para Bool" in r for r in ejecutar('true + false\n'))

def test_suma_bool_numero_error():
    assert any("Error de tipos" in r for r in ejecutar('true + 1\n'))

def test_numero_mas_bool_error():
    assert any("Error de tipos" in r for r in ejecutar('1 + true\n'))

def test_resta_bool_error():
    assert any("Error de tipos" in r for r in ejecutar('true - 1\n'))

def test_in_derecha_invalida():
    assert any("Error" in r for r in ejecutar('1 in 5\n'))

# ── Tipos válidos ─────────────────────────────────────────────

def test_suma_strings_valida():
    assert ejecutar('"hola" + " mundo"\n') == ["> hola mundo"]

def test_suma_numeros_valida():
    assert ejecutar('3 + 4\n') == ["> 7"]

def test_suma_listas_valida():
    assert ejecutar('[1, 2] + [3, 4]\n') == ["> [1, 2, 3, 4]"]

def test_not_booleano_valido():
    assert ejecutar('!false\n') == ["> True"]

# ── Operadores lógicos ────────────────────────────────────────

def test_and_no_booleano_error():
    assert any("Error de tipos" in r for r in ejecutar('5 && true\n'))

def test_or_no_booleano_error():
    assert any("Error de tipos" in r for r in ejecutar('5 || true\n'))

def test_igualdad_tipos_distintos_error():
    assert any("Error de tipos" in r for r in ejecutar('5 == "hola"\n'))

def test_relacional_string_error():
    assert any("Error de tipos" in r for r in ejecutar('"hola" > "mundo"\n'))

def test_relacional_booleano_error():
    assert any("Error de tipos" in r for r in ejecutar('true > false\n'))

def test_and_valido():
    assert ejecutar('true && false\n') == ["> False"]

def test_or_valido():
    assert ejecutar('true || false\n') == ["> True"]

def test_igualdad_numeros():
    assert ejecutar('5 == 5\n') == ["> True"]

def test_igualdad_strings():
    assert ejecutar('"hola" == "hola"\n') == ["> True"]

def test_relacional_valido():
    assert ejecutar('5 > 3\n') == ["> True"]

# ── If / elif / else ──────────────────────────────────────────

def test_if_verdadero():
    codigo = 'val x = 5\nif x > 3:\n    print("mayor")\nend\n'
    assert ejecutar(codigo) == ["mayor"]

def test_if_falso():
    codigo = 'val x = 1\nif x > 3:\n    print("mayor")\nend\n'
    assert ejecutar(codigo) == []

def test_if_else_verdadero():
    codigo = 'val x = 5\nif x > 3:\n    print("mayor")\nelse:\n    print("menor")\nend\n'
    assert ejecutar(codigo) == ["mayor"]

def test_if_else_falso():
    codigo = 'val x = 1\nif x > 3:\n    print("mayor")\nelse:\n    print("menor")\nend\n'
    assert ejecutar(codigo) == ["menor"]

def test_if_elif_verdadero():
    codigo = 'val x = 5\nif x > 10:\n    print("grande")\nelif x > 3:\n    print("medio")\nelse:\n    print("pequeño")\nend\n'
    assert ejecutar(codigo) == ["medio"]

def test_if_multiples_elif():
    codigo = 'val x = 0\nif x > 0:\n    print("positivo")\nelif x < 0:\n    print("negativo")\nelif x == 0:\n    print("cero")\nend\n'
    assert ejecutar(codigo) == ["cero"]

def test_if_condicion_no_bool_error():
    resultado = ejecutar('if 5:\n    print("algo")\nend\n')
    assert any("Error de tipos" in r for r in resultado)

def test_if_solo_elif_sin_else():
    codigo = 'val x = 2\nif x > 5:\n    print("grande")\nelif x > 1:\n    print("medio")\nend\n'
    assert ejecutar(codigo) == ["medio"]

def test_if_anidado():
    codigo = 'val x = 5\nif x > 0:\n    if x > 3:\n        print("mayor que 3")\n    end\nend\n'
    assert ejecutar(codigo) == ["mayor que 3"]

# ── While ─────────────────────────────────────────────────────

def test_while_basico():
    codigo = 'var i = 0\nwhile i < 3:\n    print(i)\n    i = i + 1\nend\n'
    assert ejecutar(codigo) == ["0", "1", "2"]

def test_while_no_ejecuta_si_falso():
    codigo = 'var i = 5\nwhile i < 3:\n    print(i)\nend\n'
    assert ejecutar(codigo) == []

def test_while_condicion_no_bool_error():
    resultado = ejecutar('while 1:\n    print("algo")\nend\n')
    assert any("Error de tipos" in r for r in resultado)

def test_while_con_acumulador():
    codigo = 'var suma = 0\nvar i = 1\nwhile i <= 5:\n    suma = suma + i\n    i = i + 1\nend\nprint(suma)\n'
    assert ejecutar(codigo) == ["15"]

def test_while_modifica_variable_externa():
    codigo = 'var x = 10\nwhile x > 0:\n    x = x - 3\nend\nprint(x)\n'
    assert ejecutar(codigo) == ["-2"]

# ── Extensión inválida ────────────────────────────────────────

def test_extension_invalida():
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        f.write(b'val x = 5\n')
        nombre = f.name
    interprete = RISCO()
    resultado = []
    try:
        interprete.ejecutar_archivo(nombre)
    except SystemExit:
        resultado = ["extension invalida"]
    finally:
        os.unlink(nombre)
    assert len(resultado) > 0

# ── input() ───────────────────────────────────────────────────

def test_input_devuelve_texto():
    codigo = 'val x = input("prompt")\nprint(x)\n'
    assert ejecutar_con_input(codigo, ["hola"]) == ["hola"]

def test_input_prompt_vacio():
    codigo = 'val x = input("")\nprint(x)\n'
    assert ejecutar_con_input(codigo, ["risco"]) == ["risco"]

def test_input_con_casteo_num():
    codigo = 'val n = num(input("num: "))\nprint(n + 1)\n'
    assert ejecutar_con_input(codigo, ["10"]) == ["11"]

def test_input_con_casteo_decimal():
    codigo = 'val d = decimal(input("dec: "))\nprint(d)\n'
    assert ejecutar_con_input(codigo, ["3.14"]) == ["3.14"]

def test_input_multiples():
    codigo = 'val a = input("a: ")\nval b = input("b: ")\nprint(a + b)\n'
    assert ejecutar_con_input(codigo, ["hola", " risco"]) == ["hola risco"]

def test_input_en_condicional():
    codigo = (
        'val edad = num(input("edad: "))\n'
        'if edad >= 18:\n'
        '    print("mayor")\n'
        'else:\n'
        '    print("menor")\n'
        'end\n'
    )
    assert ejecutar_con_input(codigo, ["20"]) == ["mayor"]
    assert ejecutar_con_input(codigo, ["15"]) == ["menor"]

def test_input_en_bucle():
    codigo = (
        'val n = num(input("n: "))\n'
        'var i = 0\n'
        'while i < n:\n'
        '    print(i)\n'
        '    i = i + 1\n'
        'end\n'
    )
    assert ejecutar_con_input(codigo, ["3"]) == ["0", "1", "2"]

def test_input_string_invalido_para_num():
    codigo = 'val x = num(input("val: "))\nprint(x)\n'
    resultado = ejecutar_con_input(codigo, ["abc"])
    assert any("Error" in r or "no se puede" in r.lower() for r in resultado)


# ══════════════════════════════════════════════════════════════
#  MÓDULO MAT — tests unitarios de primitivas (Python puro)
#
#  Estas pruebas importan directamente las funciones de nivel
#  de módulo de visitante_evaluador.py, sin pasar por ANTLR.
#  Esto las hace instantáneas y fáciles de depurar.
#
#  Tolerancias:
#    cerca(a, b, rel, abs_) →  |a-b| ≤ max(abs_, rel·|b|)
#    Para valores grandes (ej. exp(100)) se usa error relativo
#    explícito para evitar falsos negativos por magnitud.
# ══════════════════════════════════════════════════════════════

# ── _prim_sqrt ────────────────────────────────────────────────

class TestSqrt:
    """Raíz cuadrada — Newton-Raphson con parada por tolerancia."""

    def test_sqrt_cero(self):
        assert _prim_sqrt(0) == 0.0

    def test_sqrt_uno(self):
        assert cerca(_prim_sqrt(1), 1.0)

    def test_sqrt_cuatro(self):
        assert cerca(_prim_sqrt(4), 2.0)

    def test_sqrt_dos(self):
        """√2 verificado contra math.sqrt como referencia."""
        assert cerca(_prim_sqrt(2), math.sqrt(2))

    def test_sqrt_valor_grande(self):
        """√1e12 = 1e6 exacto en Float64."""
        assert cerca(_prim_sqrt(1e12), 1e6)

    def test_sqrt_decimal(self):
        assert cerca(_prim_sqrt(0.25), 0.5)

    def test_sqrt_negativo_devuelve_none(self):
        """Dominio inválido → None (el visitor convierte esto en Err)."""
        assert _prim_sqrt(-1) is None

    def test_sqrt_negativo_cualquier_valor(self):
        assert _prim_sqrt(-100) is None

    def test_sqrt_consistencia_con_math(self):
        """Verificar contra math.sqrt para un rango representativo."""
        for x in [0.01, 0.5, 3, 7, 100, 9999.9]:
            assert cerca(_prim_sqrt(x), math.sqrt(x)), f"Falla en sqrt({x})"


# ── _prim_exp ─────────────────────────────────────────────────

class TestExp:
    """Exponencial — reducción de rango + serie de Taylor."""

    def test_exp_cero(self):
        assert _prim_exp(0) == 1.0

    def test_exp_uno(self):
        """e^1 = e."""
        assert cerca(_prim_exp(1), math.e)

    def test_exp_negativo_uno(self):
        """e^-1 = 1/e."""
        assert cerca(_prim_exp(-1), 1.0 / math.e)

    def test_exp_dos(self):
        assert cerca(_prim_exp(2), math.exp(2))

    def test_exp_diez(self):
        assert cerca(_prim_exp(10), math.exp(10))

    def test_exp_negativo_diez(self):
        assert cerca(_prim_exp(-10), math.exp(-10))

    def test_exp_cien(self):
        """
        e^100 ≈ 2.688e43. Se mide error relativo para evitar
        falsos negativos por magnitud del número.
        """
        esperado = math.exp(100)
        resultado = _prim_exp(100)
        error_relativo = abs(resultado - esperado) / abs(esperado)
        assert error_relativo < 1e-9, f"Error relativo {error_relativo} > 1e-9"

    def test_exp_negativo_cien(self):
        assert cerca(_prim_exp(-100), math.exp(-100), rel=1e-9)

    def test_exp_consistencia_con_math(self):
        for x in [-5.5, -1.0, 0.0, 0.5, 1.0, 5.0, 20.0]:
            assert cerca(_prim_exp(x), math.exp(x)), f"Falla en exp({x})"

    def test_exp_fraccionario(self):
        """e^0.5 = √e."""
        assert cerca(_prim_exp(0.5), math.sqrt(math.e))


# ── _prim_log ─────────────────────────────────────────────────

class TestLog:
    """Logaritmo natural — reducción de rango + arctanh."""

    def test_log_uno(self):
        assert _prim_log(1.0) == 0.0

    def test_log_e(self):
        """ln(e) = 1."""
        assert cerca(_prim_log(math.e), 1.0)

    def test_log_dos(self):
        """ln(2) debe coincidir con la constante interna _LN2."""
        assert cerca(_prim_log(2.0), _LN2)

    def test_log_diez(self):
        assert cerca(_prim_log(10.0), math.log(10.0))

    def test_log_cien(self):
        assert cerca(_prim_log(100.0), math.log(100.0))

    def test_log_mil(self):
        """Caso difícil para la serie directa (~200 iter); aquí ≤15."""
        assert cerca(_prim_log(1000.0), math.log(1000.0))

    def test_log_fraccion(self):
        """ln(0.5) = -ln(2) = -_LN2."""
        assert cerca(_prim_log(0.5), -_LN2)

    def test_log_cero_devuelve_none(self):
        assert _prim_log(0.0) is None

    def test_log_negativo_devuelve_none(self):
        assert _prim_log(-1.0) is None

    def test_log_consistencia_con_math(self):
        for x in [0.001, 0.1, 0.5, 1.0, 2.0, math.e, 10.0, 100.0, 1e6]:
            assert cerca(_prim_log(x), math.log(x)), f"Falla en log({x})"

    def test_log_exp_inversa(self):
        """Propiedad inversa: ln(e^x) == x."""
        for x in [-3.0, 0.0, 1.0, 5.0, 10.0]:
            resultado = _prim_log(_prim_exp(x))
            assert cerca(resultado, x, abs_=1e-9), f"ln(exp({x})) = {resultado}"


# ── _prim_matmul ──────────────────────────────────────────────

class TestMatmul:
    """Multiplicación matricial A × B — orden i→k→j."""

    def test_matmul_1x1(self):
        assert matrices_iguales(_prim_matmul([[3.0]], [[4.0]]), [[12.0]])

    def test_matmul_2x2(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        assert matrices_iguales(_prim_matmul(A, B), [[19.0, 22.0], [43.0, 50.0]])

    def test_matmul_rectangular(self):
        """2×3 × 3×2 → 2×2."""
        A = [[1, 2, 3], [4, 5, 6]]
        B = [[7, 8], [9, 10], [11, 12]]
        assert matrices_iguales(_prim_matmul(A, B), [[58.0, 64.0], [139.0, 154.0]])

    def test_matmul_vector_columna(self):
        """2×2 × 2×1 → 2×1."""
        A = [[1, 2], [3, 4]]
        B = [[5], [6]]
        assert matrices_iguales(_prim_matmul(A, B), [[17.0], [39.0]])

    def test_matmul_identidad(self):
        """A × I = A."""
        A = [[1, 2], [3, 4]]
        I = [[1, 0], [0, 1]]
        assert matrices_iguales(_prim_matmul(A, I), [[1.0, 2.0], [3.0, 4.0]])

    def test_matmul_dimensiones_incompatibles(self):
        """cols(A) != filas(B) → None."""
        assert _prim_matmul([[1, 2]], [[1, 2]]) is None

    def test_matmul_con_ceros(self):
        A = [[0, 0], [0, 0]]
        B = [[1, 2], [3, 4]]
        assert matrices_iguales(_prim_matmul(A, B), [[0.0, 0.0], [0.0, 0.0]])


# ── _prim_matmulT ─────────────────────────────────────────────

class TestMatmulT:
    """Multiplicación A × B^T sin construir la transpuesta."""

    def test_matmulT_basico(self):
        """
        A = [[1,2],[3,4]]  B = [[1,2],[3,4]]
        A × B^T = [[5, 11], [11, 25]]
        """
        A = [[1, 2], [3, 4]]
        B = [[1, 2], [3, 4]]
        assert matrices_iguales(_prim_matmulT(A, B), [[5.0, 11.0], [11.0, 25.0]])

    def test_matmulT_equivale_a_matmul_transpuesta(self):
        A = [[1, 2, 3], [4, 5, 6]]          # 2×3
        B = [[1, 2, 3], [4, 5, 6]]          # 2×3  → B^T es 3×2
        # mulT(A, B) = A × B^T = (2×3)(3×2) = 2×2
        C_mulT = _prim_matmulT(A, B)
        BT = [[B[j][i] for j in range(len(B))] for i in range(len(B[0]))]
        C_ref = _prim_matmul(A, BT)
        assert matrices_iguales(C_mulT, C_ref)

    def test_matmulT_dimensiones_incompatibles(self):
        """cols(A) != cols(B) → None."""
        assert _prim_matmulT([[1, 2, 3]], [[1, 2]]) is None

    def test_matmulT_1x1(self):
        assert matrices_iguales(_prim_matmulT([[3.0]], [[4.0]]), [[12.0]])


# ── _prim_matmulAdd ───────────────────────────────────────────

class TestMatmulAdd:
    """A × W + b — capa densa en un solo recorrido."""

    def test_matmulAdd_basico(self):
        """
        [[1,2]] × I + [10, 20] = [[11, 22]]
        """
        A = [[1.0, 2.0]]
        W = [[1.0, 0.0], [0.0, 1.0]]
        b = [10.0, 20.0]
        assert matrices_iguales(_prim_matmulAdd(A, W, b), [[11.0, 22.0]])

    def test_matmulAdd_equivale_matmul_mas_bias(self):
        """mulAdd(A,W,b) == mul(A,W) + b elemento a elemento."""
        A = [[1, 2, 3], [4, 5, 6]]
        W = [[1, 0], [0, 1], [1, 1]]
        b = [100.0, 200.0]
        C_add = _prim_matmulAdd(A, W, b)
        C_mul = _prim_matmul(A, W)
        C_ref = [[C_mul[i][j] + b[j] for j in range(len(b))]
                 for i in range(len(C_mul))]
        assert matrices_iguales(C_add, C_ref)

    def test_matmulAdd_dimension_incompatible(self):
        """cols(A) != filas(W) → None."""
        assert _prim_matmulAdd([[1, 2]], [[1], [2], [3]], [0.0]) is None

    def test_matmulAdd_bias_cero(self):
        """Con bias cero el resultado es idéntico a matmul."""
        A = [[1, 2], [3, 4]]
        W = [[1, 0], [0, 1]]
        b = [0.0, 0.0]
        assert matrices_iguales(_prim_matmulAdd(A, W, b), [[1.0, 2.0], [3.0, 4.0]])


# ── LCG ───────────────────────────────────────────────────────

class TestLCG:
    """Generador Congruencial Lineal — parámetros POSIX."""

    def test_lcg_rango(self):
        """1000 valores consecutivos deben estar en [0.0, 1.0)."""
        _prim_lcg_seed(0)
        for _ in range(1000):
            v = _prim_lcg_next()
            assert 0.0 <= v < 1.0, f"Valor fuera de rango: {v}"

    def test_lcg_reproducibilidad(self):
        """La misma semilla siempre produce la misma secuencia."""
        _prim_lcg_seed(42)
        seq1 = [_prim_lcg_next() for _ in range(10)]
        _prim_lcg_seed(42)
        seq2 = [_prim_lcg_next() for _ in range(10)]
        assert seq1 == seq2

    def test_lcg_semillas_distintas_dan_secuencias_distintas(self):
        _prim_lcg_seed(1)
        seq1 = [_prim_lcg_next() for _ in range(5)]
        _prim_lcg_seed(2)
        seq2 = [_prim_lcg_next() for _ in range(5)]
        assert seq1 != seq2

    def test_lcg_no_todos_iguales(self):
        """La secuencia no debe ser constante."""
        _prim_lcg_seed(999)
        valores = {_prim_lcg_next() for _ in range(20)}
        assert len(valores) > 1

    def test_lcg_valor_exacto_primer_paso(self):
        """
        Semilla 0:
        siguiente = (1664525·0 + 1013904223) mod 2^32 = 1013904223
        valor     = 1013904223 / 4294967296
        """
        _prim_lcg_seed(0)
        v = _prim_lcg_next()
        assert abs(v - 1013904223 / (2 ** 32)) < 1e-15

    def test_lcg_semilla_grande(self):
        """Semilla > 2^32 se reduce con módulo, igual que semilla 0."""
        _prim_lcg_seed(0)
        v_ref = _prim_lcg_next()
        _prim_lcg_seed(2 ** 33)   # 2^33 mod 2^32 == 0
        v_test = _prim_lcg_next()
        assert v_ref == v_test


# ── Constante _LN2 ────────────────────────────────────────────

class TestConstanteLN2:
    """_LN2 debe coincidir con math.log(2) hasta el límite de Float64."""

    def test_ln2_precision(self):
        assert abs(_LN2 - math.log(2)) < 1e-15


class TestMatRC:
    """Tests de mat.rc — funciones escritas en RISCO puro."""

    # Escalares
    def test_mat_abs_positivo(self):
        assert ejecutar('print(mat_abs(5))\n') == ['5']

    def test_mat_abs_negativo(self):
        assert ejecutar('print(mat_abs(-3))\n') == ['3']

    def test_mat_pow(self):
        assert ejecutar('print(mat_pow(2, 10))\n') == ['1024']

    def test_mat_sqrt_via_risco(self):
        assert ejecutar('print(mat_sqrt(9.0))\n') == ["('ok', 3.0)"]

    # Estadística
    def test_mat_sum(self):
        assert ejecutar('print(mat_sum([1, 2, 3, 4]))\n') == ['10']

    def test_mat_mean(self):
        assert ejecutar('print(mat_mean([2.0, 4.0, 6.0]))\n') == ['4.0']

    def test_mat_min(self):
        assert ejecutar('print(mat_min([3, 1, 4, 1, 5]))\n') == ['1']

    def test_mat_max(self):
        assert ejecutar('print(mat_max([3, 1, 4, 1, 5]))\n') == ['5']

    # Vectores
    def test_mat_scale(self):
        assert ejecutar('print(mat_scale(2, [1, 2, 3]))\n') == ['[2, 4, 6]']

    def test_mat_dot(self):
        assert ejecutar('print(mat_dot([1, 2, 3], [4, 5, 6]))\n') == ['32']

    def test_mat_vadd(self):
        assert ejecutar('print(mat_vadd([1, 2], [3, 4]))\n') == ['[4, 6]']

    def test_mat_dot_largo_distinto(self):
        assert ejecutar('print(mat_dot([1, 2], [1, 2, 3]))\n') == ['None']

    # Matrices
    def test_mat_shape(self):
        assert ejecutar('print(mat_shape([[1,2],[3,4],[5,6]]))\n') == ['[3, 2]']

    def test_mat_zeros(self):
        assert ejecutar('print(mat_zeros(2, 3))\n') == ['[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]']

    def test_mat_ones(self):
        assert ejecutar('print(mat_ones(1, 3))\n') == ['[[1.0, 1.0, 1.0]]']

    def test_mat_identity(self):
        assert ejecutar('print(mat_identity(2))\n') == ['[[1.0, 0.0], [0.0, 1.0]]']

    def test_mat_T(self):
        assert ejecutar('print(mat_T([[1,2,3],[4,5,6]]))\n') == ['[[1, 4], [2, 5], [3, 6]]']

    def test_mat_fromList(self):
        assert ejecutar('print(mat_fromList([1,2,3,4], 2, 2))\n') == ['[[1, 2], [3, 4]]']

    def test_mat_fromList_dimension_invalida(self):
        assert ejecutar('print(mat_fromList([1,2,3], 2, 2))\n') == ['None']

    def test_mat_get(self):
        assert ejecutar('val M = [[1,2],[3,4]]\nprint(mat_get(M, 1, 0))\n') == ['3']

    def test_mat_get_fuera_de_rango(self):
        assert ejecutar('print(mat_get([[1,2]], 5, 0))\n') == ['None']

    def test_mat_row(self):
        assert ejecutar('print(mat_row([[1,2],[3,4]], 1))\n') == ['[3, 4]']

    def test_mat_col(self):
        assert ejecutar('print(mat_col([[1,2],[3,4]], 0))\n') == ['[1, 3]']

    def test_mat_mul(self):
        codigo = (
            'val A = [[1,2],[3,4]]\n'
            'val B = [[5,6],[7,8]]\n'
            'print(mat_mul(A, B))\n'
        )
        assert ejecutar(codigo) == ["('ok', [[19.0, 22.0], [43.0, 50.0]])"]

    # Seed + random (verificamos reproducibilidad)
    def test_mat_seed_reproducible(self):
        codigo = (
            'mat_seed(42)\n'
            'val a = mat_random(1, 3)\n'
            'mat_seed(42)\n'
            'val b = mat_random(1, 3)\n'
            'print(a == b)\n'
        )
        assert ejecutar(codigo) == ['True']
# ── file.rc ───────────────────────────────────────────────────
# ── file.rc ───────────────────────────────────────────────────

def test_file_writePath_y_readPath():
    codigo = (
        'file_writePath("archivo_test.txt", "hola risco")\n'
        'print(file_readPath("archivo_test.txt"))\n'
        'print(file_delete("archivo_test.txt"))\n'
    )
    resultado = ejecutar(codigo)
    assert resultado[0] == "hola risco"
    assert resultado[1] == "True"

def test_file_exists():
    codigo = (
        'file_writePath("archivo_exists.txt", "ok")\n'
        'print(file_exists("archivo_exists.txt"))\n'
        'print(file_delete("archivo_exists.txt"))\n'
    )
    resultado = ejecutar(codigo)
    assert resultado[0] == "True"
    assert resultado[1] == "True"

def test_file_readLinesPath():
    codigo = (
        'file_writePath("archivo_lineas.txt", "uno\\ndos\\ntres")\n'
        'print(file_readLinesPath("archivo_lineas.txt"))\n'
        'print(file_delete("archivo_lineas.txt"))\n'
    )
    resultado = ejecutar(codigo)
    assert resultado[0] == "[uno, dos, tres]"
    assert resultado[1] == "True"

def test_file_appendLine():
    codigo = (
        'file_writePath("archivo_append.txt", "linea1")\n'
        'file_appendLine("archivo_append.txt", "linea2")\n'
        'print(file_readPath("archivo_append.txt"))\n'
        'print(file_delete("archivo_append.txt"))\n'
    )
    resultado = ejecutar(codigo)
    assert "linea1" in resultado[0]
    assert "linea2" in resultado[0]
    assert resultado[1] == "True"

def test_file_writeLines():
    codigo = (
        'val xs = ["a", "b", "c"]\n'
        'file_writeLines("archivo_write_lines.txt", xs)\n'
        'print(file_readLinesPath("archivo_write_lines.txt"))\n'
        'print(file_delete("archivo_write_lines.txt"))\n'
    )
    resultado = ejecutar(codigo)
    assert resultado[0] == "[a, b, c]"
    assert resultado[1] == "True"

def test_file_readCSV():
    codigo = (
        'file_writePath("archivo_csv.txt", "a,b,c\\n1,2,3\\nx,y,z")\n'
        'print(file_readCSV("archivo_csv.txt"))\n'
        'print(file_delete("archivo_csv.txt"))\n'
    )
    resultado = ejecutar(codigo)
    assert resultado[0] == "[[a, b, c], [1, 2, 3], [x, y, z]]"
    assert resultado[1] == "True"

def test_file_readPath_archivo_inexistente():
    codigo = 'print(file_readPath("no_existe.txt"))\n'
    resultado = ejecutar(codigo)
    assert resultado == ["None"]

def test_file_delete_archivo_inexistente():
    codigo = 'print(file_delete("no_existe.txt"))\n'
    resultado = ejecutar(codigo)
    assert resultado == ["False"]

# ── visual.rc ─────────────────────────────────────────────────

def test_visual_bar_genera_svg():
    codigo = (
        'visual_bar(["A","B","C"], [10,20,30], "Barras", "Categoria", "Valor", "bar_test.svg")\n'
        'print(file_exists("bar_test.svg"))\n'
        'print(file_readPath("bar_test.svg"))\n'
        'print(file_delete("bar_test.svg"))\n'
    )
    resultado = ejecutar(codigo)
    assert resultado[0] == "True"
    assert "<svg" in resultado[1]
    assert "<rect" in resultado[1]
    assert "Barras" in resultado[1]
    assert resultado[2] == "True"


def test_visual_line_genera_svg():
    codigo = (
        'visual_line([10,20,15,30], "Linea", "X", "Y", "line_test.svg")\n'
        'print(file_exists("line_test.svg"))\n'
        'print(file_readPath("line_test.svg"))\n'
        'print(file_delete("line_test.svg"))\n'
    )
    resultado = ejecutar(codigo)
    assert resultado[0] == "True"
    assert "<svg" in resultado[1]
    assert "<polyline" in resultado[1]
    assert "Linea" in resultado[1]
    assert resultado[2] == "True"


def test_visual_scatter_genera_svg():
    codigo = (
        'visual_scatter([1,2,3], [4,5,6], "Scatter", "X", "Y", "scatter_test.svg")\n'
        'print(file_exists("scatter_test.svg"))\n'
        'print(file_readPath("scatter_test.svg"))\n'
        'print(file_delete("scatter_test.svg"))\n'
    )
    resultado = ejecutar(codigo)
    assert resultado[0] == "True"
    assert "<svg" in resultado[1]
    assert "<circle" in resultado[1]
    assert "Scatter" in resultado[1]
    assert resultado[2] == "True"


def test_visual_hist_genera_svg():
    codigo = (
        'visual_hist([4,7,10,8,12], "Hist", "Bins", "Frecuencia", "hist_test.svg")\n'
        'print(file_exists("hist_test.svg"))\n'
        'print(file_readPath("hist_test.svg"))\n'
        'print(file_delete("hist_test.svg"))\n'
    )
    resultado = ejecutar(codigo)
    assert resultado[0] == "True"
    assert "<svg" in resultado[1]
    assert "<rect" in resultado[1]
    assert "Hist" in resultado[1]
    assert resultado[2] == "True"

def test_memory_info_funciona():
    codigo = (
        'val x = 10\n'
        'print(memory_info())\n'
    )
    resultado = ejecutar(codigo)
    assert "variables=" in resultado[0]
    assert "recursion=" in resultado[0]


def test_memory_free_libera_variable_mutable():
    codigo = (
        'var xs = [1,2,3]\n'
        'print(memory_info())\n'
        'memory_free("xs")\n'
        'print(memory_info())\n'
    )

    resultado = ejecutar(codigo)

    assert "listas=1" in resultado[0]
    assert "celdas=3" in resultado[0]

    assert "listas=0" in resultado[1]
    assert "celdas=0" in resultado[1]
def test_memory_free_no_libera_val():
    codigo = (
        'val xs = [1,2,3]\n'
        'memory_free("xs")\n'
    )

    resultado = ejecutar(codigo)

    assert any("variables val" in r for r in resultado)


def test_factorial_iterativo_20():
    codigo = (
        'fact(n) =>\n'
        '    var acc = 1\n'
        '    var i = 1\n'
        '    while i <= n:\n'
        '        acc = acc * i\n'
        '        i = i + 1\n'
        '    end\n'
        '    return acc\n'
        'end\n'
        'print(fact(20))\n'
    )
    resultado = ejecutar(codigo)
    assert resultado[0] == "2432902008176640000"