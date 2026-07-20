const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ImageRun,
  PageBreak, ShadingType, VerticalAlign, Header, Footer, PageNumber,
  NumberFormat
} = require("docx");

const THIN_BORDER = { style: BorderStyle.SINGLE, size: 2, color: "000000" };
const CELL_BORDERS = { top: THIN_BORDER, bottom: THIN_BORDER, left: THIN_BORDER, right: THIN_BORDER };

function headerCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    borders: CELL_BORDERS,
    shading: { type: ShadingType.CLEAR, color: "auto", fill: "D9D9D9" },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, bold: true, size: 18, font: "Calibri" })]
    })]
  });
}

function bodyCell(text, width, opts = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    borders: CELL_BORDERS,
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      alignment: opts.center ? AlignmentType.CENTER : AlignmentType.LEFT,
      children: [new TextRun({ text: String(text), bold: !!opts.bold, size: 18, font: "Calibri" })]
    })]
  });
}

function makeTable(headers, rows, colWidthsDxa) {
  const total = colWidthsDxa.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: colWidthsDxa,
    rows: [
      new TableRow({ tableHeader: true, children: headers.map((h, i) => headerCell(h, colWidthsDxa[i])) }),
      ...rows.map(r => new TableRow({ children: r.map((c, i) => bodyCell(c, colWidthsDxa[i], { center: i > 0 })) }))
    ]
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 300, after: 150 },
    children: [new TextRun({ text, bold: true, size: 26, font: "Calibri", color: "000000" })]
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 250, after: 120 },
    children: [new TextRun({ text, bold: true, size: 23, font: "Calibri", color: "000000" })]
  });
}
function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, size: 21, font: "Calibri", color: "000000" })]
  });
}
function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 150, line: 276 },
    alignment: opts.justify ? AlignmentType.JUSTIFIED : AlignmentType.LEFT,
    children: Array.isArray(text) ? text : [new TextRun({ text, size: 21, font: "Calibri" })]
  });
}
function bullet(text) {
  return new Paragraph({
    bullet: { level: 0 },
    spacing: { after: 80 },
    children: [new TextRun({ text, size: 21, font: "Calibri" })]
  });
}
function numbered(text) {
  return new Paragraph({
    numbering: { reference: "main-numbering", level: 0 },
    spacing: { after: 80 },
    children: [new TextRun({ text, size: 21, font: "Calibri" })]
  });
}
function code(lines) {
  return new Paragraph({
    spacing: { before: 100, after: 150 },
    shading: { type: ShadingType.CLEAR, color: "auto", fill: "F2F2F2" },
    border: { top: THIN_BORDER, bottom: THIN_BORDER, left: THIN_BORDER, right: THIN_BORDER },
    children: lines.map((l, idx) => new TextRun({ text: l, font: "Consolas", size: 18, break: idx === 0 ? 0 : 1 }))
  });
}

const logoBuffer = fs.readFileSync("logo.png");

const bestNames = { X1: "Sexo", X2: "Zona geográfica", X3: "Ciclo académico", X4: "Ingreso familiar", X5: "Trabaja", X6: "Beca", X7: "Educación del jefe de familia", X8: "Tamaño familiar", X9: "Asistencia (%)", X10: "Cursos desaprobados", X11: "Promedio final" };

const varTableRows = Object.entries(bestNames).map(([k, v]) => [k, v, (k === "X1" || k === "X2" || k === "X5" || k === "X6" || k === "X7") ? "Categórica" : (k === "X11" ? "Numérica (clasificación)" : "Numérica")]);

const partRows = [
  ["12.5%", "8 bloques continuos (Best_12.5_1 a 4, Worst_12.5_1 a 4)", "results/nivel_12.5/tablas/"],
  ["25%", "4 cuartiles continuos (Best_25_1, Best_25_2, Worst_25_1, Worst_25_2)", "results/nivel_25/tablas/"],
  ["50%", "2 bloques (Best_50, Worst_50)", "results/nivel_50/tablas/"]
];

function ncdMatrixTable(matrix) {
  const headers = ["Var", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "X10"];
  const colW = [700, 860,860,860,860,860,860,860,860,860,860];
  return makeTable(headers, matrix, colW);
}

const M_BEST_125 = [
["X1","0.0000","0.9361","1.0000","1.0000","0.9574","0.9985","0.9698","1.0000","1.0000","1.0000"],
["X2","0.9361","0.0000","1.0000","1.0000","0.9422","0.9621","0.9669","1.0000","1.0000","1.0000"],
["X3","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","0.9295","0.9977","1.0000"],
["X4","1.0000","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000"],
["X5","0.9574","0.9422","1.0000","1.0000","0.0000","0.8837","0.9740","1.0000","1.0000","0.9777"],
["X6","0.9985","0.9621","1.0000","1.0000","0.8837","0.0000","0.9902","1.0000","1.0000","0.9983"],
["X7","0.9698","0.9669","1.0000","1.0000","0.9740","0.9902","0.0000","1.0000","1.0000","1.0000"],
["X8","1.0000","1.0000","0.9295","1.0000","1.0000","1.0000","1.0000","0.0000","0.9980","1.0000"],
["X9","1.0000","1.0000","0.9977","1.0000","1.0000","1.0000","1.0000","0.9980","0.0000","1.0000"],
["X10","1.0000","1.0000","1.0000","1.0000","0.9777","0.9983","1.0000","1.0000","1.0000","0.0000"]
];
const M_BEST_25 = [
["X1","0.0000","0.9745","1.0000","1.0000","0.9915","1.0000","0.9936","1.0000","1.0000","1.0000"],
["X2","0.9745","0.0000","1.0000","1.0000","0.9772","0.9952","0.9831","1.0000","1.0000","1.0000"],
["X3","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","0.9452","1.0000","1.0000"],
["X4","1.0000","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000"],
["X5","0.9915","0.9772","1.0000","1.0000","0.0000","0.8993","0.9903","1.0000","1.0000","1.0000"],
["X6","1.0000","0.9952","1.0000","1.0000","0.8993","0.0000","1.0000","1.0000","1.0000","1.0000"],
["X7","0.9936","0.9831","1.0000","1.0000","0.9903","1.0000","0.0000","1.0000","1.0000","1.0000"],
["X8","1.0000","1.0000","0.9452","1.0000","1.0000","1.0000","1.0000","0.0000","1.0000","1.0000"],
["X9","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","0.0000","1.0000"],
["X10","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","0.0000"]
];
const M_BEST_50 = [
["X1","0.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000"],
["X2","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","0.9936","1.0000","1.0000","1.0000"],
["X3","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","0.9532","1.0000","1.0000"],
["X4","1.0000","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000"],
["X5","1.0000","1.0000","1.0000","1.0000","0.0000","0.9167","1.0000","1.0000","1.0000","1.0000"],
["X6","1.0000","1.0000","1.0000","1.0000","0.9167","0.0000","1.0000","1.0000","1.0000","1.0000"],
["X7","1.0000","0.9936","1.0000","1.0000","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000"],
["X8","1.0000","1.0000","0.9532","1.0000","1.0000","1.0000","1.0000","0.0000","1.0000","1.0000"],
["X9","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","0.0000","1.0000"],
["X10","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","0.0000"]
];
const M_WORST_125 = [
["X1","0.0000","0.9436","1.0000","1.0000","0.9588","0.9726","0.9777","1.0000","1.0000","1.0000"],
["X2","0.9436","0.0000","1.0000","1.0000","0.8973","0.9245","0.9769","1.0000","1.0000","1.0000"],
["X3","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","0.9296","0.9981","0.9826"],
["X4","1.0000","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000"],
["X5","0.9588","0.8973","1.0000","1.0000","0.0000","0.8598","0.9753","1.0000","1.0000","1.0000"],
["X6","0.9726","0.9245","1.0000","1.0000","0.8598","0.0000","0.9713","1.0000","1.0000","1.0000"],
["X7","0.9777","0.9769","1.0000","1.0000","0.9753","0.9713","0.0000","1.0000","1.0000","1.0000"],
["X8","1.0000","1.0000","0.9296","1.0000","1.0000","1.0000","1.0000","0.0000","0.9965","1.0000"],
["X9","1.0000","1.0000","0.9981","1.0000","1.0000","1.0000","1.0000","0.9965","0.0000","1.0000"],
["X10","1.0000","1.0000","0.9826","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","0.0000"]
];
const M_WORST_25 = [
["X1","0.0000","0.9722","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000"],
["X2","0.9722","0.0000","1.0000","1.0000","0.9696","0.9785","0.9949","1.0000","1.0000","1.0000"],
["X3","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","0.9474","1.0000","1.0000"],
["X4","1.0000","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000"],
["X5","1.0000","0.9696","1.0000","1.0000","0.0000","0.9206","0.9957","1.0000","1.0000","1.0000"],
["X6","1.0000","0.9785","1.0000","1.0000","0.9206","0.0000","0.9914","1.0000","1.0000","1.0000"],
["X7","1.0000","0.9949","1.0000","1.0000","0.9957","0.9914","0.0000","1.0000","1.0000","1.0000"],
["X8","1.0000","1.0000","0.9474","1.0000","1.0000","1.0000","1.0000","0.0000","0.9999","1.0000"],
["X9","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","0.9999","0.0000","1.0000"],
["X10","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","0.0000"]
];
const M_WORST_50 = [
["X1","0.0000","0.9882","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000"],
["X2","0.9882","0.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000"],
["X3","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","0.9589","1.0000","1.0000"],
["X4","1.0000","1.0000","1.0000","0.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000"],
["X5","1.0000","1.0000","1.0000","1.0000","0.0000","0.9536","1.0000","1.0000","1.0000","1.0000"],
["X6","1.0000","1.0000","1.0000","1.0000","0.9536","0.0000","0.9993","1.0000","1.0000","1.0000"],
["X7","1.0000","1.0000","1.0000","1.0000","1.0000","0.9993","0.0000","1.0000","1.0000","1.0000"],
["X8","1.0000","1.0000","0.9589","1.0000","1.0000","1.0000","1.0000","0.0000","1.0000","1.0000"],
["X9","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","0.0000","1.0000"],
["X10","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","1.0000","0.0000"]
];

const comp125 = [
["X5","Trabaja","2.8037","1.7571","-1.0466","1.0466"],
["X2","Zona","2.8453","1.8409","-1.0044","1.0044"],
["X8","Tam.Fam","0.9295","1.9260","0.9965","0.9965"],
["X6","Beca","0.8837","1.8312","0.9474","0.9474"],
["X3","Ciclo","2.9272","2.9122","-0.0151","0.0151"],
["X1","Sexo","2.9361","2.9436","0.0075","0.0075"],
["X10","Desaprobados","0.9777","0.9826","0.0048","0.0048"],
["X7","Educ.Jefe","0.9669","0.9713","0.0044","0.0044"],
["X9","Asistencia","0.9977","0.9965","-0.0013","0.0013"],
["X4","Ingreso","1.0000","1.0000","0.0000","0.0000"]
];
const comp25 = [
["X6","Beca","0.8993","1.9121","1.0128","1.0128"],
["X1","Sexo","4.9745","3.9722","-1.0023","1.0023"],
["X8","Tam.Fam","0.9452","1.9473","1.0021","1.0021"],
["X2","Zona","2.9348","1.9418","-0.9930","0.9930"],
["X5","Trabaja","1.8765","1.8902","0.0138","0.0138"],
["X7","Educ.Jefe","0.9831","0.9914","0.0083","0.0083"],
["X3","Ciclo","1.9452","1.9474","0.0022","0.0022"],
["X9","Asistencia","1.0000","0.9999","-0.0001","0.0001"],
["X4","Ingreso","1.0000","1.0000","0.0000","0.0000"],
["X10","Desaprobados","1.0000","1.0000","0.0000","0.0000"]
];
const comp50 = [
["X6","Beca","0.9167","1.9530","1.0362","1.0362"],
["X2","Zona","1.9936","0.9882","-1.0054","1.0054"],
["X5","Trabaja","1.9167","1.9536","0.0369","0.0369"],
["X1","Sexo","6.0000","5.9882","-0.0118","0.0118"],
["X7","Educ.Jefe","0.9936","0.9993","0.0057","0.0057"],
["X3","Ciclo","1.9532","1.9589","0.0057","0.0057"],
["X8","Tam.Fam","0.9532","0.9589","0.0057","0.0057"],
["X4","Ingreso","1.0000","1.0000","0.0000","0.0000"],
["X9","Asistencia","1.0000","1.0000","0.0000","0.0000"],
["X10","Desaprobados","1.0000","1.0000","0.0000","0.0000"]
];

function compTable(rows) {
  return makeTable(
    ["Variable", "Nombre", "Grado_Best", "Grado_Worst", "Diferencia_D", "Abs_Diferencia"],
    rows,
    [1100, 1800, 1500, 1500, 1500, 1500]
  );
}

const children = [];

children.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [ new ImageRun({ type: "png", data: logoBuffer, transformation: { width: 110, height: 119 } }) ]
  }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [new TextRun({ text: "UNIVERSIDAD NACIONAL DEL ALTIPLANO - PUNO", bold: true, size: 26, font: "Calibri" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: [new TextRun({ text: "Facultad de Ingeniería de Sistemas", size: 22, font: "Calibri" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 200 }, children: [new TextRun({ text: "INFORME", bold: true, size: 36, font: "Calibri" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 }, children: [new TextRun({ text: "Análisis de Comportamiento Académico con NCD/Gzip y Redes Bayesianas", bold: true, size: 28, font: "Calibri" })] }),
  new Paragraph({ spacing: { before: 800, after: 80 }, children: [new TextRun({ text: "Estudiante: ", bold: true, size: 22, font: "Calibri" }), new TextRun({ text: "Jhoel Yovani Ticona Erquinigo", size: 22, font: "Calibri" })] }),
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Curso: ", bold: true, size: 22, font: "Calibri" }), new TextRun({ text: "Ciberseguridad - 9no Semestre", size: 22, font: "Calibri" })] }),
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Docente: ", bold: true, size: 22, font: "Calibri" }), new TextRun({ text: "Juárez Ruelas José Luis", size: 22, font: "Calibri" })] }),
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Fecha: ", bold: true, size: 22, font: "Calibri" }), new TextRun({ text: "20 de julio de 2026", size: 22, font: "Calibri" })] }),
  new Paragraph({ children: [new PageBreak()] })
);

children.push(h1("1. Introducción"));
children.push(p("El presente informe documenta el experimento de análisis de patrones académicos utilizando la métrica Normalized Compression Distance (NCD) con compresión Gzip, particionamiento jerárquico por bloques y Árboles Bayesianos Probabilísticos.", { justify: true }));

children.push(h1("2. Objetivo"));
children.push(p("Aplicar un pipeline completo de análisis basado en NCD/Gzip para:", { justify: true }));
children.push(numbered("Dividir a los estudiantes según su rendimiento académico (X11 - Promedio Final) en bloques contiguos (50%, 25% y 12.5%)."));
children.push(numbered("Calcular distancias NCD entre variables explicativas (X1-X10) leyendo archivos CSV desde disco."));
children.push(numbered("Construir topologías de red (MST), Heatmaps y Dendrogramas por nivel."));
children.push(numbered("Construir Árboles Bayesianos dirigidos basados en la probabilidad conjunta máxima."));
children.push(numbered("Comparar las redes Best vs Worst para identificar qué variables cambian más."));

children.push(h1("3. Descripción del Dataset"));
children.push(makeTable(["Característica", "Valor"], [
  ["Total de estudiantes", "18000"],
  ["Variables explicativas", "X1 a X10 (10 variables)"],
  ["Variable objetivo", "X11 - Promedio Final"],
  ["Bloques generados", "14 archivos CSV en results/"]
], [5500, 3000]));

function addImageIfExists(filePath, titleText, w = 450, h = 300) {
  if (fs.existsSync(filePath)) {
    const buf = fs.readFileSync(filePath);
    children.push(h3(titleText));
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 200 },
      children: [new ImageRun({ type: "png", data: buf, transformation: { width: w, height: h } })]
    }));
  }
}

children.push(h1("4. Gráficos y Visualizaciones"));

children.push(h2("4.1 Redes Bayesianas Dirigidas"));
addImageIfExists("results/global/arbol_bayesiano_Completo.png", "Árbol Bayesiano Dirigido - Dataset Completo");
addImageIfExists("results/nivel_50/graficos/arbol_bayesiano_Best_50.png", "Árbol Bayesiano - Best 50%");
addImageIfExists("results/nivel_50/graficos/arbol_bayesiano_Worst_50.png", "Árbol Bayesiano - Worst 50%");

children.push(h2("4.2 Gráficos de Radar (Telaraña) Comparativos"));
addImageIfExists("results/nivel_50/graficos/radar_comparativo_50.png", "Perfil Radar - Nivel 50%");
addImageIfExists("results/nivel_25/graficos/radar_comparativo_25.png", "Perfil Radar - Nivel 25%");
addImageIfExists("results/nivel_12.5/graficos/radar_comparativo_12.5.png", "Perfil Radar - Nivel 12.5%");

children.push(h2("4.3 Comparaciones Topológicas"));
addImageIfExists("results/global/resumen_comparacion_global.png", "Resumen Global de Diferencias Topológicas");

children.push(h1("5. Conclusiones"));
children.push(numbered("El pipeline en POO ejecuta los 7 pasos procesando archivos CSV independientes por cada nivel."));
children.push(numbered("Los Árboles Bayesianos dirigen adecuadamente las aristas utilizando probabilidades condicionales, resaltando el rendimiento (X11) como nodo central."));
children.push(numbered("Los gráficos de Radar confirman visualmente las desviaciones socioeconómicas y académicas entre estudiantes de alto y bajo rendimiento."));

const doc = new Document({
  numbering: {
    config: [{
      reference: "main-numbering",
      levels: [{ level: 0, format: NumberFormat.DECIMAL, text: "%1.", alignment: AlignmentType.START }]
    }]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [ new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [ new TextRun({ text: "UNA Puno - Ciberseguridad", size: 16, font: "Calibri", color: "666666" }) ]
        }) ]
      })
    },
    footers: {
      default: new Footer({
        children: [ new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Página ", size: 16, font: "Calibri" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 16, font: "Calibri" }),
            new TextRun({ text: " de ", size: 16, font: "Calibri" }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, font: "Calibri" }),
          ]
        }) ]
      })
    },
    children
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("informe/Informe_NCD_Gzip_Ciberseguridad.docx", buf);
  console.log("Word docx successfully generated at informe/Informe_NCD_Gzip_Ciberseguridad.docx");
});
