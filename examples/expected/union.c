union raw_value {
    int x;
    char c[4];
};

union raw_value u1 = {1};
union raw_value u2 = {.c={1, 0, 0, 0}};
