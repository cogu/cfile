static int add(int a, int b);

static int add(int a, int b) {
    return a + b;
}

int compute(void) {
    int result = add(10, 20);
    return result;
}
