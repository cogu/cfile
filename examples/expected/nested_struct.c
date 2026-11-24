#include <stdint.h>

struct example {
    struct addr_t {
        uint32_t port;
    } addr;
    union {
        uint8_t a8[4];
        uint16_t a16[2];
    } in_u;
};

struct example ex1 = {{80}, {{127, 0, 0, 1}}};
struct example ex2 = {.addr={.port=80}, .in_u={.a8={127, 0, 0, 1}}};
