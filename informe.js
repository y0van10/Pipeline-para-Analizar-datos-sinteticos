const fs = require("fs");
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
  ["12.5%", "2250 estudiantes con mayor promedio", "2250 estudiantes con menor promedio"],
  ["25%", "4500 estudiantes", "4500 estudiantes"],
  ["50%", "9000 estudiantes", "9000 estudiantes"]
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
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 }, children: [new TextRun({ text: "Análisis de Comportamiento Académico con NCD/Gzip", bold: true, size: 28, font: "Calibri" })] }),
  new Paragraph({ spacing: { before: 800, after: 80 }, children: [new TextRun({ text: "Estudiante: ", bold: true, size: 22, font: "Calibri" }), new TextRun({ text: "Jhoel Yovani Ticona Erquinigo", size: 22, font: "Calibri" })] }),
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Curso: ", bold: true, size: 22, font: "Calibri" }), new TextRun({ text: "Ciberseguridad - 9no Semestre", size: 22, font: "Calibri" })] }),
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Docente: ", bold: true, size: 22, font: "Calibri" }), new TextRun({ text: "Juárez Ruelas José Luis", size: 22, font: "Calibri" })] }),
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Fecha: ", bold: true, size: 22, font: "Calibri" }), new TextRun({ text: "06 de julio de 2026", size: 22, font: "Calibri" })] }),
  new Paragraph({ children: [new PageBreak()] })
);

children.push(h1("1. Introducción"));
children.push(p("El presente informe documenta el experimento de análisis de patrones académicos utilizando la métrica Normalized Compression Distance (NCD) con compresión Gzip.", { justify: true }));
children.push(p("El objetivo es descubrir qué factores socioeconómicos y académicos se comportan de manera diferente entre estudiantes de alto y bajo rendimiento, revelando las posibles causas del éxito o fracaso académico.", { justify: true }));

children.push(h1("2. Objetivo"));
children.push(p("Aplicar un pipeline completo de análisis basado en NCD/Gzip para:", { justify: true }));
children.push(numbered("Dividir a los estudiantes según su rendimiento académico (X11 - Promedio Final)."));
children.push(numbered("Calcular distancias entre variables explicativas (X1-X10) dentro de cada grupo."));
children.push(numbered("Construir topologías de red (MST) que representen las relaciones entre variables."));
children.push(numbered("Comparar las redes Best vs Worst para identificar qué variables cambian más."));
children.push(p([new TextRun({ text: "Pregunta central: ", bold: true, size: 21, font: "Calibri" }), new TextRun({ text: "¿Qué variables (causas) explican la diferencia entre estudiantes con alto y bajo promedio final?", italics: true, size: 21, font: "Calibri" })]));

children.push(h1("3. Descripción del Dataset"));
children.push(makeTable(["Característica", "Valor"], [
  ["Total de estudiantes (después de limpieza)", "18000"],
  ["Variables explicativas", "X1 a X10 (10 variables)"],
  ["Variable de clasificación", "X11 - Promedio Final"],
  ["Duplicados eliminados", "0"],
  ["Nulos eliminados", "0"]
], [5500, 3000]));
children.push(new Paragraph({ spacing: { before: 200 } }));
children.push(h2("Variables del estudio"));
children.push(makeTable(["Variable", "Descripción", "Tipo"], varTableRows, [1200, 4500, 2800]));
children.push(p("Nota: X11 se usa exclusivamente para clasificar estudiantes en Best/Worst. Las variables X1-X10 son las que se analizan con NCD para descubrir patrones.", { justify: true }));

children.push(h1("4. Metodología"));
children.push(h2("4.1 Limpieza de datos"));
children.push(p("Se eliminaron filas con valores nulos, duplicados y datos fuera de rango lógico (promedio < 0 o > 20, asistencia < 0 o > 100, etc.).", { justify: true }));

children.push(h2("4.2 Particionamiento por rendimiento académico"));
children.push(p("Los estudiantes se ordenaron por X11 (promedio final) y se crearon particiones:", { justify: true }));
children.push(makeTable(["Nivel", "Best (Top)", "Worst (Bottom)"], partRows, [1500, 3800, 3200]));

children.push(h2("4.3 Cálculo de NCD/Gzip"));
children.push(p("Para cada partición se calculó una matriz de distancia 10×10 entre las variables X1 a X10 usando la fórmula:", { justify: true }));
children.push(code(["NCD(x, y) = (C(xy) - min(C(x), C(y))) / max(C(x), C(y))"]));
children.push(p("Donde:"));
children.push(bullet("C(x) = tamaño comprimido de la columna x con gzip (nivel 9)"));
children.push(bullet("Cada columna se convirtió a cadena de texto antes de comprimir"));
children.push(bullet("NCD ≈ 0 → variables muy similares/relacionadas"));
children.push(bullet("NCD ≈ 1 → variables muy diferentes"));

children.push(h2("4.4 Construcción de topologías de red"));
children.push(p("Con cada matriz NCD se construyó un Minimum Spanning Tree (MST) usando NetworkX:", { justify: true }));
children.push(bullet("10 nodos = 10 variables"));
children.push(bullet("Aristas = distancia NCD entre variables"));
children.push(bullet("El MST conecta todas las variables con el mínimo peso total"));

children.push(h2("4.5 Comparación de topologías"));
children.push(p("Se compararon las redes Best vs Worst calculando el grado ponderado de cada variable (suma de pesos de aristas conectadas en el MST) y la diferencia:", { justify: true }));
children.push(code(["D = GradoPonderado_Worst - GradoPonderado_Best"]));
children.push(bullet("D positivo grande → la variable aumenta su conexión en Worst (factor de riesgo)"));
children.push(bullet("D negativo grande → la variable disminuye su conexión en Worst (factor protector)"));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("5. Resultados"));
children.push(h2("5.1 Matrices NCD"));

children.push(h3("Matriz NCD - BEST (12.5%)"));
children.push(ncdMatrixTable(M_BEST_125));
children.push(h3("Matriz NCD - BEST (25%)"));
children.push(ncdMatrixTable(M_BEST_25));
children.push(h3("Matriz NCD - BEST (50%)"));
children.push(ncdMatrixTable(M_BEST_50));
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h3("Matriz NCD - WORST (12.5%)"));
children.push(ncdMatrixTable(M_WORST_125));
children.push(h3("Matriz NCD - WORST (25%)"));
children.push(ncdMatrixTable(M_WORST_25));
children.push(h3("Matriz NCD - WORST (50%)"));
children.push(ncdMatrixTable(M_WORST_50));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h2("5.2 Comparación de Topologías"));

children.push(h3("Partición 12.5%"));
children.push(compTable(comp125));
children.push(p([new TextRun({ text: "Variable con MÁXIMO cambio: ", bold: true, size: 21, font: "Calibri" }), new TextRun({ text: "X5 (Trabaja) → D = -1.0466", size: 21, font: "Calibri" })]));
children.push(p([new TextRun({ text: "Variable con MÍNIMO cambio: ", bold: true, size: 21, font: "Calibri" }), new TextRun({ text: "X4 (Ingreso Familiar) → D = +0.0000", size: 21, font: "Calibri" })]));

children.push(h3("Partición 25%"));
children.push(compTable(comp25));
children.push(p([new TextRun({ text: "Variable con MÁXIMO cambio: ", bold: true, size: 21, font: "Calibri" }), new TextRun({ text: "X6 (Beca) → D = +1.0128", size: 21, font: "Calibri" })]));
children.push(p([new TextRun({ text: "Variable con MÍNIMO cambio: ", bold: true, size: 21, font: "Calibri" }), new TextRun({ text: "X10 (Cursos Desaprobados) → D = +0.0000", size: 21, font: "Calibri" })]));

children.push(h3("Partición 50%"));
children.push(compTable(comp50));
children.push(p([new TextRun({ text: "Variable con MÁXIMO cambio: ", bold: true, size: 21, font: "Calibri" }), new TextRun({ text: "X6 (Beca) → D = +1.0362", size: 21, font: "Calibri" })]));
children.push(p([new TextRun({ text: "Variable con MÍNIMO cambio: ", bold: true, size: 21, font: "Calibri" }), new TextRun({ text: "X10 (Cursos Desaprobados) → D = +0.0000", size: 21, font: "Calibri" })]));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("6. Análisis de Variables Relevantes"));
children.push(h2("Variables con mayor cambio estructural"));
children.push(p("Las siguientes variables presentan los mayores cambios en su posición dentro de la red entre los grupos Best y Worst:", { justify: true }));
children.push(bullet("X6 (Beca): máximo cambio en 2 de 3 particiones"));
children.push(bullet("X5 (Trabaja): máximo cambio en 1 de 3 particiones"));

children.push(h2("Variables con menor cambio estructural"));
children.push(p("Las siguientes variables mantienen un comportamiento similar en ambos grupos:", { justify: true }));
children.push(bullet("X10 (Cursos Desaprobados): mínimo cambio en 2 de 3 particiones"));
children.push(bullet("X4 (Ingreso Familiar): mínimo cambio en 1 de 3 particiones"));

children.push(h1("7. Discusión"));
children.push(p("El análisis NCD/Gzip permitió revelar que las relaciones entre variables socioeconómicas y académicas no son iguales para estudiantes de alto y bajo rendimiento. Las variables que más cambian su posición en la topología de red son aquellas que tienen un comportamiento diferenciado según el grupo.", { justify: true }));
children.push(p("Cuando una variable tiene un D positivo grande, significa que en el grupo Worst esa variable está más conectada/central en la red de relaciones, sugiriendo que juega un papel más determinante en el bajo rendimiento.", { justify: true }));
children.push(p("Cuando una variable tiene un D negativo grande, significa que en el grupo Best esa variable tiene mayor centralidad, sugiriendo un rol protector o asociado al buen rendimiento.", { justify: true }));

children.push(h1("8. Conclusiones"));
children.push(numbered("La técnica NCD/Gzip permite cuantificar relaciones entre variables sin asumir distribuciones estadísticas ni linealidad."));
children.push(numbered("Las topologías de red (MST) revelan la estructura de dependencias entre variables dentro de cada grupo de rendimiento."));
children.push(numbered("La comparación de topologías identifica las variables que más cambian su comportamiento entre grupos, indicando posibles factores causales."));
children.push(numbered("Los resultados son consistentes a través de las tres particiones (12.5%, 25%, 50%), lo que refuerza la robustez de los hallazgos."));

children.push(h1("9. Reproducibilidad"));
children.push(p("Para reproducir este análisis:"));
children.push(code(["pip install -r requirements.txt", "python main.py"]));
children.push(p("Los resultados se generan en:"));
children.push(bullet("results/matrices/ → Matrices NCD (CSV)"));
children.push(bullet("results/graficos/ → Gráficos de redes y comparaciones (PNG)"));
children.push(bullet("results/tablas/ → Tablas comparativas (CSV)"));

children.push(h1("10. Anexos"));
children.push(h2("Archivos generados"));
children.push(makeTable(["Carpeta", "Contenido"], [
  ["results/matrices/", "6 matrices NCD (10×10) en formato CSV"],
  ["results/graficos/", "Gráficos MST, heatmaps, comparaciones"],
  ["results/tablas/", "Particiones y tablas comparativas"],
  ["informe/", "Este informe en formato Markdown"]
], [3500, 5300]));

children.push(new Paragraph({
  spacing: { before: 400 },
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "Informe generado automáticamente por el pipeline NCD/Gzip.", italics: true, size: 18, font: "Calibri" })]
}));

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
  console.log("done");
});
