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
    probabilidad conjunta y la Jerarquía Causal Transitiva.
    Funciona con cualquier dataset y cualquier número de columnas.
    La jerarquía causal se infiere automáticamente a partir de la correlación con
    la variable objetivo (col_objetivo).
    """
    def __init__(self, dir_base="results", umbral=0.25, col_objetivo=None):
        self.dir_base    = os.path.normpath(dir_base)
        self.umbral      = umbral
        self.col_objetivo = col_objetivo
        self.arboles     = {}

    # ──────────────────────────────────────────────
    # Discretización universal (sin hardcoding)
    # ──────────────────────────────────────────────
    def discretizar_columna(self, serie):
        """
        Convierte una columna a binaria (0/1) de forma automática:
        - Si numérica: ≥ mediana → 1
        - Si categórica binaria (2 valores únicos): ordena y asigna 0/1
        - Si categórica múltiple: los que aparecen más del 50% → 1
        """
        serie = serie.copy()
        # Intentar convertir a número
        numerica = pd.to_numeric(serie, errors="coerce")
        if numerica.notna().mean() > 0.7:
            mediana = numerica.median()
            return (numerica >= mediana).astype(int).fillna(0)

        # Categórica
        unicos = serie.dropna().unique()
        if len(unicos) <= 2:
            ordenados = sorted(unicos, key=lambda x: str(x).lower())
            mapeo = {val: i for i, val in enumerate(ordenados)}
            return serie.map(mapeo).fillna(0).astype(int)

        # Múltiples categorías: top moda → 1, resto → 0
        moda = serie.mode()[0] if not serie.mode().empty else unicos[0]
        return (serie == moda).astype(int)

    def discretizar_dataframe(self, df, columnas_vars):
        """
        Discretiza solo las columnas de análisis (excluye col_objetivo).
        Retorna DataFrame con columnas originales binarizadas + col_objetivo binarizada.
        """
        df_disc = pd.DataFrame(index=df.index)
        for col in columnas_vars:
            if col in df.columns:
                df_disc[col] = self.discretizar_columna(df[col])

        # Incluir objetivo binarizado al final
        if self.col_objetivo and self.col_objetivo in df.columns:
            mediana_obj = pd.to_numeric(df[self.col_objetivo], errors="coerce").median()
            df_disc[self.col_objetivo] = (
                pd.to_numeric(df[self.col_objetivo], errors="coerce") >= mediana_obj
            ).astype(int).fillna(0)

        return df_disc

    def inferir_nivel_causal(self, df, columnas_vars):
        """
        Infiere la jerarquía causal de cada variable basándose en su
        correlación (punto-biserial o de Pearson) con la variable objetivo.
        - Nivel 2 (Resultado): col_objetivo
        - Nivel 1 (Alta corr): |r| > 0.2
        - Nivel 0 (Baja corr): |r| <= 0.2
        """
        niveles = {}
        if not self.col_objetivo or self.col_objetivo not in df.columns:
            for col in columnas_vars:
                niveles[col] = 0
            return niveles

        obj_num = pd.to_numeric(df[self.col_objetivo], errors="coerce").fillna(0)

        for col in columnas_vars:
            try:
                col_num = pd.to_numeric(df[col], errors="coerce")
                if col_num.notna().mean() < 0.5:
                    # Categórica: binarizar para correlación
                    col_num = self.discretizar_columna(df[col]).astype(float)
                else:
                    col_num = col_num.fillna(col_num.median())
                r = abs(col_num.corr(obj_num))
                niveles[col] = 1 if r > 0.2 else 0
            except Exception:
                niveles[col] = 0

        if self.col_objetivo:
            niveles[self.col_objetivo] = 2  # siempre el resultado final

        return niveles

    # ──────────────────────────────────────────────
    # Construcción del árbol bayesiano
    # ──────────────────────────────────────────────
    def construir_arbol_bayesiano(self, df_part, nombre, nivel="global"):
        # Determinar columnas de análisis (excluir objetivo para el NCD,
        # pero incluirlo en el árbol bayesiano como nodo resultado)
        columnas_vars = [c for c in df_part.columns if c != self.col_objetivo]
        if self.col_objetivo and self.col_objetivo in df_part.columns:
            columnas_vars_bayes = columnas_vars + [self.col_objetivo]
        else:
            columnas_vars_bayes = columnas_vars

        df_disc = self.discretizar_dataframe(df_part, columnas_vars)
        variables = list(df_disc.columns)
        n = len(df_disc)

        if n < 5 or len(variables) < 2:
            print(f"      ⚠️  {nombre}: datos insuficientes para árbol bayesiano ({n} filas, {len(variables)} vars)")
            return None

        nivel_causal = self.inferir_nivel_causal(df_part, variables)

        # Grafo completo con probabilidades conjuntas
        G_completo = nx.Graph()
        for var in variables:
            G_completo.add_node(var)

        datos_aristas = {}
        for var_i, var_j in combinations(variables, 2):
            if var_i not in df_disc.columns or var_j not in df_disc.columns:
                continue
            counts = df_disc.groupby([var_i, var_j]).size().unstack(fill_value=0)
            for val in [0, 1]:
                if val not in counts.index:   counts.loc[val] = 0
                if val not in counts.columns: counts[val] = 0
            counts = counts.loc[[0, 1], [0, 1]]
            probs  = counts / n

            max_prob, max_state = -1.0, None
            for a in [0, 1]:
                for b in [0, 1]:
                    p = probs.loc[a, b]
                    if p > max_prob:
                        max_prob, max_state = p, (a, b)

            dist = 1.0 - max_prob
            G_completo.add_edge(var_i, var_j, weight=dist)
            datos_aristas[(var_i, var_j)] = (max_prob, max_state)

        mst_no_dirigido = nx.minimum_spanning_tree(G_completo, weight="weight")

        arbol = nx.DiGraph()
        for var in variables:
            arbol.add_node(var)

        for u, v in mst_no_dirigido.edges():
            llave = (u, v) if (u, v) in datos_aristas else (v, u)
            max_prob, max_state = datos_aristas[llave]

            if llave == (u, v):
                estado_u, estado_v = max_state
            else:
                estado_v, estado_u = max_state

            p_u = (df_disc[u] == estado_u).sum() / n if u in df_disc else 0.5
            p_v = (df_disc[v] == estado_v).sum() / n if v in df_disc else 0.5

            lvl_u = nivel_causal.get(u, 0)
            lvl_v = nivel_causal.get(v, 0)

            if lvl_u < lvl_v:
                arbol.add_edge(u, v, weight=max_prob, state=(estado_u, estado_v))
            elif lvl_v < lvl_u:
                arbol.add_edge(v, u, weight=max_prob, state=(estado_v, estado_u))
            else:
                if p_u <= p_v:
                    arbol.add_edge(u, v, weight=max_prob, state=(estado_u, estado_v))
                else:
                    arbol.add_edge(v, u, weight=max_prob, state=(estado_v, estado_u))

        self.arboles[nombre] = arbol
        self.graficar_arbol(arbol, nombre, nivel, nivel_causal)
        return arbol

    # ──────────────────────────────────────────────
    # Visualización del árbol
    # ──────────────────────────────────────────────
    def graficar_arbol(self, arbol, nombre, nivel, nivel_causal):
        n_nodos = len(arbol.nodes())
        fig_h   = max(11, n_nodos * 0.9)
        fig_w   = max(13, n_nodos * 1.1)
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))

        # ─ Colores por nivel causal ─
        COLOR_RAIZ     = "#E65100"  # naranja: antecedentes (nivel 0)
        COLOR_INTERM   = "#1565C0"  # azul: intermediarios (nivel 1)
        COLOR_OBJETIVO = "#2E7D32"  # verde: resultado (nivel 2)

        colores_nodo  = []
        tamaños_nodo  = []
        for nodo in arbol.nodes():
            lvl = nivel_causal.get(nodo, 0)
            grado_total = arbol.in_degree(nodo) + arbol.out_degree(nodo)
            tamaños_nodo.append(1400 + grado_total * 180)

            if lvl == 2:
                colores_nodo.append(COLOR_OBJETIVO)
            elif lvl == 1:
                colores_nodo.append(COLOR_INTERM)
            else:
                colores_nodo.append(COLOR_RAIZ)

        # ─ Layout por niveles causales ─
        pos = {}
        grupos_nivel = {}
        for nodo in arbol.nodes():
            lvl = nivel_causal.get(nodo, 0)
            grupos_nivel.setdefault(lvl, []).append(nodo)

        max_lvl = max(grupos_nivel.keys()) if grupos_nivel else 0
        for lvl, nodos in grupos_nivel.items():
            y = max_lvl - lvl  # nivel 0 arriba, nivel 2 abajo
            x_coords = np.linspace(-3.0, 3.0, len(nodos))
            for i, nodo in enumerate(sorted(nodos)):
                pos[nodo] = np.array([x_coords[i], y * 1.8])

        # ─ Dibujar aristas con flechas ─
        nx.draw_networkx_edges(
            arbol, pos, ax=ax,
            arrows=True, arrowstyle="-|>", arrowsize=28,
            edge_color="#C62828", width=2.8, alpha=0.85,
            connectionstyle="arc3,rad=0.12",
            min_target_margin=32, min_source_margin=32,
        )

        # ─ Dibujar nodos ─
        nx.draw_networkx_nodes(
            arbol, pos, ax=ax, node_size=tamaños_nodo,
            node_color=colores_nodo, edgecolors="white", linewidths=2.5,
        )

        # ─ Etiquetas de nodos (nombre real, recortado) ─
        etiquetas = {n: (n[:15] + "…" if len(n) > 15 else n) for n in arbol.nodes()}
        nx.draw_networkx_labels(arbol, pos, labels=etiquetas, ax=ax,
                                font_size=8, font_weight="bold", font_color="white")

        # ─ Etiquetas de aristas ─
        etiquetas_aristas = {}
        for u, v, data in arbol.edges(data=True):
            etiquetas_aristas[(u, v)] = f"P={data['weight']:.2f}"
        nx.draw_networkx_edge_labels(arbol, pos, edge_labels=etiquetas_aristas,
                                     ax=ax, font_size=7, font_color="#D32F2F",
                                     font_weight="bold")

        # ─ Leyenda ─
        parche_raiz = mpatches.Patch(color=COLOR_RAIZ,     label="Antecedentes (baja corr. con objetivo)")
        parche_int  = mpatches.Patch(color=COLOR_INTERM,   label="Intermediarios (alta corr. con objetivo)")
        parche_tar  = mpatches.Patch(color=COLOR_OBJETIVO, label=f"Objetivo: {self.col_objetivo or 'resultado'}")
        ax.legend(handles=[parche_raiz, parche_int, parche_tar], loc="upper left", fontsize=9)

        ax.set_title(f"Árbol Bayesiano Causal Jerárquico — {nombre}\n"
                     f"Flujo: Antecedentes ➔ Intermediarios ➔ {self.col_objetivo or 'Resultado'}",
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
        print(f"      💾 Árbol Bayesiano guardado: {path}")

    # ──────────────────────────────────────────────
    # Gráfico de Radar comparativo
    # ──────────────────────────────────────────────
    def graficar_radar_comparativo(self, df_particiones):
        pares = [
            ("50",  "Best_50",     "Worst_50"),
            ("25",  "Best_25_1",   "Worst_25_2"),
            ("12.5","Best_12.5_1", "Worst_12.5_4"),
        ]

        for nivel, n_best, n_worst in pares:
            if n_best not in df_particiones or n_worst not in df_particiones:
                continue

            df_b = df_particiones[n_best]["df"]  if isinstance(df_particiones[n_best], dict) else df_particiones[n_best]
            df_w = df_particiones[n_worst]["df"] if isinstance(df_particiones[n_worst], dict) else df_particiones[n_worst]

            # Usar las columnas de análisis (sin objetivo)
            vars_radar = [c for c in df_b.columns if c != self.col_objetivo]
            if len(vars_radar) < 3:
                continue

            disc_b = self.discretizar_dataframe(df_b, vars_radar)
            disc_w = self.discretizar_dataframe(df_w, vars_radar)
            vars_disponibles = [v for v in vars_radar if v in disc_b.columns and v in disc_w.columns]

            if len(vars_disponibles) < 3:
                continue

            means_b = [disc_b[v].mean() for v in vars_disponibles]
            means_w = [disc_w[v].mean() for v in vars_disponibles]

            angles  = np.linspace(0, 2 * np.pi, len(vars_disponibles), endpoint=False).tolist()
            means_b = means_b + means_b[:1]
            means_w = means_w + means_w[:1]
            angles  = angles  + angles[:1]

            fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
            ax.plot(angles, means_b, color="#1E88E5", linewidth=2.5, label=f"BEST ({n_best})")
            ax.fill(angles, means_b, color="#1E88E5", alpha=0.25)
            ax.plot(angles, means_w, color="#E53935", linewidth=2.5, label=f"WORST ({n_worst})")
            ax.fill(angles, means_w, color="#E53935", alpha=0.25)

            labels_full = [v[:12] + "…" if len(v) > 12 else v for v in vars_disponibles]
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels_full, fontsize=8, fontweight="bold")
            ax.set_ylim(0, 1.0)
            ax.set_title(f"Radar — Nivel {nivel}%\nPerfiles: Best vs Worst",
                         fontsize=12, fontweight="bold", pad=20)
            ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1.1), fontsize=9)

            dir_g = os.path.join(self.dir_base, f"nivel_{nivel}", "graficos")
            os.makedirs(dir_g, exist_ok=True)
            path  = os.path.join(dir_g, f"radar_comparativo_{nivel}.png")
            plt.savefig(path, dpi=150, bbox_inches="tight")
            plt.close()
            print(f"      💾 Radar guardado: {path}")

    # ──────────────────────────────────────────────
    # Ejecución completa
    # ──────────────────────────────────────────────
    def ejecutar_paso(self, df_limpio, particiones):
        self.arboles = {}

        print("\n   🌳 Construyendo Árbol Bayesiano completo (dataset limpio)...")
        self.construir_arbol_bayesiano(df_limpio, "Completo", nivel="global")

        for nombre, info in particiones.items():
            nivel    = info["nivel"]
            ruta_csv = info["ruta_csv"]
            df_part  = pd.read_csv(ruta_csv)
            print(f"   🌳 Árbol Bayesiano para {nombre}...")
            self.construir_arbol_bayesiano(df_part, nombre, nivel=nivel)

        print("\n   🕸️ Generando gráficos de Radar...")
        self.graficar_radar_comparativo(particiones)

        return self.arboles
