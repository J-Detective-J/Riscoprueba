# RISCO V2 – Lenguaje DSL para Cálculo, Archivos y Visualización

## 1. Descripción

RISCO es un lenguaje específico de dominio (DSL) diseñado para soportar operaciones matemáticas, manipulación de datos, persistencia en archivos y visualización de resultados mediante gráficos.

El sistema está construido utilizando ANTLR4 y un intérprete en Python que permite ejecutar programas escritos en el lenguaje `.rc`.

En esta versión (V2), el lenguaje incluye:

- Librería matemática
- Manejo de memoria
- Manejo de archivos
- Visualización de datos (SVG)
- Soporte de funciones y recursión
- Sistema de pruebas automatizadas

---

## 2. Estructura del proyecto

RiscoV2/
├── src/
├── Risco/
│   ├── mat.rc
│   ├── file.rc
│   └── visual.rc
├── ejemplos/
├── test/
├── gramaticas/
├── requisitos.txt
└── README.md

---

## 3. Características principales

### Librería matemática
Operaciones matriciales, funciones matemáticas y generación de datos.

### Manejo de archivos
Lectura, escritura, append, CSV y verificación.

### Visualización
Gráficos SVG:
- Barras
- Líneas
- Scatter
- Histograma

Con:
- Ejes
- Etiquetas
- Escalas
- Grid

---

## 4. Ejecución

python3 src/risco.py ejemplos/prueba_visual.rc

---

## 5. Pruebas

pytest test/test_risco.py

✔ 186 pruebas pasando

---

## 6. Diseño

Código RISCO → ANTLR → Árbol → Evaluador → Resultado

---

## 7. Decisiones

- SVG sin librerías externas
- Modular (mat, file, visual)
- Testing con pytest

---
