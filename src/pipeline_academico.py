import time
import os
import pandas as pd
from src.limpiador_datos import LimpiadorDatos
from src.particionador import ParticionadorEstudiantes
from src.analizador_ncd import AnalizadorNCD
from src.gestor_topologias import GestorTopologias
from src.comparador_topologias import ComparadorTopologias
from src.analizador_bayesiano import AnalizadorBayesiano
from src.generador_reportes import GeneradorReportes

class PipelineAcademico:
    """
    Orquestador del pipeline NCD/Gzip - Análisis Académico.
    Completamente dinámico: funciona con cualquier CSV y cualquier
    número de columnas. Solo requiere indicar la columna objetivo
    (col_objetivo) que se usará para ordenar y particionar.
    Si no se indica, se detecta automáticamente.
    """
    def __init__(self, ruta_datos, nivel_gzip=9, col_objetivo=None):
        self.ruta_datos   = ruta_datos
        self.dir_base     = "results"
        self.col_objetivo = col_objetivo  # None → auto-detección en LimpiadorDatos

        # Instanciar las etapas (col_objetivo se propaga a todas)
        self.limpiador   = LimpiadorDatos(ruta_datos, col_objetivo=col_objetivo)
        self.particionador = ParticionadorEstudiantes(dir_base=self.dir_base, col_objetivo=col_objetivo)
        self.analizador  = AnalizadorNCD(dir_base=self.dir_base, nivel_gzip=nivel_gzip, col_objetivo=col_objetivo)
        self.topologia   = GestorTopologias(dir_base=self.dir_base)
        self.comparador  = ComparadorTopologias(dir_base=self.dir_base)
        self.bayesiano   = AnalizadorBayesiano(dir_base=self.dir_base, col_objetivo=col_objetivo)
        self.reportador  = GeneradorReportes()

    def _separador(self, titulo):
        print("\n" + "█" * 60)
        print(f"  {titulo}")
        print("█" * 60)

    def _paso(self, numero, titulo, metodo, *args):
        self._separador(f"PASO {numero}/7: {titulo}")
        inicio = time.time()
        resultado = metodo(*args)
        fin = time.time()
        print(f"\n   ⏱️  Tiempo del paso {numero}: {fin - inicio:.2f}s")
        return resultado

    def ejecutar(self):
        """
        Ejecuta de manera secuencial los 7 pasos del pipeline académico:
        1. Limpieza de datos (remoción de duplicados, imputación y validación del objetivo).
        2. Particionamiento jerárquico contiguo (Best/Worst para 50%, 25% y 12.5%).
        3. Cálculo de NCD (Normalized Compression Distance) usando Gzip sobre todas las variables.
        4. Construcción de topologías complejas y MST utilizando NetworkX.
        5. Comparación estructural de grados de centralidad (Best vs Worst por variable).
        6. Inferencia probabilística causal y graficado de Redes y Árboles Bayesianos.
        7. Consolidación de resultados y generación automática del Reporte Técnico en Markdown.
        """
        print("\n" + "=" * 60)
        print("   🎓 PIPELINE POO NCD/Gzip - ANÁLISIS ACADÉMICO")
        print("   Particionamiento Jerárquico (50%, 25%, 12.5%)")
        print("=" * 60)

        inicio_total = time.time()

        # ── Paso 1: Limpieza (Carga el dataset y autodetecta/valida la columna objetivo si no fue indicada) ──
        df, reporte_limpieza = self._paso(1, "LIMPIEZA DE DATOS", self.limpiador.ejecutar)

        # Propagar el col_objetivo detectado dinámicamente a todos los demás módulos de análisis
        col_obj = self.limpiador.col_objetivo
        self.particionador.col_objetivo = col_obj
        self.analizador.col_objetivo    = col_obj
        self.bayesiano.col_objetivo     = col_obj
        print(f"   🎯 Variable objetivo: '{col_obj}'")

        # ── Paso 2: Partición jerárquica contigua (Best y Worst en base a la columna objetivo) ──
        particiones = self._paso(2, "PARTICIONAMIENTO POR BLOQUES",
                                 self.particionador.ejecutar, df)

        # ── Paso 3: Análisis de Teoría de la Información (NCD/Gzip para medir disimilitud algorítmica) ──
        matrices = self._paso(3, "CÁLCULO NCD/GZIP ENTRE VARIABLES",
                              self.analizador.ejecutar, particiones)

        # ── Paso 4: Análisis de Redes Complejas (Grafo Completo, Árbol MST, Heatmap y Dendrogramas) ──
        topologias = self._paso(4, "CONSTRUCCIÓN DE TOPOLOGÍAS (MST)",
                                self.topologia.ejecutar, matrices)

        print("\n   🌳 Generando dendrogramas comparativos por nivel...")
        self.topologia.graficar_dendrograma_comparativo(matrices)

        # ── Paso 5: Comparación de Centralidad Estructural (Diferencia de grado ponderado D = Worst - Best) ──
        comparaciones = self._paso(5, "COMPARACIÓN BEST vs WORST",
                                   self.comparador.ejecutar, topologias)

        # ── Paso 6: Redes Bayesianas y Árboles de Probabilidad Conjunta Causal Jerárquica ──
        arboles = self._paso(6, "ÁRBOLES BAYESIANOS (PROB. CONJUNTA)",
                             self.bayesiano.ejecutar_paso, df, particiones)

        # ── Paso 7: Informe ──
        ruta_informe = self._paso(7, "GENERACIÓN DE INFORME",
                                  self.reportador.ejecutar,
                                  reporte_limpieza, particiones, matrices,
                                  topologias, comparaciones)

        fin_total = time.time()
        print("\n" + "=" * 60)
        print(f"   ✅ PIPELINE COMPLETADO en {fin_total - inicio_total:.2f}s")
        print(f"   🎯 Variable objetivo usada: '{col_obj}'")
        print("=" * 60)
        print(f"   Informe final: {ruta_informe}\n")
