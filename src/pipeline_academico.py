import time
import os
from src.limpiador_datos import LimpiadorDatos
from src.particionador import ParticionadorEstudiantes
from src.analizador_ncd import AnalizadorNCD
from src.gestor_topologias import GestorTopologias
from src.comparador_topologias import ComparadorTopologias
from src.analizador_bayesiano import AnalizadorBayesiano
from src.generador_reportes import GeneradorReportes

class PipelineAcademico:
    """
    Encapsula y conecta las etapas individuales del experimento en español
    con almacenamiento jerárquico por bloques (50%, 25%, 12.5%).
    """
    def __init__(self, ruta_datos, nivel_gzip=9):
        self.ruta_datos = ruta_datos
        self.dir_base = "results"
        
        # Instanciar las etapas en español como objetos
        self.limpiador = LimpiadorDatos(ruta_datos)
        self.particionador = ParticionadorEstudiantes(dir_base=self.dir_base)
        self.analizador = AnalizadorNCD(dir_base=self.dir_base, nivel_gzip=nivel_gzip)
        self.topologia = GestorTopologias(dir_base=self.dir_base)
        self.comparador = ComparadorTopologias(dir_base=self.dir_base)
        self.bayesiano = AnalizadorBayesiano(dir_base=self.dir_base)
        self.reportador = GeneradorReportes()

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
        print("\n" + "=" * 60)
        print("   🎓 PIPELINE POO NCD/Gzip - ANÁLISIS ACADÉMICO")
        print("   Particionamiento Jerárquico por Bloques (50%, 25%, 12.5%)")
        print("=" * 60)

        inicio_total = time.time()

        # Paso 1: Limpieza
        df, reporte_limpieza = self._paso(1, "LIMPIEZA DE DATOS", self.limpiador.ejecutar)

        # Paso 2: Particiones jerárquicas (Sub-bloques)
        particiones = self._paso(2, "PARTICIONAMIENTO POR BLOQUES", self.particionador.ejecutar, df)

        # Paso 3: NCD/Gzip leyendo CSVs de disco
        matrices = self._paso(3, "CÁLCULO NCD/GZIP ENTRE VARIABLES", self.analizador.ejecutar, particiones)

        # Paso 4: Topologías (MST, heatmap, dendrograma por nivel)
        topologias = self._paso(4, "CONSTRUCCIÓN DE TOPOLOGÍAS (MST)", self.topologia.ejecutar, matrices)

        # Dendrogramas comparativos Best vs Worst extremos
        print("\n   🌳 Generando dendrogramas comparativos por nivel...")
        self.topologia.graficar_dendrograma_comparativo(matrices)

        # Paso 5: Comparación Best vs Worst (Diferencia D)
        comparaciones = self._paso(5, "COMPARACIÓN BEST vs WORST", self.comparador.ejecutar, topologias)

        # Paso 6: Árboles Bayesianos (MST Dirigido de Probabilidad Conjunta)
        arboles_bayesianos = self._paso(6, "CONSTRUCCIÓN DE ÁRBOLES BAYESIANOS (PROB. CONJUNTA)", self.bayesiano.ejecutar_paso, df, particiones)

        # Paso 7: Informe
        ruta_informe = self._paso(7, "GENERACIÓN DE INFORME", self.reportador.ejecutar, 
                                  reporte_limpieza, particiones, matrices, topologias, comparaciones)

        fin_total = time.time()

        print("\n" + "=" * 60)
        print(f"   ✅ PIPELINE POO COMPLETADO en {fin_total - inicio_total:.2f}s")
        print("=" * 60)
        print(f"   Informe final disponible en: {ruta_informe}\n")
