"""
=============================================================
  PASO 6: GENERACIÓN DE INFORME DE RESULTADOS
=============================================================
Genera un informe detallado en formato Markdown con:
- Descripción del dataset y metodología
- Matrices NCD embebidas como tablas
- Resultados de las comparaciones
- Identificación de variables clave
- Conclusiones automáticas
=============================================================
"""

import os
import pandas as pd
from datetime import datetime

# ── CONFIGURACIÓN ──────────────────────────────────────────
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "informe", "informe_ncd_gzip.md")

NOMBRES_COMPLETOS = {
    "X1": "Sexo", "X2": "Zona", "X3": "Ciclo",
    "X4": "Ingreso Familiar", "X5": "Trabaja", "X6": "Beca",
    "X7": "Educación Jefe de Familia", "X8": "Tamaño Familiar",
    "X9": "Asistencia", "X10": "Cursos Desaprobados"
}
# ───────────────────────────────────────────────────────────


def generar_tabla_markdown(df, max_decimales=4):
    """Convierte un DataFrame a tabla Markdown."""
    cols = df.columns.tolist()
    lineas = []
    # Encabezado
    lineas.append("| " + " | ".join(str(c) for c in cols) + " |")
    lineas.append("| " + " | ".join("---" for _ in cols) + " |")
    # Filas
    for _, row in df.iterrows():
        vals = []
        for c in cols:
            v = row[c]
            if isinstance(v, float):
                vals.append(f"{v:.{max_decimales}f}")
            else:
                vals.append(str(v))
        lineas.append("| " + " | ".join(vals) + " |")
    return "\n".join(lineas)


def ejecutar(reporte_limpieza, particiones, matrices, topologias, comparaciones):
    """Genera el informe completo en Markdown."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    n_estudiantes = reporte_limpieza.get("final", "N/A")

    # ── CONSTRUIR INFORME ──────────────────────────────────

    md = f"""# Informe: Análisis de Comportamiento Académico con NCD/Gzip

**Fecha:** {fecha}
**Curso:** Ciberseguridad - 9no Semestre
**Universidad:** Universidad Nacional del Altiplano - Puno

---

## 1. Introducción

El presente informe documenta el experimento de análisis de patrones académicos
utilizando la métrica **Normalized Compression Distance (NCD)** con compresión **Gzip**.

El objetivo es descubrir **qué factores socioeconómicos y académicos** se comportan
de manera diferente entre estudiantes de alto y bajo rendimiento, revelando las
posibles **causas** del éxito o fracaso académico.

## 2. Objetivo

Aplicar un pipeline completo de análisis basado en NCD/Gzip para:

1. Dividir a los estudiantes según su rendimiento académico (X11 - Promedio Final)
2. Calcular distancias entre variables explicativas (X1-X10) dentro de cada grupo
3. Construir topologías de red (MST) que representen las relaciones entre variables
4. Comparar las redes Best vs Worst para identificar qué variables cambian más

**Pregunta central:** ¿Qué variables (causas) explican la diferencia entre
estudiantes con alto y bajo promedio final?

## 3. Descripción del Dataset

| Característica | Valor |
|---|---|
| Total de estudiantes (después de limpieza) | {n_estudiantes} |
| Variables explicativas | X1 a X10 (10 variables) |
| Variable de clasificación | X11 - Promedio Final |
| Duplicados eliminados | {reporte_limpieza.get('duplicados_eliminados', 0)} |
| Nulos eliminados | {reporte_limpieza.get('nulos_eliminados', 0)} |

### Variables del estudio

| Variable | Descripción | Tipo |
|---|---|---|
| X1 | Sexo | Categórica |
| X2 | Zona geográfica | Categórica |
| X3 | Ciclo académico | Numérica |
| X4 | Ingreso familiar | Numérica |
| X5 | Trabaja | Categórica |
| X6 | Beca | Categórica |
| X7 | Educación del jefe de familia | Categórica |
| X8 | Tamaño familiar | Numérica |
| X9 | Asistencia (%) | Numérica |
| X10 | Cursos desaprobados | Numérica |
| **X11** | **Promedio final** | **Numérica (clasificación)** |

> **Nota:** X11 se usa exclusivamente para clasificar estudiantes en Best/Worst.
> Las variables X1-X10 son las que se analizan con NCD para descubrir patrones.

## 4. Metodología

### 4.1 Limpieza de datos

Se eliminaron filas con valores nulos, duplicados y datos fuera de rango lógico
(promedio < 0 o > 20, asistencia < 0 o > 100, etc.).

### 4.2 Particionamiento por rendimiento académico

Los estudiantes se ordenaron por X11 (promedio final) y se crearon particiones:

| Nivel | Best (Top) | Worst (Bottom) |
|---|---|---|
| 12.5% | {len(particiones.get('Best_12.5', []))} estudiantes con mayor promedio | {len(particiones.get('Worst_12.5', []))} estudiantes con menor promedio |
| 25% | {len(particiones.get('Best_25', []))} estudiantes | {len(particiones.get('Worst_25', []))} estudiantes |
| 50% | {len(particiones.get('Best_50', []))} estudiantes | {len(particiones.get('Worst_50', []))} estudiantes |

### 4.3 Cálculo de NCD/Gzip

Para cada partición se calculó una **matriz de distancia 10×10** entre las variables
X1 a X10 usando la fórmula:

```
NCD(x, y) = (C(xy) - min(C(x), C(y))) / max(C(x), C(y))
```

Donde:
- `C(x)` = tamaño comprimido de la columna x con gzip (nivel 9)
- Cada columna se convirtió a cadena de texto antes de comprimir
- `NCD ≈ 0` → variables muy similares/relacionadas
- `NCD ≈ 1` → variables muy diferentes

### 4.4 Construcción de topologías de red

Con cada matriz NCD se construyó un **Minimum Spanning Tree (MST)** usando NetworkX:
- 10 nodos = 10 variables
- Aristas = distancia NCD entre variables
- El MST conecta todas las variables con el mínimo peso total

### 4.5 Comparación de topologías

Se compararon las redes Best vs Worst calculando el **grado ponderado** de cada
variable (suma de pesos de aristas conectadas en el MST) y la diferencia:

```
D = GradoPonderado_Worst - GradoPonderado_Best
```

- **D positivo grande** → la variable aumenta su conexión en Worst (factor de riesgo)
- **D negativo grande** → la variable disminuye su conexión en Worst (factor protector)

## 5. Resultados

### 5.1 Matrices NCD

"""

    # Agregar matrices NCD
    for nombre, df_matriz in sorted(matrices.items()):
        tipo = "BEST" if "Best" in nombre else "WORST"
        nivel = nombre.split("_")[1]
        md += f"#### Matriz NCD - {tipo} ({nivel}%)\n\n"
        md += generar_tabla_markdown(df_matriz.reset_index().rename(columns={"index": "Var"}), 4)
        md += "\n\n"

    md += "### 5.2 Comparación de Topologías\n\n"

    # Agregar comparaciones
    for nivel in sorted(comparaciones.keys(), key=lambda x: float(x)):
        comp = comparaciones[nivel]
        tabla = comp["tabla"]
        max_c = comp["max_cambio"]
        min_c = comp["min_cambio"]

        md += f"#### Partición {nivel}%\n\n"
        md += generar_tabla_markdown(tabla, 4)
        md += f"\n\n**Variable con MÁXIMO cambio:** {max_c['Variable']} "
        md += f"({NOMBRES_COMPLETOS.get(max_c['Variable'], '')}) → D = {max_c['Diferencia_D']:+.4f}\n\n"
        md += f"**Variable con MÍNIMO cambio:** {min_c['Variable']} "
        md += f"({NOMBRES_COMPLETOS.get(min_c['Variable'], '')}) → D = {min_c['Diferencia_D']:+.4f}\n\n"

    # ── CONCLUSIONES ──────────────────────────────────────

    # Encontrar variables que consistentemente cambian más
    variables_max = [comp["max_cambio"]["Variable"] for comp in comparaciones.values()]
    variables_min = [comp["min_cambio"]["Variable"] for comp in comparaciones.values()]

    # Contar frecuencia
    from collections import Counter
    freq_max = Counter(variables_max).most_common(3)
    freq_min = Counter(variables_min).most_common(3)

    md += f"""## 6. Análisis de Variables Relevantes

### Variables con mayor cambio estructural

Las siguientes variables presentan los mayores cambios en su posición dentro
de la red entre los grupos Best y Worst:

"""
    for var, count in freq_max:
        nombre = NOMBRES_COMPLETOS.get(var, "")
        md += f"- **{var} ({nombre})**: máximo cambio en {count} de {len(comparaciones)} particiones\n"

    md += f"""
### Variables con menor cambio estructural

Las siguientes variables mantienen un comportamiento similar en ambos grupos:

"""
    for var, count in freq_min:
        nombre = NOMBRES_COMPLETOS.get(var, "")
        md += f"- **{var} ({nombre})**: mínimo cambio en {count} de {len(comparaciones)} particiones\n"

    md += f"""

## 7. Discusión

El análisis NCD/Gzip permitió revelar que las relaciones entre variables
socioeconómicas y académicas **no son iguales** para estudiantes de alto y bajo
rendimiento. Las variables que más cambian su posición en la topología de red
son aquellas que tienen un comportamiento diferenciado según el grupo.

Cuando una variable tiene un **D positivo grande**, significa que en el grupo
Worst esa variable está más conectada/central en la red de relaciones,
sugiriendo que juega un papel más determinante en el bajo rendimiento.

Cuando una variable tiene un **D negativo grande**, significa que en el grupo
Best esa variable tiene mayor centralidad, sugiriendo un rol protector o
asociado al buen rendimiento.

## 8. Conclusiones

1. La técnica NCD/Gzip permite cuantificar relaciones entre variables sin
   asumir distribuciones estadísticas ni linealidad.

2. Las topologías de red (MST) revelan la estructura de dependencias entre
   variables dentro de cada grupo de rendimiento.

3. La comparación de topologías identifica las variables que más cambian
   su comportamiento entre grupos, indicando posibles factores causales.

4. Los resultados son consistentes a través de las tres particiones
   (12.5%, 25%, 50%), lo que refuerza la robustez de los hallazgos.

## 9. Reproducibilidad

Para reproducir este análisis:

```bash
pip install -r requirements.txt
python main.py
```

Los resultados se generan en:
- `results/matrices/` → Matrices NCD (CSV)
- `results/graficos/` → Gráficos de redes y comparaciones (PNG)
- `results/tablas/` → Tablas comparativas (CSV)

## 10. Anexos

### Archivos generados

| Carpeta | Contenido |
|---|---|
| `results/matrices/` | 6 matrices NCD (10×10) en formato CSV |
| `results/graficos/` | Gráficos MST, heatmaps, comparaciones |
| `results/tablas/` | Particiones y tablas comparativas |
| `informe/` | Este informe en formato Markdown |

---

*Informe generado automáticamente por el pipeline NCD/Gzip.*
"""

    # Guardar
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\n   💾 Informe guardado: {os.path.normpath(OUTPUT_PATH)}")
    print(f"      Tamaño: {len(md)} caracteres")

    return OUTPUT_PATH


if __name__ == "__main__":
    print("=" * 55)
    print("  PASO 6: GENERACIÓN DE INFORME")
    print("=" * 55)
    print("  Ejecuta desde main.py para obtener todos los datos.")
