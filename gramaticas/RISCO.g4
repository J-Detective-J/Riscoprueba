grammar RISCO; 

// Permite compartir estado dentro del parser generado.
// En RISCO la memoria real se maneja en el VisitanteEvaluador,

@parser::members {
    # Memoria para variables
    memoria = {}
}


//  PROGRAMA


// Programa principal - acepta saltos de línea entre sentencias
programa: (NL* sentencia NL*)* EOF;


//  SENTENCIAS


sentencia
    : declaracion_variable
    | asignacion
    | expresion_stmt
    | for_stmt
    | print_stmt
    | if_stmt
    | while_stmt
    | declaracion_funcion  
    | return_stmt            
    ;

// print built-in
print_stmt
    : PRINT '(' expresion ')' NL
    ;

// Declaración de variables
declaracion_variable
    : 'val' IDENTIFICADOR '=' expresion NL
    | 'var' IDENTIFICADOR '=' expresion NL
    ;

// Reasignación de variables
asignacion
    : IDENTIFICADOR '=' expresion NL
    ;

// Expresión como sentencia
expresion_stmt
    : expresion NL
    ;

// Bucle for
for_stmt
    : 'for' IDENTIFICADOR 'in' expresion ':' NL
      (NL* sentencia)*
      END  NL
    ;

// Condicional if/elif/else
if_stmt
    : IF expresion ':' NL 
      (NL* sentencia)*
      (ELIF expresion ':' NL (NL* sentencia)*)*
      (ELSE ':' NL (NL* sentencia)*)?
      END NL
    ;

// Bucle while
while_stmt
    : WHILE expresion ':' NL
      (NL* sentencia)*
      END NL
    ;

//      Declaración de función
//    Soporta dos formas:
//      a) Una línea:    nombre(p1, p2) => expresion NL
//      b) Multilínea:   nombre(p1, p2) => NL  sentencias* end NL
declaracion_funcion
    : IDENTIFICADOR '(' lista_params? ')' '=>' expresion NL           // forma corta
    | IDENTIFICADOR '(' lista_params? ')' '=>' NL                     // forma larga
      (NL* sentencia)*
      END NL
    ;

lista_params
    : IDENTIFICADOR (',' IDENTIFICADOR)*
    ;

// return
return_stmt
    : 'return' expresion NL
    ;



//  EXPRESIONES  (precedencia de menor a mayor)


//  1. Punto de entrada — también permite lambdas anónimas
expresion
    : '(' lista_params? ')' '=>' expresion   // lambda anónima: (x, y) => x + y
    | or_logico
    ;

//  2. OR lógico
or_logico
    : and_logico ('||' and_logico)*
    ;

//  3. AND lógico
and_logico
    : igualdad ('&&' igualdad)*
    ;

//  4. Igualdad / desigualdad
igualdad
    : relacional (('==' | '!=') relacional)*
    ;

//  5. Relacionales
relacional
    : suma (('>' | '<' | '>=' | '<=') suma)*
    ;

//  6. Suma / resta  (+  concatenación de listas y strings)
suma
    : comparacion (('+' | '-') comparacion)*
    ;

//  7. Pertenencia
comparacion
    : termino ('in' termino)?
    ;

//  8. Multiplicación / división / módulo
termino
    : potencia (('*' | '/' | '%') potencia)*
    ;

//  9. Potencia (asociativa por la derecha)
potencia
    : acceso
    | acceso '^' potencia
    ;

// 10. Indexación y llamada a función (mayor precedencia que potencia)
//     Maneja: expr[i]  y  expr[i][j]  encadenados
acceso
    : primario ('[' expresion ']')*   // indexación, posiblemente encadenada
    ;

// 11. Primarios
primario
    : NUMERO
    | DECIMAL
    | STRING
    | BOOLEANO
    | NULL
    | lista
    | llamada_funcion                 // nombre(args) o builtin(args)
    | casteo                          // num(x) decimal(x) texto(x) bool(x)
    | IDENTIFICADOR
    | '(' expresion ')'
    | '-' primario                    // negativo unario
    | '!' primario                    // not lógico
    ;


//  COLECCIONES


lista
    : '[' (expresion (',' expresion)*)? ']'
    ;


//  LLAMADAS A FUNCIÓN


llamada_funcion
    : IDENTIFICADOR '(' lista_args? ')'
    | LONG_F '(' lista_args? ')'      // built-in: long()
    | RANGE_F '(' lista_args? ')'     // built-in: range()
    | MAP_F '(' lista_args? ')'       // built-in: map()
    | FILTER_F '(' lista_args? ')'    // built-in: filter()
    | REDUCE_F '(' lista_args? ')'    // built-in: reduce()
    | UNWRAP_F '(' lista_args? ')'    // built-in: unwrap()
    | FREE_F '(' lista_args? ')'      // built-in: free()
    ;

lista_args
    : argumento (',' argumento)*
    ;

// Un argumento puede ser una expresión normal o una lambda anónima
argumento
    : expresion
    ;


//  CASTEO EXPLÍCITO

//  num(x)
//  decimal(x)
//  texto(x)
//  bool(x)

casteo
    : NUM_CAST    '(' expresion ')'
    | DECIMAL_CAST '(' expresion ')'
    | TEXTO_CAST  '(' expresion ')'
    | BOOL_CAST   '(' expresion ')'
    ;



//  TOKENS DE PALABRAS RESERVADAS


FOR          : 'for';
IN           : 'in';
END          : 'end';
VAL          : 'val';
VAR          : 'var';
PRINT        : 'print';
IF           : 'if';
ELIF         : 'elif';
ELSE         : 'else';
WHILE        : 'while';
RETURN       : 'return';

// Built-ins como tokens para que no colisionen con IDENTIFICADOR

LONG_F       : 'long';
RANGE_F      : 'range';
MAP_F        : 'map';
FILTER_F     : 'filter';
REDUCE_F     : 'reduce';
UNWRAP_F     : 'unwrap';
FREE_F       : 'free';

// Casteos como tokens reservados
NUM_CAST     : 'num';
DECIMAL_CAST : 'decimal';
TEXTO_CAST   : 'texto';
BOOL_CAST    : 'bool';


//  TOKENS DE OPERADORES


AND  : '&&';
OR   : '||';
EQ   : '==';
NEQ  : '!=';
GTE  : '>=';
LTE  : '<=';


//  TOKENS LÉXICOS


NUMERO       : DIGITO+;
DECIMAL      : DIGITO+ '.' DIGITO+;
STRING       : '"' ( ~["\r\n] | '\\"' )* '"';
BOOLEANO     : 'true' | 'false';
NULL         : 'null';
IDENTIFICADOR: LETRA (LETRA | DIGITO | '_')*;


//  FRAGMENTOS

fragment LETRA  : [a-zA-ZáéíóúñÁÉÍÓÚÑ];
fragment DIGITO : [0-9];


//  WHITESPACE, SALTOS DE LÍNEA Y COMENTARIOS

NL : ('\r'? '\n')+;
WS : [ \t]+ -> skip;

COMENTARIO_LINEA  : '//' ~[\r\n]* -> skip;
COMENTARIO_BLOQUE : '/-' .*? '-/' -> skip;
COMENTARIO_DOC    : '///' ~[\r\n]* -> skip;
