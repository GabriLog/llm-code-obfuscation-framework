function sum(a, b) {
    return a + b;
}
function subtract(a, b) {
    return a - b;
}
function multiply(a, b) {
    return a * b;
}
function divide(a, b) {
    if (b === 0) return "Error: División por cero";
    return a / b;
}
function power(a, b) {
    return Math.pow(a, b);
}
function sqrt(a) {
    return Math.sqrt(a);
}
function factorial(n) {
    if (n < 0) return "Error: Factorial de número negativo";
    let result = 1;
    for (let i = 2; i <= n; i++) result *= i;
    return result;
}
function isPrime(n) {
    if (n <= 1) return false;
    for (let i = 2; i <= Math.sqrt(n); i++) {
        if (n % i === 0) return false;
    }
    return true;
}
function main() {
    const a = 12;
    const b = 5;
    console.log("Calculadora simple\n");
    console.log(`${a} + ${b} = ${sum(a, b)}`);
    console.log(`${a} - ${b} = ${subtract(a, b)}`);
    console.log(`${a} * ${b} = ${multiply(a, b)}`);
    console.log(`${a} / ${b} = ${divide(a, b)}`);
    console.log(`${a} ^ ${b} = ${power(a, b)}`);
    console.log(`√${a} = ${sqrt(a)}`);
    console.log(`${a}! = ${factorial(a)}`);
    console.log(`${a} es primo? ${isPrime(a)}`);
}
main();