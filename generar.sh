#!/usr/bin/env bash
# generar.sh — Regenera el lexer, parser y visitor de RISCO con ANTLR 4.
# Uso: bash generar.sh   (o: chmod +x generar.sh && ./generar.sh)

set -euo pipefail

# ── 1. Activar el entorno virtual si existe ──────────────────────────────────
# 'source' solo funciona en bash/zsh; este script ya exige bash por el shebang.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_ACTIVATE=""
for candidate in \
        "$SCRIPT_DIR/venv/bin/activate" \
        "$SCRIPT_DIR/../venv/bin/activate" \
        "venv/bin/activate"; do
    if [[ -f "$candidate" ]]; then
        VENV_ACTIVATE="$candidate"
        break
    fi
done

if [[ -n "$VENV_ACTIVATE" ]]; then
    # shellcheck source=/dev/null
    source "$VENV_ACTIVATE"
    echo "✅ Entorno virtual activado: $VENV_ACTIVATE"
else
    echo "⚠️  No se encontró venv — usando Python del sistema"
fi

echo ""
echo "════════════════════════════════════════"
echo "  Generando lexer, parser y visitor"
echo "════════════════════════════════════════"

# ── 2. Localizar o descargar el JAR de ANTLR ────────────────────────────────
ANTLR_VERSION="4.13.2"
ANTLR_JAR="antlr-${ANTLR_VERSION}-complete.jar"

# Buscar el JAR en varias ubicaciones habituales
JAR_PATH=""
for candidate in \
        "/usr/local/lib/${ANTLR_JAR}" \
        "/usr/local/share/${ANTLR_JAR}" \
        "$SCRIPT_DIR/${ANTLR_JAR}" \
        "$HOME/${ANTLR_JAR}"; do
    if [[ -f "$candidate" ]]; then
        JAR_PATH="$candidate"
        break
    fi
done

if [[ -z "$JAR_PATH" ]]; then
    # Intentar descargarlo en /usr/local/lib (puede necesitar sudo)
    DEST="/usr/local/lib/${ANTLR_JAR}"
    echo "📥 Descargando ANTLR ${ANTLR_VERSION}..."
    if curl -fsSL -o "$DEST" \
            "https://www.antlr.org/download/${ANTLR_JAR}" 2>/dev/null; then
        JAR_PATH="$DEST"
    elif sudo curl -fsSL -o "$DEST" \
            "https://www.antlr.org/download/${ANTLR_JAR}"; then
        JAR_PATH="$DEST"
    else
        echo "❌ No se pudo descargar el JAR de ANTLR."
        echo "   Descárgalo manualmente desde https://www.antlr.org/download/${ANTLR_JAR}"
        echo "   y colócalo en /usr/local/lib/ o en el directorio raíz del proyecto."
        exit 1
    fi
fi
echo "✅ JAR de ANTLR: $JAR_PATH"

# ── 3. Verificar que java está disponible ────────────────────────────────────
if ! command -v java &>/dev/null; then
    echo "❌ 'java' no encontrado. Instala el JDK:"
    echo "   sudo apt install default-jdk   (Debian/Ubuntu/Kali)"
    exit 1
fi
echo "✅ Java: $(java -version 2>&1 | head -1)"

# ── 4. Verificar que existe la gramática ─────────────────────────────────────
GRAMMAR="gramaticas/RISCO.g4"
if [[ ! -f "$GRAMMAR" ]]; then
    echo "❌ No se encuentra la gramática en '$GRAMMAR'."
    echo "   Asegúrate de ejecutar este script desde la raíz del proyecto."
    exit 1
fi
echo "✅ Gramática: $GRAMMAR"

# ── 5. Limpiar archivos anteriores ───────────────────────────────────────────
echo ""
echo "🧹 Limpiando archivos anteriores..."
rm -f gramaticas/RISCO*.py
rm -rf generado

# ── 6. Generar con ANTLR ─────────────────────────────────────────────────────
echo "⚙️  Ejecutando ANTLR..."
java -jar "$JAR_PATH" \
    -Dlanguage=Python3 \
    -visitor \
    -no-listener \
    -o generado \
    "$GRAMMAR"

ANTLR_EXIT=$?
if [[ $ANTLR_EXIT -ne 0 ]]; then
    echo "❌ ANTLR terminó con error (código $ANTLR_EXIT)."
    exit 1
fi

# ── 7. Mover archivos generados al directorio gramaticas/ ────────────────────
echo "📂 Copiando archivos generados..."

# ANTLR genera los archivos en generado/<ruta_relativa_a_la_gramática>/
# La estructura exacta depende de la ruta usada, buscamos los .py generados
GENERATED_PY=$(find generado -name "RISCO*.py" 2>/dev/null)
if [[ -z "$GENERATED_PY" ]]; then
    echo "❌ ANTLR no generó archivos .py. Revisa la gramática."
    exit 1
fi

for f in $GENERATED_PY; do
    cp "$f" gramaticas/
    echo "   → $(basename "$f")"
done

# Garantizar que gramaticas/ es un paquete Python
touch gramaticas/__init__.py

# ── 8. Limpiar directorio temporal ───────────────────────────────────────────
rm -rf generado

# ── 9. Resumen ───────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════"
echo "✅ Generación completada"
echo "════════════════════════════════════════"
ls -la gramaticas/RISCO*.py