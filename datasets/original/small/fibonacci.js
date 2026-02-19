function fibonacci(n) {
    if (!Number.isInteger(n) || n < 0) {
        throw new Error("Input must be a non-negative integer");
    } else if (n === 0) {
        return 0;
    } else if (n === 1) {
        return 1;
    } else {
        let a = 0;
        let b = 1;
        for (let i = 2; i <= n; i++) {
            let temp = a + b;
            a = b;
            b = temp;
        }
        return b;
    }
}
console.log(fibonacci(10));