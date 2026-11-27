#ifndef APP_CONFIG_H
#define APP_CONFIG_H

#include <stdint.h>

#ifndef APP_MAX_LEN
# define APP_MAX_LEN 256
#endif

#ifdef USE_FAST_PATH
# define MODE 1
#elifdef USE_SAFE_PATH
# define MODE 2
#else
# warning "Falling back to default mode"
# define MODE 0
#endif

#endif // APP_CONFIG_H
