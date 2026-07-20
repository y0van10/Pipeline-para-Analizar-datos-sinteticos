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
    Clase encargada de construir las topologías de red:
    1. Grafo NCD Completo (Todos contra Todos sin filtrar).
    2. Árbol de Expansión Mínima (MST).
    3. Heatmaps de distancias NCD.
    4. Dendrogramas de agrupamiento jerárquico.
    """
    def __init__(self, dir_base="results"):
        self.dir_base = os.path.normpath(dir_base)
        self.topologias = {}

    def _es_categorica(self, nombre_col, df_ref=None):
        kw_cat = ["sexo", "gender", "sex", "zona", "zone", "area", "trabaja", "work",
                  "beca", "scholarship", "educ", "school_type", "type", "internet",
                  "parental", "involvement", "extracurricular", "disability", "peer"]
        nombre_lower = nombre_col.lower()
        if any(kw in nombre_lower for kw in kw_cat):
            return True
        return False

    def construir_grafo_completo(self, df_matriz):
        G = nx.Graph()
        etiquetas = list(df_matriz.index)
        for i, var_i in enumerate(etiquetas):
            G.add_node(var_i)
            for j, var_j in enumerate(etiquetas):
                if i < j:
                    G.add_edge(var_i, var_j, weight=float(df_matriz.iloc[i, j]))
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

    def graficar_grafo_completo(self, G, nombre, nivel):
        """
        Grafica el Grafo NCD Completo (Todos contra Todos)
        donde la grosor y opacidad de las aristas varían según la similitud (1 - NCD).
        """
        fig, ax = plt.subplots(figsize=(14, 11))

        colores_nodo = ["#FF7043" if self._es_categorica(n) else "#42A5F5" for n in G.nodes()]
        pos = nx.circular_layout(G) if len(G.nodes()) > 12 else nx.spring_layout(G, seed=42, k=2.0)

        pesos = [G[u][v]["weight"] for u, v in G.edges()]
        min_p = min(pesos) if pesos else 0
        max_p = max(pesos) if pesos else 1

        # En NCD, menor peso = mayor similitud. Queremos destacar aristas con menor NCD.
        similitud = [1.0 - w for w in pesos]
        sim_min = min(similitud) if similitud else 0
        sim_max = max(similitud) if similitud else 1

        anchos = [0.5 + 3.0 * ((s - sim_min) / (sim_max - sim_min + 1e-6)) for s in similitud]
        alphas = [0.15 + 0.65 * ((s - sim_min) / (sim_max - sim_min + 1e-6)) for s in similitud]

        for (u, v), w_val, a_val in zip(G.edges(), anchos, alphas):
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], ax=ax,
                                   width=w_val, alpha=a_val, edge_color="#37474F")

        # Dibujar etiquetas solo en las NCD más similares (top 40%) si hay muchas variables
        umbral_sim = np.percentile(similitud, 60) if len(similitud) > 25 else 0.0
        edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in G.edges() if (1.0 - G[u][v]['weight']) >= umbral_sim}
        if edge_labels:
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=6, font_color="#D32F2F")

        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=1300,
                               node_color=colores_nodo, edgecolors="white", linewidths=2.5)

        labels = {n: n[:16] + "…" if len(n) > 16 else n for n in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=7, font_weight="bold", font_color="white")

        parche_cat = mpatches.Patch(color="#FF7043", label="Variable Categórica")
        parche_num = mpatches.Patch(color="#42A5F5", label="Variable Numérica")
        ax.legend(handles=[parche_cat, parche_num], loc="upper left", fontsize=9)

        n_vars = len(list(G.nodes()))
        n_edges = len(list(G.edges()))
        ax.set_title(f"Grafo NCD Completo (Todos contra Todos) — {nombre}\n"
                     f"Partición Nivel {nivel}% | {n_vars} variables ({n_edges} conexiones NCD)",
                     fontsize=13, fontweight="bold")
        ax.axis("off")

        plt.tight_layout()
        dir_g = self._obtener_dir_graficos(nivel)
        path = os.path.join(dir_g, f"grafo_completo_{nombre}.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def graficar_mst(self, mst, nombre, nivel):
        fig, ax = plt.subplots(figsize=(14, 11))

        colores_nodo = ["#FF7043" if self._es_categorica(n) else "#42A5F5" for n in mst.nodes()]
        pos = nx.spring_layout(mst, seed=42, k=2.5)

        pesos = [mst[u][v]["weight"] for u, v in mst.edges()]
        peso_max = max(pesos) if pesos else 1
        anchos = [3.0 * (1 - w / peso_max) + 0.5 for w in pesos]

        nx.draw_networkx_edges(mst, pos, ax=ax, width=anchos, alpha=0.6, edge_color="#78909C")
        edge_labels = {(u, v): f"{mst[u][v]['weight']:.3f}" for u, v in mst.edges()}
        nx.draw_networkx_edge_labels(mst, pos, edge_labels=edge_labels, ax=ax, font_size=7, font_color="#546E7A")

        nx.draw_networkx_nodes(mst, pos, ax=ax, node_size=1400,
                               node_color=colores_nodo, edgecolors="white", linewidths=2.5)

        labels = {n: n[:18] + "…" if len(n) > 18 else n for n in mst.nodes()}
        nx.draw_networkx_labels(mst, pos, labels=labels, ax=ax, font_size=7, font_weight="bold", font_color="white")

        parche_cat = mpatches.Patch(color="#FF7043", label="Variable Categórica")
        parche_num = mpatches.Patch(color="#42A5F5", label="Variable Numérica")
        ax.legend(handles=[parche_cat, parche_num], loc="upper left", fontsize=9)

        n_vars = len(list(mst.nodes()))
        ax.set_title(f"Árbol de Expansión Mínima (MST) — {nombre}\n"
                     f"Partición Nivel {nivel}% | {n_vars} variables",
                     fontsize=13, fontweight="bold")
        ax.axis("off")

        plt.tight_layout()
        dir_g = self._obtener_dir_graficos(nivel)
        path = os.path.join(dir_g, f"mst_{nombre}.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def graficar_heatmap(self, df_matriz, nombre, nivel):
        fig, ax = plt.subplots(figsize=(max(8, len(df_matriz) * 0.8),
                                        max(7, len(df_matriz) * 0.7)))
        datos = df_matriz.values
        etiquetas = list(df_matriz.index)

        im = ax.imshow(datos, cmap="YlOrRd", vmin=0, vmax=1)
        plt.colorbar(im, ax=ax, label="Distancia NCD (0=similar, 1=diferente)")

        etiq_cortas = [e[:14] + "…" if len(e) > 14 else e for e in etiquetas]
        ax.set_xticks(range(len(etiquetas)))
        ax.set_yticks(range(len(etiquetas)))
        ax.set_xticklabels(etiq_cortas, rotation=45, ha="right", fontsize=7)
        ax.set_yticklabels(etiq_cortas, fontsize=7)

        for i in range(len(etiquetas)):
            for j in range(len(etiquetas)):
                color_texto = "white" if datos[i, j] > 0.7 else "black"
                ax.text(j, i, f"{datos[i, j]:.3f}", ha="center", va="center",
                        fontsize=6, color=color_texto)

        ax.set_title(f"Matriz NCD — {nombre} (Nivel {nivel}%)\n"
                     f"Distancias entre {len(etiquetas)} variables",
                     fontsize=12, fontweight="bold")

        plt.tight_layout()
        dir_g = self._obtener_dir_graficos(nivel)
        path = os.path.join(dir_g, f"heatmap_{nombre}.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def graficar_dendrograma(self, df_matriz, nombre, nivel):
        fig, ax = plt.subplots(figsize=(max(12, len(df_matriz) * 1.2), 7))
        etiquetas = list(df_matriz.index)
        etiq_cortas = [e[:16] + "…" if len(e) > 16 else e for e in etiquetas]

        mat = df_matriz.values.copy()
        np.fill_diagonal(mat, 0)
        dist_condensada = squareform(mat, checks=False)
        Z = linkage(dist_condensada, method="ward")
        color_umbral = 0.5 * max(Z[:, 2]) if len(Z) > 0 else 0

        dendrogram(Z, labels=etiq_cortas, ax=ax, leaf_rotation=40, leaf_font_size=8,
                   color_threshold=color_umbral, above_threshold_color="#78909C")

        for lbl in ax.get_xmajorticklabels():
            var_id = lbl.get_text()
            lbl.set_color("#E65100" if self._es_categorica(var_id) else "#1565C0")
            lbl.set_fontweight("bold")

        ax.set_title(f"Dendrograma Jerárquico — {nombre}\n"
                     f"Partición Nivel {nivel}% | Agrupamiento por NCD",
                     fontsize=13, fontweight="bold")
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
            ("50",  "Best_50",     "Worst_50",     "BEST (Alto Rendimiento)",    "WORST (Bajo Rendimiento)"),
            ("25",  "Best_25_1",   "Worst_25_2",   "BEST 25% (Extremo Superior)","WORST 25% (Extremo Inferior)"),
            ("12.5","Best_12.5_1", "Worst_12.5_4", "BEST 12.5% (Extremo Sup.)",  "WORST 12.5% (Extremo Inf.)"),
        ]

        for nivel, n_best, n_worst, t_best, t_worst in pares_comparativos:
            if n_best not in matrices or n_worst not in matrices:
                continue

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 8))

            for ax, nombre, tipo_t, color_t in [
                (ax1, n_best,  t_best,  "#1565C0"),
                (ax2, n_worst, t_worst, "#C62828"),
            ]:
                df_matriz = matrices[nombre]["df_matriz"]
                etiquetas = list(df_matriz.index)
                etiq_cortas = [e[:14] + "…" if len(e) > 14 else e for e in etiquetas]

                mat = df_matriz.values.copy()
                np.fill_diagonal(mat, 0)
                dist_condensada = squareform(mat, checks=False)
                Z = linkage(dist_condensada, method="ward")
                color_umbral = 0.5 * max(Z[:, 2]) if len(Z) > 0 else 0

                dendrogram(Z, labels=etiq_cortas, ax=ax, leaf_rotation=40, leaf_font_size=8,
                           color_threshold=color_umbral, above_threshold_color="#78909C")

                ax.set_title(tipo_t, fontsize=12, fontweight="bold", color=color_t)
                ax.set_ylabel("Distancia (Ward)", fontsize=10)
                ax.grid(axis="y", alpha=0.3, linestyle="--")

                for lbl in ax.get_xmajorticklabels():
                    var_id = lbl.get_text()
                    lbl.set_color("#E65100" if self._es_categorica(var_id) else "#1565C0")
                    lbl.set_fontweight("bold")

            fig.suptitle(f"Comparación Dendrogramas Extremos — Nivel {nivel}%\n"
                         "¿Cómo cambia el agrupamiento entre los mejores y peores?",
                         fontsize=14, fontweight="bold")
            plt.tight_layout()
            dir_g = self._obtener_dir_graficos(nivel)
            path = os.path.join(dir_g, f"dendrograma_comparativo_{nivel}.png")
            plt.savefig(path, dpi=150, bbox_inches="tight")
            plt.close()
            print(f"   💾 Dendrograma comparativo nivel_{nivel}: dendrograma_comparativo_{nivel}.png")

    def construir_topologias(self, matrices):
        self.topologias = {}

        for nombre, info in matrices.items():
            nivel = info["nivel"]
            df_matriz = info["df_matriz"]
            n_vars = len(df_matriz)
            print(f"\n   🔧 Topología '{nombre}' (Nivel {nivel}%, {n_vars} variables)...")

            G = self.construir_grafo_completo(df_matriz)
            mst = self.extraer_mst(G)
            peso_total = sum(mst[u][v]["weight"] for u, v in mst.edges())
            grados = self.calcular_grado_ponderado(mst)

            # Generar los 4 artefactos topológicos
            self.graficar_grafo_completo(G, nombre, nivel)
            self.graficar_mst(mst, nombre, nivel)
            self.graficar_heatmap(df_matriz, nombre, nivel)
            self.graficar_dendrograma(df_matriz, nombre, nivel)

            self.topologias[nombre] = {
                "nivel": nivel,
                "mst": mst,
                "grados": grados,
                "grafo_completo": G,
                "peso_total_mst": peso_total,
            }
            print(f"      ✅ Grafo Completo, MST, Heatmap y Dendrograma guardados en results/nivel_{nivel}/graficos/")

        return self.topologias

    def ejecutar(self, matrices):
        return self.construir_topologias(matrices)
