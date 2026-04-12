import pytest
import sys
import os
from io import StringIO

# Para que encuentre los módulos de src y gramaticas
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.risco import RISCO

def ejecutar(codigo):
    """Ejecuta código RISCO y captura lo que imprime"""
    captura = StringIO()
    sys.stdout = captura
    interprete = RISCO(modo_interactivo=True)
    interprete._ejecutar_codigo(codigo)
    sys.stdout = sys.__stdout__
    return [l.strip() for l in captura.getvalue().strip().splitlines() if l.strip()]


# Operaciones básicas 

def test_suma():
    assert ejecutar("val x = 5\nval y = 3\nx + y\n") == ["> 8"]

def test_resta():
    assert ejecutar("val x = 5\nval y = 3\nx - y\n") == ["> 2"]

def test_multiplicacion():
    assert ejecutar("val x = 5\nval y = 3\nx * y\n") == ["> 15"]

def test_division():
    resultado = ejecutar("val x = 5\nval y = 3\nx / y\n")
    assert resultado == ["> 1.6666666666666667"]

def test_division_por_cero():
    resultado = ejecutar("1 / 0\n")
    assert any("División por cero" in r for r in resultado)

def test_modulo():
    assert ejecutar("10 % 3\n") == ["> 1"]

def test_potencia():
    assert ejecutar("2 ^ 3\n") == ["> 8"]

def test_potencia_asociatividad_derecha():
    assert ejecutar('2 ^ 3 ^ 2\n') == ["> 512"]

# Precedencia

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
    # 2 + 3 > 4 debe evaluarse como (2+3) > 4 = True
    assert ejecutar('2 + 3 > 4\n') == ["> True"]

def test_precedencia_logica_con_comparacion():
    # 3 > 2 && 1 < 5 debe evaluarse como (3>2) && (1<5) = True
    assert ejecutar('3 > 2 && 1 < 5\n') == ["> True"]

# Variables 

def test_val_inmutable():
    resultado = ejecutar("val x = 10\nx\n")
    assert resultado == ["> 10"]

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

# Strings 

def test_string():
    assert ejecutar('"hola"\n') == ['> hola']

def test_string_concatenacion():
    assert ejecutar('"hola" + " risco"\n') == ['> hola risco']


#  Booleanos

def test_booleano_true():
    assert ejecutar("true\n") == ["> True"]

def test_booleano_false():
    assert ejecutar("false\n") == ["> False"]

def test_not_logico():
    assert ejecutar("!true\n") == ["> False"]


# Listas

def test_lista():
    assert ejecutar("[1, 2, 3]\n") == ["> [1, 2, 3]"]

def test_lista_vacia():
    assert ejecutar("[]\n") == ["> []"]


# For

def test_for_lista():
    codigo = "val nums = [1, 2, 3]\nfor n in nums:\n    n\nend\n"
    assert ejecutar(codigo) == ["> 1", "> 2", "> 3"]

def test_for_string():
    codigo = 'val p = "ab"\nfor c in p:\n    c\nend\n'
    assert ejecutar(codigo) == ["> a", "> b"]

def test_for_variable_no_existe_fuera():
    # Después del for, n no debe existir
    codigo = "val nums = [1]\nfor n in nums:\n    n\nend\nn\n"
    lineas = ejecutar(codigo)
    assert "> 1" in lineas       # dentro del for sí imprime
    assert lineas[-1] != "> 1"   # fuera del for no vuelve a imprimir

def test_for_anidado():
    codigo = 'val a = [1, 2]\nval b = [3, 4]\nfor x in a:\n    for y in b:\n        print(x + y)\n    end\nend\n'
    assert ejecutar(codigo) == ["4", "5", "5", "6"]

# In como expresión de comparacion

def test_in_verdadero():
    codigo = 'val frutas = ["pera", "uva"]\n"pera" in frutas\n'
    assert ejecutar(codigo) == ["> True"]

def test_in_falso():
    codigo = 'val frutas = ["pera", "uva"]\n"mango" in frutas\n'
    assert ejecutar(codigo) == ["> False"]

def test_in_numero():
    codigo = "val nums = [1, 2, 3]\n2 in nums\n"
    assert ejecutar(codigo) == ["> True"]

# Print

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

# Validación de tipos con errores

def test_suma_string_numero_error():
    resultado = ejecutar('"hola" + 3\n')
    assert any("Error de tipos" in r for r in resultado)

def test_suma_numero_string_error():
    resultado = ejecutar('3 + "hola"\n')
    assert any("Error de tipos" in r for r in resultado)

def test_resta_strings_error():
    resultado = ejecutar('"hola" - "h"\n')
    assert any("Error de tipos" in r for r in resultado)

def test_multiplicacion_string_numero_error():
    resultado = ejecutar('"hola" * 3\n')
    assert any("Error de tipos" in r for r in resultado)

def test_division_string_error():
    resultado = ejecutar('"hola" / 2\n')
    assert any("Error de tipos" in r for r in resultado)

def test_modulo_string_error():
    resultado = ejecutar('"hola" % 2\n')
    assert any("Error de tipos" in r for r in resultado)

def test_not_sobre_numero_error():
    resultado = ejecutar('!5\n')
    assert any("Error de tipos" in r for r in resultado)

def test_not_sobre_string_error():
    resultado = ejecutar('!"hola"\n')
    assert any("Error de tipos" in r for r in resultado)

def test_potencia_booleano_error():
    resultado = ejecutar('true ^ 2\n')
    assert any("Error de tipos" in r for r in resultado)

def test_potencia_string_error():
    resultado = ejecutar('"hola" ^ 2\n')
    assert any("Error de tipos" in r for r in resultado)

def test_suma_con_null_error():
    resultado = ejecutar('null + 1\n')
    assert any("Error de tipos" in r for r in resultado)

def test_suma_booleanos_error():
    resultado = ejecutar('true + false\n')
    assert any("no está definido para Bool" in r for r in resultado)

def test_suma_bool_numero_error():
    resultado = ejecutar('true + 1\n')
    assert any("Error de tipos" in r for r in resultado)

def test_numero_mas_bool_error():
    resultado = ejecutar('1 + true\n')
    assert any("Error de tipos" in r for r in resultado)

def test_resta_bool_error():
    resultado = ejecutar('true - 1\n')
    assert any("Error de tipos" in r for r in resultado)

def test_in_derecha_invalida():
    resultado = ejecutar('1 in 5\n')
    assert any("Error" in r for r in resultado)

# Operaciones válidas con tipos correctos

def test_suma_strings_valida():
    assert ejecutar('"hola" + " mundo"\n') == ["> hola mundo"]

def test_suma_numeros_valida():
    assert ejecutar('3 + 4\n') == ["> 7"]

def test_suma_listas_valida():
    assert ejecutar('[1, 2] + [3, 4]\n') == ["> [1, 2, 3, 4]"]

def test_not_booleano_valido():
    assert ejecutar('!false\n') == ["> True"]

# Operadores lógicos — solo operan booleanos

def test_and_no_booleano_error():
    resultado = ejecutar('5 && true\n')
    assert any("Error de tipos" in r for r in resultado)

def test_or_no_booleano_error():
    resultado = ejecutar('5 || true\n')
    assert any("Error de tipos" in r for r in resultado)

# Igualdad — tipos distintos

def test_igualdad_tipos_distintos_error():
    resultado = ejecutar('5 == "hola"\n')
    assert any("Error de tipos" in r for r in resultado)

# Relacionales — solo operan sobre números

def test_relacional_string_error():
    resultado = ejecutar('"hola" > "mundo"\n')
    assert any("Error de tipos" in r for r in resultado)

def test_relacional_booleano_error():
    resultado = ejecutar('true > false\n')
    assert any("Error de tipos" in r for r in resultado)

# Casos válidos de comparación lógica y relacional

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

# If/elif/else

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

# While

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

# Extensión Inválida

def test_extension_invalida():
    import tempfile, os
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        f.write(b'val x = 5\n')
        nombre = f.name
    interprete = RISCO()
    # Capturar que lanza error o imprime advertencia
    resultado = []
    try:
        interprete.ejecutar_archivo(nombre)
    except SystemExit:
        resultado = ["extension invalida"]
    finally:
        os.unlink(nombre)
    assert len(resultado) > 0