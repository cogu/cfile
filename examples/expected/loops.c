int compute_sum(int n) {
    int sum = 0;
    for (int i = 0, j = 0; i < n; i++, j+=2) {
        sum += i + j; // increment variable
    }
    while (sum > 100) {
        sum -= 10;
    }
    do {
        sum++;
    } while (sum < 10);
    return sum;
}
