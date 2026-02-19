function generateMatrix(rows, cols, min = 0, max = 100) {
    const matrix = [];
    for (let i = 0; i < rows; i++) {
        const row = [];
        for (let j = 0; j < cols; j++) {
            row.push(Math.floor(Math.random() * (max - min + 1)) + min);
        }
        matrix.push(row);
    }
    return matrix;
}
function analyzeMatrix(matrix) {
    let total = 0;
    let count = 0;
    let max = -Infinity;
    let min = Infinity;
    for (const row of matrix) {
        for (const value of row) {
            total += value;
            count++;
            if (value > max) max = value;
            if (value < min) min = value;
        }
    }
    return {
        rows: matrix.length,
        cols: matrix[0].length,
        totalElements: count,
        sum: total,
        average: count > 0 ? total / count : 0,
        max: max,
        min: min
    };
}
function printMatrix(matrix) {
    for (const row of matrix) {
        console.log(row.join("\t"));
    }
}
function main() {
    const rows = 10;
    const cols = 10;
    const matrix = generateMatrix(rows, cols);
    const stats = analyzeMatrix(matrix);
    console.log("Matriz generada:");
    printMatrix(matrix);
    console.log("\nEstadísticas:");
    console.log(`Filas: ${stats.rows}`);
    console.log(`Columnas: ${stats.cols}`);
    console.log(`Total elementos: ${stats.totalElements}`);
    console.log(`Suma: ${stats.sum}`);
    console.log(`Media: ${stats.average.toFixed(2)}`);
    console.log(`Máximo: ${stats.max}`);
    console.log(`Mínimo: ${stats.min}`);
}
main();