function isPrime(n) {
    if (!Number.isInteger(n) || n < 0) {
        throw new Error("Input must be a non-negative integer");
    } else if (n <= 1) {
        return false;
    } else if (n <= 3) {
        return true;
    } else if (n % 2 === 0 || n % 3 === 0) {
        return false;
    } else {
        for (let i = 5; i * i <= n; i += 6) {
            if (n % i === 0 || n % (i + 2) === 0) {
                return false;
            }
        }
        return true;
    }
}
function analyzeNumbers(limit) {
    let primes = [];
    let sum = 0;
    for (let i = 1; i <= limit; i++) {
        if (isPrime(i)) {
            primes.push(i);
            sum += i;
        }
    }
    return {
        count: primes.length,
        sum: sum,
        average: primes.length > 0 ? sum / primes.length : 0,
        max: primes[primes.length - 1]
    };
}
function main() {
    const limit = 200;
    const result = analyzeNumbers(limit);
    console.log("Análisis de números primos:");
    console.log(`Límite: ${limit}`);
    console.log(`Cantidad: ${result.count}`);
    console.log(`Suma: ${result.sum}`);
    console.log(`Media: ${result.average.toFixed(2)}`);
    console.log(`Máximo: ${result.max}`);
}
main();