import os
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform

class GestorTopologias:
    """
    Clase encargada de construir las topologías de red (MST), heatmaps y dendrogramas
    a partir de las matrices de distancias NCD de cada partición, guardando las imágenes
    en las carpetas organizadas por nivel.
    """
    NOMBRES_COMPLETOS = {
        "X1": "Sexo", "X2": "Zona", "X3": "Ciclo",
        "X4": "Ingreso", "X5": "Trabaja", "X6": "Beca",
        "X7": "Educ.Jefe", "X8": "Tam.Fam", "X9": "Asistencia",
        "X10": "Desaprobados"
    }

    def __init__(self, dir_base="results"):
        self.dir_base = os.path.normpath(dir_base)
        self.topologias = {}

    def construir_grafo_completo(self, df_matriz):
        G = nx.Graph()
        etiquetas = list(df_matriz.index)
        for i, var_i in enumerate(etiquetas):
            G.add_node(var_i)
            for j, var_j in enumerate(etiquetas):
                if i < j:
                    peso = df_matriz.iloc[i, j]
                    G.add_edge(var_i, var_j, weight=peso)
        return G

    def extraer_mst(self, G):
        return nx.minimum_spanning_tree(G, weight="weight")

    def calcular_grado_ponderado(self, mst):
        grados = {}
        for nodo in mst.nodes():
            peso_total = sum(mst[nodo][vecino]["weight"] for vecino in mst.neighbors(nodo))
            grados[nodo] = round(peso_total, 6)
        return grados

    def _obtener_dir_graficos(self, nivel):
        dir_g = os.path.join(self.dir_base, f"nivel_{nivel}", "graficos")
        os.makedirs(dir_g, exist_ok=True)
        return dir_g

    def graficar_mst(self, mst, nombre, nivel):
        fig, ax = plt.subplots(figsize=(12, 10))
        categoricas = {"X1", "X2", "X5", "X6", "X7"}
        
        colores_nodo = ["#FF7043" if n in categoricas else "#42A5F5" for n in mst.nodes()]
        pos = nx.spring_layout(mst, seed=42, k=2.5)

        pesos = [mst[u][v]["weight"] for u, v in mst.edges()]
        peso_max = max(pesos) if pesos else 1
        anchos = [3.0 * (1 - w / peso_max) + 0.5 for w in pesos]

        nx.draw_networkx_edges(mst, pos, ax=ax, width=anchos, alpha=0.6, edge_color="#78909C")
        edge_labels = {(u, v): f"{mst[u][v]['weight']:.3f}" for u, v in mst.edges()}
        nx.draw_networkx_edge_labels(mst, pos, edge_labels=edge_labels, ax=ax, font_size=8, font_color="#546E7A")

        nx.draw_networkx_nodes(mst, pos, ax=ax, node_size=1200, node_color=colores_nodo, edgecolors="white", linewidths=2.5)
        labels = {n: f"{n}\n{self.NOMBRES_COMPLETOS.get(n, '')}" for n in mst.nodes()}
        nx.draw_networkx_labels(mst, pos, labels=labels, ax=ax, font_size=8, font_weight="bold", font_color="white")

        parche_cat = mpatches.Patch(color="#FF7043", label="Categórica")
        parche_num = mpatches.Patch(color="#42A5F5", label="Numérica")
        ax.legend(handles=[parche_cat, parche_num], loc="upper left", fontsize=10)

        tipo = "BEST" if "Best" in nombre else "WORST"
        ax.set_title(f"Árbol de Expansión Mínima (MST) - {nombre}\nPartición Nivel {nivel}% | Variables X1-X10", fontsize=13, fontweight="bold")
        ax.axis("off")

        plt.tight_layout()
        dir_g = self._obtener_dir_graficos(nivel)
        path = os.path.join(dir_g, f"mst_{nombre}.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def graficar_heatmap(self, df_matriz, nombre, nivel):
        fig, ax = plt.subplots(figsize=(10, 8))
        datos = df_matriz.values
        etiquetas = list(df_matriz.index)

        im = ax.imshow(datos, cmap="YlOrRd", vmin=0, vmax=1)
        plt.colorbar(im, ax=ax, label="Distancia NCD (0=similar, 1=diferente)")

        ax.set_xticks(range(len(etiquetas)))
        ax.set_yticks(range(len(etiquetas)))
        etiq_completas = [f"{e}\n{self.NOMBRES_COMPLETOS.get(e, '')}" for e in etiquetas]
        ax.set_xticklabels(etiq_completas, rotation=45, ha="right", fontsize=8)
        ax.set_yticklabels(etiq_completas, fontsize=8)

        for i in range(len(etiquetas)):
            for j in range(len(etiquetas)):
                color_texto = "white" if datos[i, j] > 0.7 else "black"
                ax.text(j, i, f"{datos[i, j]:.3f}", ha="center", va="center", fontsize=7, color=color_texto)

        ax.set_title(f"Matriz NCD - {nombre} (Nivel {nivel}%)\nDistancias entre Variables X1-X10", fontsize=12, fontweight="bold")
        
        plt.tight_layout()
        dir_g = self._obtener_dir_graficos(nivel)
        path = os.path.join(dir_g, f"heatmap_{nombre}.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def graficar_dendrograma(self, df_matriz, nombre, nivel):
        fig, ax = plt.subplots(figsize=(12, 7))
        etiquetas = list(df_matriz.index)
        etiq_completas = [f"{e} ({self.NOMBRES_COMPLETOS.get(e, '')})" for e in etiquetas]

        mat = df_matriz.values.copy()
        np.fill_diagonal(mat, 0)
        dist_condensada = squareform(mat, checks=False)
        Z = linkage(dist_condensada, method="ward")
        color_umbral = 0.5 * max(Z[:, 2]) if len(Z) > 0 else 0

        dendrogram(Z, labels=etiq_completas, ax=ax, leaf_rotation=35, leaf_font_size=9,
                   color_threshold=color_umbral, above_threshold_color="#78909C")

        categoricas_idx = {"X1", "X2", "X5", "X6", "X7"}
        for lbl in ax.get_xmajorticklabels():
            var_id = lbl.get_text().split(" ")[0]
            lbl.set_color("#E65100" if var_id in categoricas_idx else "#1565C0")
            lbl.set_fontweight("bold")

        ax.set_title(f"Dendrograma Jerárquico - {nombre}\nPartición Nivel {nivel}% | Agrupamiento de Variables por NCD", fontsize=13, fontweight="bold")
        ax.set_ylabel("Distancia (Ward)", fontsize=11)

        parche_cat = mpatches.Patch(color="#E65100", label="Categórica")
        parche_num = mpatches.Patch(color="#1565C0", label="Numérica")
        ax.legend(handles=[parche_cat, parche_num], loc="upper right", fontsize=10)
        ax.grid(axis="y", alpha=0.3, linestyle="--")

        plt.tight_layout()
        dir_g = self._obtener_dir_graficos(nivel)
        path = os.path.join(dir_g, f"dendrograma_{nombre}.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def graficar_dendrograma_comparativo(self, matrices):
        pares_comparativos = [
            ("50", "Best_50", "Worst_50", "BEST (Alto Rendimiento)", "WORST (Bajo Rendimiento)"),
            ("25", "Best_25_1", "Worst_25_2", "BEST 25% (Extremo Superior)", "WORST 25% (Extremo Inferior)"),
            ("12.5", "Best_12.5_1", "Worst_12.5_4", "BEST 12.5% (Extremo Superior)", "WORST 12.5% (Extremo Inferior)")
        ]

        for nivel, n_best, n_worst, t_best, t_worst in pares_comparativos:
            if n_best not in matrices or n_worst not in matrices:
                continue

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

            for ax, nombre, tipo_t, color_t in [
                (ax1, n_best, t_best, "#1565C0"),
                (ax2, n_worst, t_worst, "#C62828")
            ]:
                df_matriz = matrices[nombre]["df_matriz"]
                etiquetas = list(df_matriz.index)
                etiq_completas = [f"{e} ({self.NOMBRES_COMPLETOS.get(e, '')})" for e in etiquetas]

                mat = df_matriz.values.copy()
                np.fill_diagonal(mat, 0)
                dist_condensada = squareform(mat, checks=False)
                Z = linkage(dist_condensada, method="ward")
                color_umbral = 0.5 * max(Z[:, 2]) if len(Z) > 0 else 0

                dendrogram(Z, labels=etiq_completas, ax=ax, leaf_rotation=40, leaf_font_size=8,
                           color_threshold=color_umbral, above_threshold_color="#78909C")

                ax.set_title(tipo_t, fontsize=12, fontweight="bold", color=color_t)
                ax.set_ylabel("Distancia (Ward)", fontsize=10)
                ax.grid(axis="y", alpha=0.3, linestyle="--")

                categoricas_idx = {"X1", "X2", "X5", "X6", "X7"}
                for lbl in ax.get_xmajorticklabels():
                    var_id = lbl.get_text().split(" ")[0]
                    lbl.set_color("#E65100" if var_id in categoricas_idx else "#1565C0")
                    lbl.set_fontweight("bold")

            fig.suptitle(f"Comparación de Dendrogramas Extremos - Partición Nivel {nivel}%\n¿Cómo cambia el agrupamiento entre extremos de rendimiento?", fontsize=14, fontweight="bold")
            plt.tight_layout()
            dir_g = self._obtener_dir_graficos(nivel)
            path = os.path.join(dir_g, f"dendrograma_comparativo_{nivel}.png")
            plt.savefig(path, dpi=150, bbox_inches="tight")
            plt.close()
            print(f"   💾 Dendrograma comparativo generado en nivel_{nivel}: dendrograma_comparativo_{nivel}.png")

    def construir_topologias(self, matrices):
        self.topologias = {}

        for nombre, info in matrices.items():
            nivel = info["nivel"]
            df_matriz = info["df_matriz"]
            print(f"\n   🔧 Construyendo topología para {nombre} (Nivel {nivel}%)...")
            
            G = self.construir_grafo_completo(df_matriz)
            mst = self.extraer_mst(G)
            peso_total = sum(mst[u][v]["weight"] for u, v in mst.edges())
            grados = self.calcular_grado_ponderado(mst)

            # Guardar imágenes por carpeta de nivel
            self.graficar_mst(mst, nombre, nivel)
            self.graficar_heatmap(df_matriz, nombre, nivel)
            self.graficar_dendrograma(df_matriz, nombre, nivel)

            self.topologias[nombre] = {
                "nivel": nivel,
                "mst": mst,
                "grados": grados,
                "grafo_completo": G,
                "peso_total_mst": peso_total
            }
            print(f"      ✅ MST, Heatmap y Dendrograma guardados en results/nivel_{nivel}/graficos/")

        return self.topologias

    def ejecutar(self, matrices):
        return self.construir_topologias(matrices)
