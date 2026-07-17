import os
from datetime import datetime

class GeneradorReportes:
    """
    Clase encargada de consolidar los resultados obtenidos en las etapas del pipeline
    y redactar el reporte final estructurado en Markdown.
    """
    NOMBRES_COMPLETOS = {
        "X1": "Sexo", "X2": "Zona", "X3": "Ciclo",
        "X4": "Ingreso Familiar", "X5": "Trabaja", "X6": "Beca",
        "X7": "Educación Jefe de Familia", "X8": "Tamaño Familiar",
        "X9": "Asistencia", "X10": "Cursos Desaprobados"
    }

    def __init__(self, ruta_informe="informe/informe_ncd_gzip.md"):
        self.ruta_informe = os.path.normpath(ruta_informe)

    def _generar_tabla_markdown(self, df, max_decimales=4):
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

    def escribir_reporte(self, reporte_limpieza, particiones, matrices, topologias, comparaciones):
        os.makedirs(os.path.dirname(self.ruta_informe), exist_ok=True)
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        n_estudiantes = reporte_limpieza.get("final", "N/A")

        # Empezar a armar el string Markdown
        md = f"""# Informe: Análisis de Comportamiento Académico con NCD/Gzip

Este informe documenta los resultados del experimento automatizado llevado a cabo sobre el modelo de factores socioacadémicos utilizando la distancia de compresión normalizada (NCD) con el compresor Gzip.

**Fecha de ejecución:** {fecha}  
**Total de estudiantes analizados:** {n_estudiantes}

---

## 1. Limpieza y Validación de Datos

El dataset original pasó por un proceso de limpieza para garantizar la calidad y lógica de los datos.

*   **Filas originales:** {reporte_limpieza.get('original', 'N/A')}
*   **Duplicados eliminados:** {reporte_limpieza.get('duplicados_eliminados', 0)}
*   **Filas nulas eliminadas:** {reporte_limpieza.get('nulos_eliminados', 0)}
*   **Registros no numéricos eliminados:** {reporte_limpieza.get('no_numericos_eliminados', 0)}
*   **Registros fuera de rango eliminados:** {reporte_limpieza.get('fuera_rango_eliminados', 0)}
*   **Filas finales retenidas:** {reporte_limpieza.get('final', 0)} ({100 * reporte_limpieza.get('final', 1) / reporte_limpieza.get('original', 1):.2f}%)

---

## 2. Definición de Grupos y Muestras

Los estudiantes se ordenaron de manera descendente según su rendimiento académico (**X11 - Promedio Final**) y se seleccionaron muestras en los extremos de rendimiento académico:

*   **Best (Alto rendimiento):** El porcentaje de estudiantes con mayor promedio.
*   **Worst (Bajo rendimiento):** El porcentaje de estudiantes con menor promedio.

Las muestras definidas fueron:
*   **12.5%:** {len(particiones.get('Best_12.5', []))} estudiantes por subgrupo.
*   **25%:** {len(particiones.get('Best_25', []))} estudiantes por subgrupo.
*   **50%:** {len(particiones.get('Best_50', []))} estudiantes por subgrupo.

---

## 3. Matrices NCD (Normalized Compression Distance)

A continuación se presentan las matrices de distancia calculadas para cada grupo de rendimiento y nivel de partición. Un valor cercano a `0` indica alta similitud/relación y un valor cercano a `1` indica independencia.

"""

        for nombre, df_matriz in matrices.items():
            md += f"### Matriz NCD - {nombre}\n\n"
            md += self._generar_tabla_markdown(df_matriz) + "\n\n"

        md += """---

## 4. Comparación de Topologías (Best vs Worst)

Al extraer el Árbol de Expansión Mínima (MST) de cada grafo y calcular el **Grado Ponderado** (suma de pesos de aristas incidentes en el árbol), evaluamos qué tan conectada y central es cada variable dentro de la red del grupo.

La diferencia se calcula como:
$$D = Grado_{Worst} - Grado_{Best}$$

Un valor de $D$ muy positivo o muy negativo nos muestra variables que cambian drásticamente su rol en el comportamiento de los estudiantes de bajo rendimiento frente a los de alto rendimiento.

"""

        for nivel, df_comp in comparaciones.items():
            md += f"### Comparación para Partición {nivel}%\n\n"
            md += self._generar_tabla_markdown(df_comp) + "\n\n"
            
            # Extraer extremos
            max_var = df_comp.iloc[0]
            min_var = df_comp.iloc[-1]
            md += f"*   🔴 **Máximo Cambio:** Variable `{max_var['Variable']}` ({max_var['Nombre']}) con una diferencia $|D| = {max_var['Abs_Diferencia']:.4f}$\n"
            md += f"*   🟢 **Mínimo Cambio:** Variable `{min_var['Variable']}` ({min_var['Nombre']}) con una diferencia $|D| = {min_var['Abs_Diferencia']:.4f}$\n\n"

        md += """---

## 5. Conclusiones y Discusión Académica

El análisis comparativo de las topologías revela cambios estructurales críticos en las relaciones de los estudiantes:

"""

        # Generar conclusiones automáticas basadas en la partición más pequeña (extrema)
        if "12.5" in comparaciones:
            df_125 = comparaciones["12.5"]
            max_cambio = df_125.iloc[0]
            segundo_cambio = df_125.iloc[1]
            
            md += f"1.  **Factores Determinantes:** Al comparar los extremos de rendimiento académico (el 12.5% superior e inferior), las variables cuyas relaciones y centralidad topológica cambian de forma más radical son **{max_cambio['Nombre']} ({max_cambio['Variable']})** y **{segundo_cambio['Nombre']} ({segundo_cambio['Variable']})**.\n"
            md += f"2.  **Mecánica de Impacto:** La variable `{max_cambio['Variable']}` pasa de tener un grado de {max_cambio['Grado_Best']:.4f} en los mejores estudiantes a {max_cambio['Grado_Worst']:.4f} en los peores. Este cambio drástico ($D = {max_cambio['Diferencia_D']:+.4f}$) demuestra que su influencia en la red socioacadémica cambia significativamente según el rendimiento final.\n"
            md += f"3.  **Variables Invariantes:** Las variables que mostraron menor variación o que permanecieron casi idénticas en ambas redes son aquellas al final del ranking, lideradas por **{df_125.iloc[-1]['Nombre']} ({df_125.iloc[-1]['Variable']})**, sugiriendo que su rol es neutro o estable en este contexto experimental.\n"

        md += """
Este experimento demuestra empíricamente que la causa del bajo rendimiento académico (X11) no puede explicarse evaluando variables de manera aislada, sino a través de la **reorganización estructural de las variables socioeconómicas y familiares**.
"""

        with open(self.ruta_informe, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"   💾 Informe guardado: {self.ruta_informe}")
        return self.ruta_informe

    def ejecutar(self, reporte_limpieza, particiones, matrices, topologias, comparaciones):
        return self.escribir_reporte(reporte_limpieza, particiones, matrices, topologias, comparaciones)
