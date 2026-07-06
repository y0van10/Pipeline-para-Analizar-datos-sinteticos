"""
=============================================================
  PASO 4: CONSTRUCCIÓN DE TOPOLOGÍAS DE RED (MST)
=============================================================
Para cada matriz NCD (10×10 entre variables):

1. Crea un grafo completo ponderado con NetworkX
   - 10 nodos = 10 variables (X1 a X10)
   - Aristas = distancia NCD entre cada par
2. Extrae el Minimum Spanning Tree (MST)
   - Conecta todas las variables con el mínimo costo
3. Calcula el grado ponderado de cada variable
   - Suma de pesos NCD de las aristas conectadas
   - Un grado ponderado ALTO = variable muy conectada/central
   - Un grado ponderado BAJO = variable periférica

El MST revela la ESTRUCTURA de relaciones entre variables.
Si la estructura cambia entre Best y Worst, las variables
que más cambian son las que más se asocian con el rendimiento.
=============================================================
"""

import os
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform

# ── CONFIGURACIÓN ──────────────────────────────────────────
VARIABLES_ANALISIS = [
    "X1_sexo", "X2_zona", "X3_ciclo", "X4_ingreso_familiar",
    "X5_trabaja", "X6_beca", "X7_educ_jefe", "X8_tam_familiar",
    "X9_asistencia", "X10_cursos_desaprobados"
]

ETIQUETAS = [f"X{k+1}" for k in range(10)]

NOMBRES_COMPLETOS = {
    "X1": "Sexo", "X2": "Zona", "X3": "Ciclo",
    "X4": "Ingreso", "X5": "Trabaja", "X6": "Beca",
    "X7": "Educ.Jefe", "X8": "Tam.Fam", "X9": "Asistencia",
    "X10": "Desaprobados"
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "graficos")
# ───────────────────────────────────────────────────────────


def construir_grafo_completo(df_matriz):
    """
    Crea un grafo completo ponderado a partir de la matriz NCD.
    Cada nodo es una variable, cada arista tiene peso = NCD.
    """
    G = nx.Graph()
    etiquetas = list(df_matriz.index)

    for i, var_i in enumerate(etiquetas):
        G.add_node(var_i)
        for j, var_j in enumerate(etiquetas):
            if i < j:
                peso = df_matriz.iloc[i, j]
                G.add_edge(var_i, var_j, weight=peso)

    return G


def extraer_mst(G):
    """
    Extrae el Minimum Spanning Tree (árbol de expansión mínima).
    Conecta todos los nodos con el mínimo peso total.
    """
    mst = nx.minimum_spanning_tree(G, weight="weight")
    return mst


def calcular_grado_ponderado(mst):
    """
    Calcula la suma de pesos de aristas conectadas a cada nodo.
    Esto representa cuán 'central' es cada variable en la red.
    """
    grados = {}
    for nodo in mst.nodes():
        peso_total = sum(
            mst[nodo][vecino]["weight"]
            for vecino in mst.neighbors(nodo)
        )
        grados[nodo] = round(peso_total, 6)
    return grados


def graficar_mst(mst, nombre, output_dir):
    """
    Genera un gráfico visual del MST con colores diferenciados
    para variables categóricas y numéricas.
    """
    fig, ax = plt.subplots(figsize=(12, 10))

    # Clasificar variables
    categoricas = {"X1", "X2", "X5", "X6", "X7"}
    numericas = {"X3", "X4", "X8", "X9", "X10"}

    # Colores por tipo de variable
    colores_nodo = []
    for nodo in mst.nodes():
        if nodo in categoricas:
            colores_nodo.append("#FF7043")  # naranja = categórica
        else:
            colores_nodo.append("#42A5F5")  # azul = numérica

    # Layout
    pos = nx.spring_layout(mst, seed=42, k=2.5)

    # Dibujar aristas con grosor proporcional al peso invertido
    pesos = [mst[u][v]["weight"] for u, v in mst.edges()]
    peso_max = max(pesos) if pesos else 1
    anchos = [3.0 * (1 - w / peso_max) + 0.5 for w in pesos]

    nx.draw_networkx_edges(mst, pos, ax=ax, width=anchos, alpha=0.6,
                           edge_color="#78909C")

    # Etiquetas de peso en aristas
    edge_labels = {(u, v): f"{mst[u][v]['weight']:.3f}" for u, v in mst.edges()}
    nx.draw_networkx_edge_labels(mst, pos, edge_labels=edge_labels,
                                 ax=ax, font_size=8, font_color="#546E7A")

    # Dibujar nodos
    nx.draw_networkx_nodes(mst, pos, ax=ax, node_size=1200,
                           node_color=colores_nodo, edgecolors="white",
                           linewidths=2.5)

    # Etiquetas de nodos con nombre completo
    labels = {n: f"{n}\n{NOMBRES_COMPLETOS.get(n, '')}" for n in mst.nodes()}
    nx.draw_networkx_labels(mst, pos, labels=labels, ax=ax,
                            font_size=8, font_weight="bold", font_color="white")

    # Leyenda
    parche_cat = mpatches.Patch(color="#FF7043", label="Categórica")
    parche_num = mpatches.Patch(color="#42A5F5", label="Numérica")
    ax.legend(handles=[parche_cat, parche_num], loc="upper left", fontsize=10)

    # Título
    tipo = "BEST (Alto rendimiento)" if "Best" in nombre else "WORST (Bajo rendimiento)"
    pct = nombre.split("_")[1]
    ax.set_title(f"Árbol de Expansión Mínima (MST) - {tipo}\n"
                 f"Partición: {pct}% | Variables X1-X10",
                 fontsize=13, fontweight="bold")
    ax.axis("off")

    plt.tight_layout()
    path = os.path.join(output_dir, f"mst_{nombre}.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path


def graficar_heatmap(df_matriz, nombre, output_dir):
    """Genera heatmap de la matriz NCD."""
    fig, ax = plt.subplots(figsize=(10, 8))
    datos = df_matriz.values
    etiquetas = list(df_matriz.index)

    im = ax.imshow(datos, cmap="YlOrRd", vmin=0, vmax=1)
    plt.colorbar(im, ax=ax, label="Distancia NCD (0=similar, 1=diferente)")

    ax.set_xticks(range(len(etiquetas)))
    ax.set_yticks(range(len(etiquetas)))

    etiq_completas = [f"{e}\n{NOMBRES_COMPLETOS.get(e, '')}" for e in etiquetas]
    ax.set_xticklabels(etiq_completas, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(etiq_completas, fontsize=8)

    # Anotar valores
    for i in range(len(etiquetas)):
        for j in range(len(etiquetas)):
            color_texto = "white" if datos[i, j] > 0.7 else "black"
            ax.text(j, i, f"{datos[i, j]:.3f}", ha="center", va="center",
                    fontsize=7, color=color_texto)

    tipo = "BEST" if "Best" in nombre else "WORST"
    pct = nombre.split("_")[1]
    ax.set_title(f"Matriz NCD - {tipo} ({pct}%)\nDistancias entre Variables X1-X10",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(output_dir, f"heatmap_{nombre}.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path


def ejecutar(matrices):
    """
    Punto de entrada del paso 4.
    Construye MST y calcula grados ponderados para cada partición.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    topologias = {}  # nombre -> {mst, grados, grafo}

    for nombre, df_matriz in matrices.items():
        print(f"\n   🔧 Construyendo topología para {nombre}...")

        # Grafo completo
        G = construir_grafo_completo(df_matriz)

        # MST
        mst = extraer_mst(G)
        peso_total = sum(mst[u][v]["weight"] for u, v in mst.edges())
        print(f"      Aristas MST: {mst.number_of_edges()}")
        print(f"      Peso total MST: {peso_total:.4f}")

        # Grado ponderado
        grados = calcular_grado_ponderado(mst)
        var_max = max(grados, key=grados.get)
        var_min = min(grados, key=grados.get)
        print(f"      Variable más central: {var_max} ({NOMBRES_COMPLETOS.get(var_max, '')}) = {grados[var_max]:.4f}")
        print(f"      Variable más periférica: {var_min} ({NOMBRES_COMPLETOS.get(var_min, '')}) = {grados[var_min]:.4f}")

        # Guardar gráficos
        path_mst = graficar_mst(mst, nombre, OUTPUT_DIR)
        print(f"      💾 MST: {os.path.basename(path_mst)}")

        path_heat = graficar_heatmap(df_matriz, nombre, OUTPUT_DIR)
        print(f"      💾 Heatmap: {os.path.basename(path_heat)}")

        path_dendro = graficar_dendrograma(df_matriz, nombre, OUTPUT_DIR)
        print(f"      💾 Dendrograma: {os.path.basename(path_dendro)}")

        topologias[nombre] = {
            "mst": mst,
            "grados": grados,
            "grafo_completo": G,
            "peso_total_mst": peso_total
        }

    print(f"\n   ✅ {len(topologias)} topologías construidas")
    return topologias


def graficar_dendrograma(df_matriz, nombre, output_dir):
    """
    Genera un dendrograma jerárquico a partir de la matriz NCD.
    Muestra cómo se agrupan las variables por similitud.
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    etiquetas = list(df_matriz.index)
    etiq_completas = [f"{e} ({NOMBRES_COMPLETOS.get(e, '')})" for e in etiquetas]

    # Convertir matriz cuadrada a forma condensada para scipy
    # Asegurar que la diagonal sea 0 y la matriz sea simétrica
    mat = df_matriz.values.copy()
    np.fill_diagonal(mat, 0)
    dist_condensada = squareform(mat, checks=False)

    # Linkage jerárquico (Ward minimiza la varianza intra-cluster)
    Z = linkage(dist_condensada, method="ward")

    # Colores para las ramas
    color_umbral = 0.5 * max(Z[:, 2]) if len(Z) > 0 else 0

    # Dibujar dendrograma
    dn = dendrogram(
        Z,
        labels=etiq_completas,
        ax=ax,
        leaf_rotation=35,
        leaf_font_size=9,
        color_threshold=color_umbral,
        above_threshold_color="#78909C"
    )

    # Colorear etiquetas: categóricas en naranja, numéricas en azul
    categoricas_idx = {"X1", "X2", "X5", "X6", "X7"}
    xlbls = ax.get_xmajorticklabels()
    for lbl in xlbls:
        texto = lbl.get_text()
        var_id = texto.split(" ")[0]  # "X1 (Sexo)" → "X1"
        if var_id in categoricas_idx:
            lbl.set_color("#E65100")
        else:
            lbl.set_color("#1565C0")
        lbl.set_fontweight("bold")

    # Título y formato
    tipo = "BEST (Alto rendimiento)" if "Best" in nombre else "WORST (Bajo rendimiento)"
    pct = nombre.split("_")[1]
    ax.set_title(f"Dendrograma Jerárquico - {tipo}\n"
                 f"Partición: {pct}% | Agrupamiento de Variables X1-X10 por NCD",
                 fontsize=13, fontweight="bold")
    ax.set_ylabel("Distancia (Ward)", fontsize=11)
    ax.set_xlabel("Variables", fontsize=11)

    # Leyenda
    parche_cat = mpatches.Patch(color="#E65100", label="Categórica")
    parche_num = mpatches.Patch(color="#1565C0", label="Numérica")
    ax.legend(handles=[parche_cat, parche_num], loc="upper right", fontsize=10)

    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()
    path = os.path.join(output_dir, f"dendrograma_{nombre}.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path


def graficar_dendrograma_comparativo(matrices, output_dir):
    """
    Genera dendrogramas Best vs Worst lado a lado para cada nivel.
    """
    niveles = set()
    for nombre in matrices.keys():
        pct = nombre.split("_")[1]
        niveles.add(pct)

    for nivel in sorted(niveles, key=lambda x: float(x)):
        nombre_best = f"Best_{nivel}"
        nombre_worst = f"Worst_{nivel}"

        if nombre_best not in matrices or nombre_worst not in matrices:
            continue

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

        for ax, nombre, titulo_tipo, color_titulo in [
            (ax1, nombre_best, "BEST (Alto rendimiento)", "#1565C0"),
            (ax2, nombre_worst, "WORST (Bajo rendimiento)", "#C62828")
        ]:
            df_matriz = matrices[nombre]
            etiquetas = list(df_matriz.index)
            etiq_completas = [f"{e} ({NOMBRES_COMPLETOS.get(e, '')})" for e in etiquetas]

            mat = df_matriz.values.copy()
            np.fill_diagonal(mat, 0)
            dist_condensada = squareform(mat, checks=False)
            Z = linkage(dist_condensada, method="ward")
            color_umbral = 0.5 * max(Z[:, 2]) if len(Z) > 0 else 0

            dendrogram(
                Z,
                labels=etiq_completas,
                ax=ax,
                leaf_rotation=40,
                leaf_font_size=8,
                color_threshold=color_umbral,
                above_threshold_color="#78909C"
            )

            ax.set_title(f"{titulo_tipo}", fontsize=12, fontweight="bold",
                         color=color_titulo)
            ax.set_ylabel("Distancia (Ward)", fontsize=10)
            ax.grid(axis="y", alpha=0.3, linestyle="--")

            # Colorear etiquetas
            categoricas_idx = {"X1", "X2", "X5", "X6", "X7"}
            for lbl in ax.get_xmajorticklabels():
                var_id = lbl.get_text().split(" ")[0]
                lbl.set_color("#E65100" if var_id in categoricas_idx else "#1565C0")
                lbl.set_fontweight("bold")

        fig.suptitle(f"Comparación de Dendrogramas - Partición {nivel}%\n"
                     f"¿Cómo cambia el agrupamiento de variables entre Best y Worst?",
                     fontsize=14, fontweight="bold")
        plt.tight_layout()
        path = os.path.join(output_dir, f"dendrograma_comparativo_{nivel}.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"   💾 Dendrograma comparativo: dendrograma_comparativo_{nivel}.png")


if __name__ == "__main__":
    print("=" * 55)
    print("  PASO 4: TOPOLOGÍAS DE RED (MST)")
    print("=" * 55)
    print("  Ejecuta desde main.py para obtener las matrices.")
