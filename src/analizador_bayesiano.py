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
    Clase encargada de construir:
    1. Redes Bayesianas Completas (Todos contra Todos dirigidos).
    2. Árboles Bayesianos MST (Red de Máxima Expansión Mínima).
    basados en la probabilidad conjunta y la Jerarquía Causal Transitiva.
    """
    def __init__(self, dir_base="results", umbral=0.25, col_objetivo=None):
        self.dir_base     = os.path.normpath(dir_base)
        self.umbral       = umbral
        self.col_objetivo = col_objetivo
        self.arboles      = {}

    def discretizar_columna(self, serie):
        serie = serie.copy()
        numerica = pd.to_numeric(serie, errors="coerce")
        if numerica.notna().mean() > 0.7:
            mediana = numerica.median()
            return (numerica >= mediana).astype(int).fillna(0)

        unicos = serie.dropna().unique()
        if len(unicos) <= 2:
            ordenados = sorted(unicos, key=lambda x: str(x).lower())
            mapeo = {val: i for i, val in enumerate(ordenados)}
            return serie.map(mapeo).fillna(0).astype(int)

        moda = serie.mode()[0] if not serie.mode().empty else unicos[0]
        return (serie == moda).astype(int)

    def discretizar_dataframe(self, df, columnas_vars):
        df_disc = pd.DataFrame(index=df.index)
        for col in columnas_vars:
            if col in df.columns:
                df_disc[col] = self.discretizar_columna(df[col])

        if self.col_objetivo and self.col_objetivo in df.columns:
            mediana_obj = pd.to_numeric(df[self.col_objetivo], errors="coerce").median()
            df_disc[self.col_objetivo] = (
                pd.to_numeric(df[self.col_objetivo], errors="coerce") >= mediana_obj
            ).astype(int).fillna(0)

        return df_disc

    def inferir_nivel_causal(self, df, columnas_vars):
        """
        Determina la Jerarquía Causal Transitiva de las variables basándose en
        su nivel de correlación lineal/punto-biserial con la variable objetivo:
          - Nivel 2: La variable objetivo (col_objetivo), que es el resultado final.
          - Nivel 1: Variables intermediarias con alta correlación (|r| > 0.2) con el objetivo.
          - Nivel 0: Variables antecedentes con baja correlación (|r| <= 0.2) con el objetivo.
        Esta jerarquía previene ciclos bidireccionales en el grafo y orienta las flechas
        desde los niveles más bajos hacia los más altos (Causalidad de abajo hacia arriba).
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
                    col_num = self.discretizar_columna(df[col]).astype(float)
                else:
                    col_num = col_num.fillna(col_num.median())
                r = abs(col_num.corr(obj_num))
                niveles[col] = 1 if r > 0.2 else 0
            except Exception:
                niveles[col] = 0

        if self.col_objetivo:
            niveles[self.col_objetivo] = 2

        return niveles

    def _orientar_arista(self, u, v, max_prob, max_state, df_disc, nivel_causal, n):
        """
        Orienta de manera dirigida la arista entre los nodos u y v siguiendo dos criterios:
        1. Jerarquía Causal: El nodo en un nivel inferior (antecedente) siempre apunta
           al nodo en el nivel superior (ejemplo: Nivel 0 -> Nivel 1 -> Nivel 2).
        2. Criterio de Entropía Local: Si están en el mismo nivel causal, la flecha se orienta
           desde el estado menos probable (mayor especificidad/sorpresa) hacia el más probable.
        """
        p_u = (df_disc[u] == max_state[0]).sum() / n if u in df_disc else 0.5
        p_v = (df_disc[v] == max_state[1]).sum() / n if v in df_disc else 0.5

        lvl_u = nivel_causal.get(u, 0)
        lvl_v = nivel_causal.get(v, 0)

        if lvl_u < lvl_v:
            return u, v, max_prob, max_state
        elif lvl_v < lvl_u:
            return v, u, max_prob, (max_state[1], max_state[0])
        else:
            if p_u <= p_v:
                return u, v, max_prob, max_state
            else:
                return v, u, max_prob, (max_state[1], max_state[0])

    def construir_arbol_bayesiano(self, df_part, nombre, nivel="global"):
        """
        Construye tanto la Red Bayesiana Completa como el Árbol Bayesiano (MST).
        Calcula la distribución de probabilidad conjunta para cada par de variables
        y extrae el estado conjunto de mayor probabilidad para medir su similitud.
        """
        columnas_vars = [c for c in df_part.columns if c != self.col_objetivo]
        df_disc = self.discretizar_dataframe(df_part, columnas_vars)
        variables = list(df_disc.columns)
        n = len(df_disc)

        if n < 5 or len(variables) < 2:
            print(f"      ⚠️  {nombre}: datos insuficientes ({n} filas, {len(variables)} vars)")
            return None

        nivel_causal = self.inferir_nivel_causal(df_part, variables)

        G_completo = nx.Graph()
        for var in variables:
            G_completo.add_node(var)

        datos_aristas = {}
        for var_i, var_j in combinations(variables, 2):
            if var_i not in df_disc.columns or var_j not in df_disc.columns:
                continue
            
            # Tabla de contingencia cruzada para contar frecuencias conjuntas de X_i y X_j
            counts = df_disc.groupby([var_i, var_j]).size().unstack(fill_value=0)
            for val in [0, 1]:
                if val not in counts.index:   counts.loc[val] = 0
                if val not in counts.columns: counts[val] = 0
            counts = counts.loc[[0, 1], [0, 1]]
            probs  = counts / n # Distribución de probabilidad conjunta P(X_i, X_j)

            # Buscamos el estado conjunto con la mayor probabilidad (Moda de la probabilidad conjunta)
            max_prob, max_state = -1.0, None
            for a in [0, 1]:
                for b in [0, 1]:
                    p = probs.loc[a, b]
                    if p > max_prob:
                        max_prob, max_state = p, (a, b)

            # Usamos la disimilitud probabilística (1 - P_max) como el peso/distancia
            dist = 1.0 - max_prob
            G_completo.add_edge(var_i, var_j, weight=dist)
            datos_aristas[(var_i, var_j)] = (max_prob, max_state)

        # ─────────────────────────────────────────────
        # 1. RED COMPLETA (Todos contra Todos)
        # ─────────────────────────────────────────────
        red_completa = nx.DiGraph()
        for v in variables:
            red_completa.add_node(v)

        for (u, v), (max_prob, max_state) in datos_aristas.items():
            origen, destino, prob, st = self._orientar_arista(u, v, max_prob, max_state, df_disc, nivel_causal, n)
            red_completa.add_edge(origen, destino, weight=prob, state=st)

        # ─────────────────────────────────────────────
        # 2. ÁRBOLES BAYESIANOS (MST)
        # ─────────────────────────────────────────────
        mst_no_dirigido = nx.minimum_spanning_tree(G_completo, weight="weight")
        arbol_mst = nx.DiGraph()
        for v in variables:
            arbol_mst.add_node(v)

        for u, v in mst_no_dirigido.edges():
            llave = (u, v) if (u, v) in datos_aristas else (v, u)
            max_prob, max_state = datos_aristas[llave]
            origen, destino, prob, st = self._orientar_arista(llave[0], llave[1], max_prob, max_state, df_disc, nivel_causal, n)
            arbol_mst.add_edge(origen, destino, weight=prob, state=st)

        self.arboles[f"MST_{nombre}"] = arbol_mst
        self.arboles[f"Completa_{nombre}"] = red_completa

        # Graficar ambos
        self.graficar_red(arbol_mst, nombre, nivel, nivel_causal, es_completa=False)
        self.graficar_red(red_completa, nombre, nivel, nivel_causal, es_completa=True)

        return arbol_mst

    def graficar_red(self, red, nombre, nivel, nivel_causal, es_completa=False):
        n_nodos = len(red.nodes())
        fig_h   = max(11, n_nodos * 0.9)
        fig_w   = max(13, n_nodos * 1.1)
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))

        COLOR_RAIZ     = "#E65100"  # naranja: antecedentes (nivel 0)
        COLOR_INTERM   = "#1565C0"  # azul: intermediarios (nivel 1)
        COLOR_OBJETIVO = "#2E7D32"  # verde: resultado (nivel 2)

        colores_nodo  = []
        tamaños_nodo  = []
        for nodo in red.nodes():
            lvl = nivel_causal.get(nodo, 0)
            grado_total = red.in_degree(nodo) + red.out_degree(nodo)
            tamaños_nodo.append(1400 + grado_total * (100 if es_completa else 180))

            if lvl == 2:
                colores_nodo.append(COLOR_OBJETIVO)
            elif lvl == 1:
                colores_nodo.append(COLOR_INTERM)
            else:
                colores_nodo.append(COLOR_RAIZ)

        # Layout por niveles causales
        pos = {}
        grupos_nivel = {}
        for nodo in red.nodes():
            lvl = nivel_causal.get(nodo, 0)
            grupos_nivel.setdefault(lvl, []).append(nodo)

        max_lvl = max(grupos_nivel.keys()) if grupos_nivel else 0
        for lvl, nodos in grupos_nivel.items():
            y = max_lvl - lvl
            x_coords = np.linspace(-3.0, 3.0, len(nodos))
            for i, nodo in enumerate(sorted(nodos)):
                pos[nodo] = np.array([x_coords[i], y * 1.8])

        # Dibujar aristas
        pesos = [data["weight"] for _, _, data in red.edges(data=True)]
        p_min = min(pesos) if pesos else 0
        p_max = max(pesos) if pesos else 1

        if es_completa:
            # En la red completa, variar alpha y ancho por probabilidad para no atoturar
            anchos = [0.8 + 2.5 * ((w - p_min) / (p_max - p_min + 1e-6)) for w in pesos]
            alphas = [0.25 + 0.60 * ((w - p_min) / (p_max - p_min + 1e-6)) for w in pesos]

            for (u, v, data), w_val, a_val in zip(red.edges(data=True), anchos, alphas):
                nx.draw_networkx_edges(
                    red, pos, edgelist=[(u, v)], ax=ax,
                    arrows=True, arrowstyle="-|>", arrowsize=18,
                    edge_color="#C62828", width=w_val, alpha=a_val,
                    connectionstyle="arc3,rad=0.15",
                    min_target_margin=25, min_source_margin=25
                )
        else:
            # MST
            nx.draw_networkx_edges(
                red, pos, ax=ax,
                arrows=True, arrowstyle="-|>", arrowsize=28,
                edge_color="#C62828", width=2.8, alpha=0.85,
                connectionstyle="arc3,rad=0.12",
                min_target_margin=32, min_source_margin=32,
            )

        # Dibujar nodos
        nx.draw_networkx_nodes(
            red, pos, ax=ax, node_size=tamaños_nodo,
            node_color=colores_nodo, edgecolors="white", linewidths=2.5,
        )

        etiquetas = {n: (n[:15] + "…" if len(n) > 15 else n) for n in red.nodes()}
        nx.draw_networkx_labels(red, pos, labels=etiquetas, ax=ax,
                                font_size=8, font_weight="bold", font_color="white")

        # Dibujar etiquetas en aristas (solo top en completa si son muchas)
        etiquetas_aristas = {}
        umbral_label = np.percentile(pesos, 50) if es_completa and len(pesos) > 20 else 0.0
        for u, v, data in red.edges(data=True):
            if not es_completa or data["weight"] >= umbral_label:
                etiquetas_aristas[(u, v)] = f"P={data['weight']:.2f}"

        if etiquetas_aristas:
            nx.draw_networkx_edge_labels(red, pos, edge_labels=etiquetas_aristas,
                                         ax=ax, font_size=6 if es_completa else 7,
                                         font_color="#D32F2F", font_weight="bold")

        parche_raiz = mpatches.Patch(color=COLOR_RAIZ,     label="Antecedentes (baja corr. con objetivo)")
        parche_int  = mpatches.Patch(color=COLOR_INTERM,   label="Intermediarios (alta corr. con objetivo)")
        parche_tar  = mpatches.Patch(color=COLOR_OBJETIVO, label=f"Objetivo: {self.col_objetivo or 'resultado'}")
        ax.legend(handles=[parche_raiz, parche_int, parche_tar], loc="upper left", fontsize=9)

        tipo_str = "Red Bayesiana Completa (Todos contra Todos)" if es_completa else "Árbol Bayesiano (MST)"
        ax.set_title(f"{tipo_str} — {nombre}\n"
                     f"Flujo: Antecedentes ➔ Intermediarios ➔ {self.col_objetivo or 'Resultado'}",
                     fontsize=13, fontweight="bold")
        ax.axis("off")
        plt.tight_layout()

        dir_g = os.path.join(self.dir_base, "global") if nivel == "global" else os.path.join(self.dir_base, f"nivel_{nivel}", "graficos")
        os.makedirs(dir_g, exist_ok=True)

        nombre_archivo = f"red_bayesiana_completa_{nombre}.png" if es_completa else f"arbol_bayesiano_{nombre}.png"
        path = os.path.join(dir_g, nombre_archivo)
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"      💾 {tipo_str} guardado: {path}")

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

    def ejecutar_paso(self, df_limpio, particiones):
        self.arboles = {}

        print("\n   🌳 Construyendo Red Completa y Árbol MST (dataset completo)...")
        self.construir_arbol_bayesiano(df_limpio, "Completo", nivel="global")

        for nombre, info in particiones.items():
            nivel    = info["nivel"]
            ruta_csv = info["ruta_csv"]
            df_part  = pd.read_csv(ruta_csv)
            print(f"   🌳 Red Completa y Árbol MST para {nombre}...")
            self.construir_arbol_bayesiano(df_part, nombre, nivel=nivel)

        print("\n   🕸️ Generando gráficos de Radar...")
        self.graficar_radar_comparativo(particiones)

        return self.arboles
