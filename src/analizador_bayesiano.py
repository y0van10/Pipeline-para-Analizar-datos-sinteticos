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
    probabilidad conjunta de las variables discretizadas con flechas ultraclaras y legibles.
    También genera gráficos de Radar (Telaraña) comparativos.
    """
    NOMBRES_COMPLETOS = {
        "X1": "Sexo", "X2": "Zona", "X3": "Ciclo",
        "X4": "Ingreso", "X5": "Trabaja", "X6": "Beca",
        "X7": "Educ.Jefe", "X8": "Tam.Fam", "X9": "Asistencia",
        "X10": "Desaprobados", "X11": "Rendimiento"
    }

    def __init__(self, dir_base="results", umbral=0.25):
        self.dir_base = os.path.normpath(dir_base)
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
        df_disc = pd.DataFrame()
        
        df_disc["X1"] = df["X1_sexo"].apply(lambda x: 0 if str(x).lower().startswith("masc") else 1).astype(int)
        df_disc["X2"] = df["X2_zona"].apply(lambda x: 0 if str(x).lower().startswith("rur") else 1).astype(int)
        df_disc["X3"] = (df["X3_ciclo"] >= df["X3_ciclo"].median()).astype(int)
        df_disc["X4"] = (df["X4_ingreso_familiar"] >= df["X4_ingreso_familiar"].median()).astype(int)
        df_disc["X5"] = df["X5_trabaja"].apply(lambda x: 0 if str(x).lower().strip() == 'no' else 1).astype(int)
        df_disc["X6"] = df["X6_beca"].apply(lambda x: 0 if str(x).lower().strip() == 'no' else 1).astype(int)
        
        educ_mapped = df["X7_educ_jefe"].apply(self._mapear_educacion)
        df_disc["X7"] = (educ_mapped >= educ_mapped.median()).astype(int)
        
        df_disc["X8"] = (df["X8_tam_familiar"] >= df["X8_tam_familiar"].median()).astype(int)
        df_disc["X9"] = (df["X9_asistencia"] >= df["X9_asistencia"].median()).astype(int)
        df_disc["X10"] = (df["X10_cursos_desaprobados"] > 0).astype(int)
        df_disc["X11"] = (df["X11_promedio_final"] >= 11).astype(int)
        
        return df_disc

    def construir_arbol_bayesiano(self, df_part, nombre, nivel="global"):
        df_disc = self.discretizar_dataframe(df_part)
        n = len(df_disc)
        variables = list(df_disc.columns)

        G_completo = nx.Graph()
        for var in variables:
            G_completo.add_node(var)

        datos_aristas = {}
        for var_i, var_j in combinations(variables, 2):
            counts = df_disc.groupby([var_i, var_j]).size().unstack(fill_value=0)
            for val_i in [0, 1]:
                if val_i not in counts.index:
                    counts.loc[val_i] = 0
            for val_j in [0, 1]:
                if val_j not in counts.columns:
                    counts[val_j] = 0
            counts = counts.loc[[0, 1], [0, 1]]
            probs = counts / n
            
            max_prob = -1.0
            max_state = None
            for a in [0, 1]:
                for b in [0, 1]:
                    p = probs.loc[a, b]
                    if p > max_prob:
                        max_prob = p
                        max_state = (a, b)
            
            dist = 1.0 - max_prob
            G_completo.add_edge(var_i, var_j, weight=dist)
            datos_aristas[(var_i, var_j)] = (max_prob, max_state)

        mst_no_dirigido = nx.minimum_spanning_tree(G_completo, weight="weight")

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
            if p_u <= p_v:
                arbol_bayesiano.add_edge(u, v, weight=max_prob, state=(estado_u, estado_v))
            else:
                arbol_bayesiano.add_edge(v, u, weight=max_prob, state=(estado_v, estado_u))

        self.arboles[nombre] = arbol_bayesiano
        self.graficar_arbol(arbol_bayesiano, nombre, nivel)
        return arbol_bayesiano

    def graficar_arbol(self, arbol, nombre, nivel):
        fig, ax = plt.subplots(figsize=(13, 11))

        categoricas = {"X1", "X2", "X5", "X6", "X7"}
        target = {"X11"}

        colores_nodo = []
        tamaños_nodo = []
        for nodo in arbol.nodes():
            grado_in = arbol.in_degree(nodo)
            grado_out = arbol.out_degree(nodo)
            tamanio = 1400 + (grado_in + grado_out) * 200
            tamaños_nodo.append(tamanio)

            if nodo in target:
                colores_nodo.append("#2E7D32")  # verde oscuro = Rendimiento X11
            elif nodo in categoricas:
                colores_nodo.append("#E65100")  # naranja intenso = Categórica
            else:
                colores_nodo.append("#1565C0")  # azul intenso = Numérica

        pos = nx.spring_layout(arbol, seed=42, k=2.2)

        # Dibujar aristas dirigidas con arcos curvos y márgenes limpios
        nx.draw_networkx_edges(
            arbol, pos, ax=ax,
            arrows=True, arrowstyle="-|>", arrowsize=25,
            edge_color="#C62828", width=2.8, alpha=0.85,
            connectionstyle="arc3,rad=0.12",
            min_target_margin=30, min_source_margin=30
        )

        # Dibujar nodos
        nx.draw_networkx_nodes(
            arbol, pos, ax=ax, node_size=tamaños_nodo,
            node_color=colores_nodo, edgecolors="white", linewidths=2.5
        )

        # Etiquetas de nodos
        etiquetas = {n: f"{n}\n{self.NOMBRES_COMPLETOS.get(n, '')}" for n in arbol.nodes()}
        nx.draw_networkx_labels(
            arbol, pos, labels=etiquetas, ax=ax,
            font_size=9, font_weight="bold", font_color="white"
        )

        # Etiquetas de aristas (Probabilidad Conjunta y Estado)
        etiquetas_aristas = {}
        for u, v, data in arbol.edges(data=True):
            prob = data["weight"]
            est = data["state"]
            etiquetas_aristas[(u, v)] = f"P={prob:.2f}\n{est}"

        nx.draw_networkx_edge_labels(
            arbol, pos, edge_labels=etiquetas_aristas,
            ax=ax, font_size=8, font_color="#D32F2F", font_weight="bold"
        )

        # Leyenda explicativa
        parche_cat = mpatches.Patch(color="#E65100", label="Variable Categórica (X1, X2, X5-X7)")
        parche_num = mpatches.Patch(color="#1565C0", label="Variable Numérica (X3, X4, X8-X10)")
        parche_tar = mpatches.Patch(color="#2E7D32", label="Target: Rendimiento (X11)")
        ax.legend(handles=[parche_cat, parche_num, parche_tar], loc="upper left", fontsize=10)

        ax.set_title(f"Árbol Bayesiano Dirigido (Red Causal Probabilística) - {nombre}\n"
                     f"Las flechas indican la dirección del condicionamiento | Pesos = P(Xi, Xj)",
                     fontsize=13, fontweight="bold")
        ax.axis("off")

        plt.tight_layout()
        if nivel == "global":
            dir_g = os.path.join(self.dir_base, "global")
        else:
            dir_g = os.path.join(self.dir_base, f"nivel_{nivel}", "graficos")
        
        os.makedirs(dir_g, exist_ok=True)
        path = os.path.join(dir_g, f"arbol_bayesiano_{nombre}.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"      💾 Gráfico Bayesiano con flechas claras guardado: {path}")

    def graficar_radar_comparativo(self, df_particiones):
        """
        Genera un Gráfico de Telaraña / Radar comparando las medias de los factores
        entre el grupo de mayor y menor rendimiento.
        """
        pares = [
            ("50", "Best_50", "Worst_50"),
            ("25", "Best_25_1", "Worst_25_2"),
            ("12.5", "Best_12.5_1", "Worst_12.5_4")
        ]

        for nivel, n_best, n_worst in pares:
            if n_best not in df_particiones or n_worst not in df_particiones:
                continue

            df_b = df_particiones[n_best]["df"] if isinstance(df_particiones[n_best], dict) else df_particiones[n_best]
            df_w = df_particiones[n_worst]["df"] if isinstance(df_particiones[n_worst], dict) else df_particiones[n_worst]

            disc_b = self.discretizar_dataframe(df_b)
            disc_w = self.discretizar_dataframe(df_w)

            vars_radar = [f"X{i}" for i in range(1, 11)]
            means_b = [disc_b[v].mean() for v in vars_radar]
            means_w = [disc_w[v].mean() for v in vars_radar]

            angles = np.linspace(0, 2 * np.pi, len(vars_radar), endpoint=False).tolist()
            means_b += means_b[:1]
            means_w += means_w[:1]
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
            
            ax.plot(angles, means_b, color="#1E88E5", linewidth=2.5, linestyle="-", label=f"BEST ({n_best})")
            ax.fill(angles, means_b, color="#1E88E5", alpha=0.25)

            ax.plot(angles, means_w, color="#E53935", linewidth=2.5, linestyle="-", label=f"WORST ({n_worst})")
            ax.fill(angles, means_w, color="#E53935", alpha=0.25)

            labels_full = [f"{v}\n({self.NOMBRES_COMPLETOS[v]})" for v in vars_radar]
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels_full, fontsize=9, fontweight="bold")
            ax.set_ylim(0, 1.0)
            ax.set_title(f"Gráfico de Telaraña (Radar) - Nivel {nivel}%\nComparación de Perfiles Socioacadémicos", fontsize=12, fontweight="bold", pad=20)
            ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1.1), fontsize=10)

            dir_g = os.path.join(self.dir_base, f"nivel_{nivel}", "graficos")
            os.makedirs(dir_g, exist_ok=True)
            path = os.path.join(dir_g, f"radar_comparativo_{nivel}.png")
            plt.savefig(path, dpi=150, bbox_inches="tight")
            plt.close()
            print(f"      💾 Gráfico Radar comparativo guardado: {path}")

    def ejecutar_paso(self, df_limpio, particiones):
        self.arboles = {}

        # 1. Árbol completo
        print("\n   🌳 Construyendo Árbol Bayesiano completo...")
        self.construir_arbol_bayesiano(df_limpio, "Completo", nivel="global")

        # 2. Árboles por bloque
        for nombre, info in particiones.items():
            nivel = info["nivel"]
            ruta_csv = info["ruta_csv"]
            df_part = pd.read_csv(ruta_csv)
            print(f"   🌳 Construyendo Árbol Bayesiano para {nombre} desde {os.path.basename(ruta_csv)}...")
            self.construir_arbol_bayesiano(df_part, nombre, nivel=nivel)

        # 3. Graficar Radar Comparativo
        print("\n   🕸️ Generando gráficos de Radar (Telaraña)...")
        self.graficar_radar_comparativo(particiones)

        return self.arboles
