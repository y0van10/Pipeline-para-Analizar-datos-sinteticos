import time
import os
from src.data_cleaner import DataCleaner
from src.partitioner import StudentPartitioner
from src.ncd_analyzer import NCDAnalyzer
from src.topology_manager import TopologyManager
from src.topology_comparator import TopologyComparator
from src.report_generator import ReportGenerator

class AcademicPipeline:
    """
    Clase Orquestadora (Controlador) que representa el Pipeline de Análisis Académico completo.
    Encapsula y conecta las etapas individuales del experimento.
    """
    def __init__(self, dataset_path, partition_levels=[0.125, 0.25, 0.50], gzip_level=9):
        self.dataset_path = dataset_path
        
        # Instanciar las etapas como objetos
        self.cleaner = DataCleaner(dataset_path)
        self.partitioner = StudentPartitioner(levels=partition_levels)
        self.analyzer = NCDAnalyzer(gzip_level=gzip_level)
        self.topology = TopologyManager()
        self.comparator = TopologyComparator()
        self.generator = ReportGenerator()

    def _separador(self, titulo):
        print("\n" + "█" * 60)
        print(f"  {titulo}")
        print("█" * 60)

    def _paso(self, numero, titulo, metodo, *args):
        self._separador(f"PASO {numero}/6: {titulo}")
        inicio = time.time()
        resultado = metodo(*args)
        fin = time.time()
        print(f"\n   ⏱️  Tiempo del paso {numero}: {fin - inicio:.2f}s")
        return resultado

    def run(self):
        print("\n" + "=" * 60)
        print("   🎓 PIPELINE POO NCD/Gzip - ANÁLISIS ACADÉMICO")
        print("   Cuantificación de Patrones en Orientación a Objetos")
        print("=" * 60)

        inicio_total = time.time()

        # Paso 1: Limpieza
        df, reporte_limpieza = self._paso(1, "LIMPIEZA DE DATOS", self.cleaner.ejecutar)

        # Paso 2: Particiones
        particiones = self._paso(2, "PARTICIONAMIENTO POR RENDIMIENTO", self.partitioner.ejecutar, df)

        # Paso 3: NCD/Gzip
        matrices = self._paso(3, "CÁLCULO NCD/GZIP ENTRE VARIABLES", self.analyzer.ejecutar, particiones)

        # Paso 4: Topologías (MST, heatmap, dendrograma)
        topologias = self._paso(4, "CONSTRUCCIÓN DE TOPOLOGÍAS (MST)", self.topology.ejecutar, matrices)

        # Dendrogramas comparativos Best vs Worst
        print("\n   🌳 Generando dendrogramas comparativos...")
        self.topology.graficar_dendrograma_comparativo(matrices)

        # Paso 5: Comparación Best vs Worst (Diferencia D)
        comparaciones = self._paso(5, "COMPARACIÓN BEST vs WORST", self.comparator.ejecutar, topologias)

        # Paso 6: Informe
        path_informe = self._paso(6, "GENERACIÓN DE INFORME", self.generator.ejecutar, 
                                  reporte_limpieza, particiones, matrices, topologias, comparaciones)

        fin_total = time.time()

        print("\n" + "=" * 60)
        print(f"   ✅ PIPELINE POO COMPLETADO en {fin_total - inicio_total:.2f}s")
        print("=" * 60)
        print(f"   Informe final disponible en: {path_informe}\n")
