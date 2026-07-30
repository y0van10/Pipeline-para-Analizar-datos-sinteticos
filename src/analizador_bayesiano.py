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
        """
        Grafica la red bayesiana causal con alta resolución (300 DPI) para permitir
        un zoom nítido (con lupa), letras más grandes, nodos más amplios y sin recortar
        los nombres de variables largas.
        """
        n_nodos = len(red.nodes())
        fig_h   = max(12, n_nodos * 1.0)
        fig_w   = max(14, n_nodos * 1.2)
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))

        COLOR_RAIZ     = "#E65100"  # naranja oscuro: antecedentes
        COLOR_INTERM   = "#1565C0"  # azul: intermediarios
        COLOR_OBJETIVO = "#2E7D32"  # verde oscuro: resultado objetivo

        colores_nodo  = []
        tamaños_nodo  = []
        for nodo in red.nodes():
            lvl = nivel_causal.get(nodo, 0)
            grado_total = red.in_degree(nodo) + red.out_degree(nodo)
            # Aumentamos el tamaño base de los nodos para alojar textos legibles
            tamaños_nodo.append(2600 + grado_total * (120 if es_completa else 200))

            if lvl == 2:
                colores_nodo.append(COLOR_OBJETIVO)
            elif lvl == 1:
                colores_nodo.append(COLOR_INTERM)
            else:
                colores_nodo.append(COLOR_RAIZ)

        # Disposición (layout) jerárquico por nivel causal
        pos = {}
        grupos_nivel = {}
        for nodo in red.nodes():
            lvl = nivel_causal.get(nodo, 0)
            grupos_nivel.setdefault(lvl, []).append(nodo)

        max_lvl = max(grupos_nivel.keys()) if grupos_nivel else 0
        for lvl, nodos in grupos_nivel.items():
            y = max_lvl - lvl
            x_coords = np.linspace(-3.5, 3.5, len(nodos))
            for i, nodo in enumerate(sorted(nodos)):
                pos[nodo] = np.array([x_coords[i], y * 2.0])

        # Dibujar aristas con opacidad y grosores adecuados
        pesos = [data["weight"] for _, _, data in red.edges(data=True)]
        p_min = min(pesos) if pesos else 0
        p_max = max(pesos) if pesos else 1

        if es_completa:
            anchos = [1.0 + 3.0 * ((w - p_min) / (p_max - p_min + 1e-6)) for w in pesos]
            alphas = [0.30 + 0.60 * ((w - p_min) / (p_max - p_min + 1e-6)) for w in pesos]

            for (u, v, data), w_val, a_val in zip(red.edges(data=True), anchos, alphas):
                nx.draw_networkx_edges(
                    red, pos, edgelist=[(u, v)], ax=ax,
                    arrows=True, arrowstyle="-|>", arrowsize=20,
                    edge_color="#C62828", width=w_val, alpha=a_val,
                    connectionstyle="arc3,rad=0.15",
                    min_target_margin=30, min_source_margin=30
                )
        else:
            # MST
            nx.draw_networkx_edges(
                red, pos, ax=ax,
                arrows=True, arrowstyle="-|>", arrowsize=32,
                edge_color="#C62828", width=3.5, alpha=0.85,
                connectionstyle="arc3,rad=0.12",
                min_target_margin=38, min_source_margin=38,
            )

        # Dibujar nodos en pantalla
        nx.draw_networkx_nodes(
            red, pos, ax=ax, node_size=tamaños_nodo,
            node_color=colores_nodo, edgecolors="white", linewidths=2.5,
        )

        # Mostrar etiquetas de nodos sin truncar tanto (hasta 30 caracteres para legibilidad total)
        etiquetas = {n: (n[:30] + "…" if len(n) > 30 else n) for n in red.nodes()}
        nx.draw_networkx_labels(red, pos, labels=etiquetas, ax=ax,
                                font_size=9, font_weight="bold", font_color="white")

        # Mostrar probabilidades en las aristas
        etiquetas_aristas = {}
        umbral_label = np.percentile(pesos, 50) if es_completa and len(pesos) > 20 else 0.0
        for u, v, data in red.edges(data=True):
            if not es_completa or data["weight"] >= umbral_label:
                etiquetas_aristas[(u, v)] = f"P={data['weight']:.2f}"

        if etiquetas_aristas:
            nx.draw_networkx_edge_labels(red, pos, edge_labels=etiquetas_aristas,
                                         ax=ax, font_size=8,
                                         font_color="#D32F2F", font_weight="bold")

        parche_raiz = mpatches.Patch(color=COLOR_RAIZ,     label="Antecedentes (baja corr. con objetivo)")
        parche_int  = mpatches.Patch(color=COLOR_INTERM,   label="Intermediarios (alta corr. con objetivo)")
        parche_tar  = mpatches.Patch(color=COLOR_OBJETIVO, label=f"Objetivo: {self.col_objetivo or 'resultado'}")
        ax.legend(handles=[parche_raiz, parche_int, parche_tar], loc="upper left", fontsize=10)

        tipo_str = "Red Bayesiana Completa (Todos contra Todos)" if es_completa else "Árbol Bayesiano (MST)"
        ax.set_title(f"{tipo_str} — {nombre}\n"
                     f"Flujo Causal: Antecedentes ➔ Intermediarios ➔ {self.col_objetivo or 'Resultado'}",
                     fontsize=14, fontweight="bold")
        ax.axis("off")
        plt.tight_layout()

        dir_g = os.path.join(self.dir_base, "global") if nivel == "global" else os.path.join(self.dir_base, f"nivel_{nivel}", "graficos")
        os.makedirs(dir_g, exist_ok=True)

        nombre_archivo = f"red_bayesiana_completa_{nombre}.png" if es_completa else f"arbol_bayesiano_{nombre}.png"
        path = os.path.join(dir_g, nombre_archivo)
        
        # Guardamos a 300 DPI para resolución nítida en pantallas y PDFs
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"      💾 {tipo_str} guardado a 300 DPI: {path}")

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

        # Nota: Los gráficos de radar (telaraña) han sido eliminados por requerimiento de diseño.
        return self.arboles


