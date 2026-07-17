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
    Clase Orquestadora (Controlador) que representa el Pipeline de Análisis Académico completo.
    Encapsula y conecta las etapas individuales del experimento en español (7 pasos, incluyendo Árboles Bayesianos).
    """
    def __init__(self, ruta_datos, niveles_particion=[0.125, 0.25, 0.50], nivel_gzip=9):
        self.ruta_datos = ruta_datos
        
        # Instanciar las etapas en español como objetos
        self.limpiador = LimpiadorDatos(ruta_datos)
        self.particionador = ParticionadorEstudiantes(niveles=niveles_particion)
        self.analizador = AnalizadorNCD(nivel_gzip=nivel_gzip)
        self.topologia = GestorTopologias()
        self.comparador = ComparadorTopologias()
        self.bayesiano = AnalizadorBayesiano()
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
        print("   Cuantificación de Patrones en Orientación a Objetos (ES)")
        print("=" * 60)

        inicio_total = time.time()

        # Paso 1: Limpieza
        df, reporte_limpieza = self._paso(1, "LIMPIEZA DE DATOS", self.limpiador.ejecutar)

        # Paso 2: Particiones
        particiones = self._paso(2, "PARTICIONAMIENTO POR RENDIMIENTO", self.particionador.ejecutar, df)

        # Paso 3: NCD/Gzip
        matrices = self._paso(3, "CÁLCULO NCD/GZIP ENTRE VARIABLES", self.analizador.ejecutar, particiones)

        # Paso 4: Topologías (MST, heatmap, dendrograma)
        topologias = self._paso(4, "CONSTRUCCIÓN DE TOPOLOGÍAS (MST)", self.topologia.ejecutar, matrices)

        # Dendrogramas comparativos Best vs Worst
        print("\n   🌳 Generando dendrogramas comparativos...")
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
