import os
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from itertools import combinations

class AnalizadorBayesiano:
    """
    Clase encargada de construir Árboles Bayesianos (MSTs dirigidos) basados en la 
    probabilidad conjunta de las variables discretizadas para cada partición.
    """
    NOMBRES_COMPLETOS = {
        "X1": "Sexo", "X2": "Zona", "X3": "Ciclo",
        "X4": "Ingreso", "X5": "Trabaja", "X6": "Beca",
        "X7": "Educ.Jefe", "X8": "Tam.Fam", "X9": "Asistencia",
        "X10": "Desaprobados", "X11": "Rendimiento"
    }

    def __init__(self, dir_salida="results/graficos", umbral=0.25):
        self.dir_salida = os.path.normpath(dir_salida)
        self.umbral = umbral
        self.arboles = {}

    def _mapear_educacion(self, val):
        val_str = str(val).lower().strip()
        if "sin" in val_str:
            return 0
        elif "prim" in val_str:
            return 1
        elif "sec" in val_str:
            return 2
        elif "tec" in val_str:
            return 3
        elif "univ" in val_str:
            return 4
        return 2

    def discretizar_dataframe(self, df):
        """
        Discretiza todas las variables continuas y categóricas del DataFrame
        a valores binarios (0 y 1) para permitir el análisis probabilístico.
        """
        df_disc = pd.DataFrame()
        
        # X1_sexo (Masculino -> 0, Femenino -> 1)
        df_disc["X1"] = df["X1_sexo"].apply(lambda x: 0 if str(x).lower().startswith("masc") else 1).astype(int)
        
        # X2_zona (Rural -> 0, Urbana -> 1)
        df_disc["X2"] = df["X2_zona"].apply(lambda x: 0 if str(x).lower().startswith("rur") else 1).astype(int)
        
        # X3_ciclo (>= mediana -> 1)
        df_disc["X3"] = (df["X3_ciclo"] >= df["X3_ciclo"].median()).astype(int)
        
        # X4_ingreso_familiar (>= mediana -> 1)
        df_disc["X4"] = (df["X4_ingreso_familiar"] >= df["X4_ingreso_familiar"].median()).astype(int)
        
        # X5_trabaja (No -> 0, Si -> 1)
        df_disc["X5"] = df["X5_trabaja"].apply(lambda x: 0 if str(x).lower().strip() == 'no' else 1).astype(int)
        
        # X6_beca (No -> 0, Si -> 1)
        df_disc["X6"] = df["X6_beca"].apply(lambda x: 0 if str(x).lower().strip() == 'no' else 1).astype(int)
        
        # X7_educ_jefe (>= mediana de nivel de educación -> 1)
        educ_mapped = df["X7_educ_jefe"].apply(self._mapear_educacion)
        df_disc["X7"] = (educ_mapped >= educ_mapped.median()).astype(int)
        
        # X8_tam_familiar (>= mediana -> 1)
        df_disc["X8"] = (df["X8_tam_familiar"] >= df["X8_tam_familiar"].median()).astype(int)
        
        # X9_asistencia (>= mediana -> 1)
        df_disc["X9"] = (df["X9_asistencia"] >= df["X9_asistencia"].median()).astype(int)
        
        # X10_cursos_desaprobados (> 0 -> 1)
        df_disc["X10"] = (df["X10_cursos_desaprobados"] > 0).astype(int)
        
        # X11_promedio_final (>= 11 aprobado -> 1)
        df_disc["X11"] = (df["X11_promedio_final"] >= 11).astype(int)
        
        return df_disc

    def construir_arbol_bayesiano(self, df_part, nombre):
        """
        Construye un árbol de variables dirigidas donde las aristas representan 
        asociaciones probabilísticas conjuntas máximas ordenadas como un MST.
        """
        df_disc = self.discretizar_dataframe(df_part)
        n = len(df_disc)
        variables = list(df_disc.columns)

        # 1. Crear Grafo Completo con pesos = 1 - Probabilidad Conjunta Máxima
        G_completo = nx.Graph()
        for var in variables:
            G_completo.add_node(var)

        datos_aristas = {}
        for var_i, var_j in combinations(variables, 2):
            counts = df_disc.groupby([var_i, var_j]).size().unstack(fill_value=0)
            
            # Asegurar representación de los 4 estados
            for val_i in [0, 1]:
                if val_i not in counts.index:
                    counts.loc[val_i] = 0
            for val_j in [0, 1]:
                if val_j not in counts.columns:
                    counts[val_j] = 0
            counts = counts.loc[[0, 1], [0, 1]]
            probs = counts / n
            
            # Encontrar el estado (a, b) con la probabilidad conjunta máxima
            max_prob = -1.0
            max_state = None
            for a in [0, 1]:
                for b in [0, 1]:
                    p = probs.loc[a, b]
                    if p > max_prob:
                        max_prob = p
                        max_state = (a, b)
            
            # Distancia inversa
            dist = 1.0 - max_prob
            G_completo.add_edge(var_i, var_j, weight=dist)
            datos_aristas[(var_i, var_j)] = (max_prob, max_state)

        # 2. Obtener el Árbol de Expansión Mínima (MST)
        mst_no_dirigido = nx.minimum_spanning_tree(G_completo, weight="weight")

        # 3. Direccionar el MST usando la regla de Probabilidad Condicional
        arbol_bayesiano = nx.DiGraph()
        for var in variables:
            arbol_bayesiano.add_node(var)

        for u, v in mst_no_dirigido.edges():
            llave = (u, v) if (u, v) in datos_aristas else (v, u)
            max_prob, max_state = datos_aristas[llave]
            
            if llave == (u, v):
                estado_u, estado_v = max_state
            else:
                estado_v, estado_u = max_state
                
            p_u = (df_disc[u] == estado_u).sum() / n
            p_v = (df_disc[v] == estado_v).sum() / n
            
            # Direccionar de menor probabilidad marginal a mayor
            # Esto equivale a apuntar en la dirección con mayor probabilidad condicional
            if p_u <= p_v:
                arbol_bayesiano.add_edge(u, v, weight=max_prob, state=(estado_u, estado_v))
            else:
                arbol_bayesiano.add_edge(v, u, weight=max_prob, state=(estado_v, estado_u))

        self.arboles[nombre] = arbol_bayesiano
        self.graficar_arbol(arbol_bayesiano, nombre)
        return arbol_bayesiano

    def graficar_arbol(self, arbol, nombre):
        """
        Dibuja el Árbol Bayesiano con flechas de dirección de dependencia
        y colores según el tipo de variable.
        """
        fig, ax = plt.subplots(figsize=(12, 10))

        categoricas = {"X1", "X2", "X5", "X6", "X7"}
        numericas = {"X3", "X4", "X8", "X9", "X10"}
        target = {"X11"}

        colores_nodo = []
        for nodo in arbol.nodes():
            if nodo in target:
                colores_nodo.append("#66BB6A")  # verde = Target (X11)
            elif nodo in categoricas:
                colores_nodo.append("#FF7043")  # naranja = Categórica
            else:
                colores_nodo.append("#42A5F5")  # azul = Numérica

        # Layout del Grafo
        pos = nx.spring_layout(arbol, seed=42, k=2.0)

        # Dibujar aristas dirigidas
        nx.draw_networkx_edges(
            arbol, pos, ax=ax,
            arrows=True, arrowstyle="-|>", arrowsize=20,
            edge_color="#455A64", width=2.5, alpha=0.8
        )

        # Dibujar nodos
        nx.draw_networkx_nodes(
            arbol, pos, ax=ax, node_size=1300,
            node_color=colores_nodo, edgecolors="white", linewidths=2.5
        )

        # Nombres de etiquetas
        etiquetas = {n: f"{n}\n{self.NOMBRES_COMPLETOS.get(n, '')}" for n in arbol.nodes()}
        nx.draw_networkx_labels(
            arbol, pos, labels=etiquetas, ax=ax,
            font_size=8, font_weight="bold", font_color="white"
        )

        # Etiquetas de las aristas: Probabilidad Conjunta y Estado
        etiquetas_aristas = {}
        for u, v, data in arbol.edges(data=True):
            prob = data["weight"]
            est = data["state"]
            etiquetas_aristas[(u, v)] = f"P={prob:.2f}\n{est}"

        nx.draw_networkx_edge_labels(
            arbol, pos, edge_labels=etiquetas_aristas,
            ax=ax, font_size=8, font_color="#37474F"
        )

        # Leyenda
        parche_cat = mpatches.Patch(color="#FF7043", label="Variable Categórica")
        parche_num = mpatches.Patch(color="#42A5F5", label="Variable Numérica")
        parche_tar = mpatches.Patch(color="#66BB6A", label="Rendimiento (X11)")
        ax.legend(handles=[parche_cat, parche_num, parche_tar], loc="upper left", fontsize=10)

        tipo = "BEST (Alto rendimiento)" if "Best" in nombre else "WORST (Bajo rendimiento)"
        pct = nombre.split("_")[1] if "_" in nombre else "Completo"
        ax.set_title(f"Árbol Bayesiano Probabilístico (MST Dirigido) - {tipo}\n"
                     f"Partición: {pct}% | Enlaces basados en Max Probabilidad Conjunta",
                     fontsize=13, fontweight="bold")
        ax.axis("off")

        plt.tight_layout()
        path = os.path.join(self.dir_salida, f"arbol_bayesiano_{nombre}.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"      💾 Gráfico guardado: arbol_bayesiano_{nombre}.png")

    def ejecutar_paso(self, df_limpio, particiones):
        os.makedirs(self.dir_salida, exist_ok=True)
        self.arboles = {}

        # 1. Construir árbol para el dataset completo
        print("\n   🌳 Construyendo Árbol Bayesiano completo...")
        self.construir_arbol_bayesiano(df_limpio, "Completo")

        # 2. Construir árbol para cada partición Best/Worst
        for nombre, df_part in particiones.items():
            print(f"   🌳 Construyendo Árbol Bayesiano para {nombre}...")
            self.construir_arbol_bayesiano(df_part, nombre)

        return self.arboles
