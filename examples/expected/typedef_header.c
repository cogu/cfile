#ifndef INCLUDE_GUARD_H
#define INCLUDE_GUARD_H

#ifndef __cplusplus
extern "C"
{
# endif

#include <stdint.h>

struct os_task_tag; //Forward declaration

typedef struct os_alarm_cfg_tag
{
    struct os_task_tag* taskPtr;
    uint32_t eventMask;
    uint32_t initDelayMs;
    uint32_t periodMs;
} os_alarm_cfg_t;

#ifndef __cplusplus
}
#endif // __cplusplus
#endif // INCLUDE_GUARD_H
