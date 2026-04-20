const esprima = require("esprima");
const fs = require("fs");

function extractNodeTypes(node, types = []) {
  if (!node || typeof node !== "object") return types;
  if (node.type) types.push(node.type);
  for (const key of Object.keys(node)) {
    const child = node[key];
    if (Array.isArray(child)) {
      child.forEach((c) => extractNodeTypes(c, types));
    } else if (child && typeof child === "object") {
      extractNodeTypes(child, types);
    }
  }
  return types;
}

function countFreq(arr) {
  return arr.reduce((acc, val) => {
    acc[val] = (acc[val] || 0) + 1;
    return acc;
  }, {});
}

function cosineSimilarity(freqA, freqB) {
  const allKeys = new Set([...Object.keys(freqA), ...Object.keys(freqB)]);
  let dot = 0, magA = 0, magB = 0;
  for (const k of allKeys) {
    const a = freqA[k] || 0;
    const b = freqB[k] || 0;
    dot += a * b;
    magA += a * a;
    magB += b * b;
  }
  if (magA === 0 || magB === 0) return 0;
  return dot / (Math.sqrt(magA) * Math.sqrt(magB));
}

function parseCode(code) {
  try {
    return esprima.parseScript(code, { tolerant: true });
  } catch (e) {
    try {
      return esprima.parseModule(code, { tolerant: true });
    } catch (e2) {
      return null;
    }
  }
}

const [, , fileA, fileB] = process.argv;

if (!fileA || !fileB) {
  console.error(JSON.stringify({ error: "Uso: node ast_similarity.js <fileA> <fileB>" }));
  process.exit(1);
}

const codeA = fs.readFileSync(fileA, "utf-8");
const codeB = fs.readFileSync(fileB, "utf-8");

const astA = parseCode(codeA);
const astB = parseCode(codeB);

if (!astA || !astB) {
  console.log(JSON.stringify({
    score: 0.0,
    parse_error: !astA ? "fileA" : "fileB",
    nodes_a: 0,
    nodes_b: 0,
  }));
  process.exit(0);
}

const typesA = extractNodeTypes(astA);
const typesB = extractNodeTypes(astB);

const freqA = countFreq(typesA);
const freqB = countFreq(typesB);

const score = cosineSimilarity(freqA, freqB);

console.log(JSON.stringify({
  score: parseFloat(score.toFixed(4)),
  nodes_a: typesA.length,
  nodes_b: typesB.length,
  parse_error: null,
}));
