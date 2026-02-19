const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const dataset = process.argv[2];
const targetScript = process.argv[3];

if (!dataset || !targetScript) {
    console.error("Uso: node obfuscate.js <dataset> <script>");
    process.exit(1);
}

const INPUT_DIR = path.resolve(__dirname, "../datasets/original", dataset);
const OUTPUT_DIR = path.resolve(__dirname, "../datasets/obfuscation", dataset);

const OBFUSCATOR_OPTIONS = [
    "--compact true",
    "--control-flow-flattening true",
    "--control-flow-flattening-threshold 0.75",
    "--dead-code-injection true",
    "--dead-code-injection-threshold 0.4",
    "--string-array true",
    "--string-array-encoding base64"
].join(" ");


function getScripts() {
    return fs.readdirSync(INPUT_DIR).filter(f => f.endsWith(".js"));
}

function obfuscate(script) {
    const inputPath = path.join(INPUT_DIR, script);
    const outputPath = path.join(OUTPUT_DIR, script)
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    const start = Date.now();
    execSync(
        `npx javascript-obfuscator "${inputPath}" --output "${outputPath}" ${OBFUSCATOR_OPTIONS}`,
        { stdio: ["ignore", "ignore", "inherit"] }
    );
    return Number(((Date.now() - start) / 1000).toFixed(2)); 
}

function main() {
    const scripts = getScripts();
    let targetTime = null;
    for (const script of scripts) {
        const time = obfuscate(script);
        if (script === targetScript) {
            targetTime = time;
        }
    }
    if (targetTime === null) {
        console.error("Script objetivo no encontrado en el dataset");
        process.exit(1);
    }
    console.log(targetTime);
}

main();
